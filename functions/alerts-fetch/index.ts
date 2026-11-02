// Pulls official warnings into bsos_alerts every 15 minutes (called by pg_cron with the x-fetch-key header).
// Sources: Met Office (UK warnings, via MeteoAlarm's UK feed), Environment Agency (England floods), US National Weather Service,
// MeteoAlarm (Europe, 37 national services), GDACS (worldwide disasters). Each source is stored with a
// normalised level: 1 red/extreme, 2 amber/severe, 3 yellow/moderate, 4 information.
import "jsr:@supabase/functions-js/edge-runtime.d.ts";
import { createClient } from "jsr:@supabase/supabase-js@2";
import { ISO3 } from "./iso.ts";

const UA = { "User-Agent": "BlackoutSOS/1.0 (https://blackoutsos.com; alerts@blackoutsos.com)" };
const json = (body: unknown, status = 200) => new Response(JSON.stringify(body), { status, headers: { "Content-Type": "application/json" } });

type Row = {
  source: string; external_id: string; country: string; regions: string[]; area: string | null;
  level: number; severity: string; event: string; headline: string; summary: string | null; link: string | null;
  issued_at: string; expires_at: string | null;
};
const SEV = ["", "red", "amber", "yellow", "info"];
const clip = (s: string | null | undefined, n: number) => { if (!s) return null; const t = s.replace(/\s+/g, " ").trim(); return t.length > n ? t.slice(0, n - 1) + "…" : t; };
const dec = (s: string) => s.replace(/<!\[CDATA\[([\s\S]*?)\]\]>/g, "$1").replace(/<[^>]+>/g, "").replace(/&amp;/g, "&").replace(/&lt;/g, "<").replace(/&gt;/g, ">").replace(/&quot;/g, '"').replace(/&#39;|&apos;/g, "'").replace(/&nbsp;/g, " ").replace(/&#(\d+);/g, (_, n) => String.fromCharCode(+n)).trim();
const tag = (block: string, name: string) => { const m = block.match(new RegExp("<" + name + "(?:\\s[^>]*)?>([\\s\\S]*?)</" + name + ">")); return m ? dec(m[1]) : ""; };
const blocks = (xml: string, name: string) => Array.from(xml.matchAll(new RegExp("<" + name + "(?:\\s[^>]*)?>([\\s\\S]*?)</" + name + ">", "g"))).map((m) => m[1]);
const iso = (d: string | null | undefined) => { if (!d) return null; const t = Date.parse(d); return isNaN(t) ? null : new Date(t).toISOString(); };
async function get(url: string, headers: Record<string, string> = {}, ms = 20000): Promise<string> {
  const c = new AbortController(); const t = setTimeout(() => c.abort(), ms);
  try { const r = await fetch(url, { headers: { ...UA, ...headers }, signal: c.signal }); if (!r.ok) throw new Error(`${r.status} ${url}`); return await r.text(); }
  finally { clearTimeout(t); }
}

// ---------- Met Office regions (UK warnings arrive through MeteoAlarm's UK feed, which names these regions) ----------
const MO_CODES: Record<string, string> = { "Orkney & Shetland": "os", "Highlands & Eilean Siar": "he", "Grampian": "gr", "Central, Tayside & Fife": "ta", "Strathclyde": "st", "Dumfries, Galloway, Lothian & Borders": "dg", "Northern Ireland": "ni", "Wales": "wl", "North West England": "nw", "North East England": "ne", "Yorkshire & Humber": "yh", "West Midlands": "wm", "East Midlands": "em", "East of England": "ee", "South West England": "sw", "London & South East England": "se" };

// ---------- Environment Agency: England flood warnings (levels 1-2) ----------
const EA_TO_REGION: [RegExp, string][] = [[/east anglia|norfolk|suffolk|cambridge|essex|bedford|hertford/i, "ee"], [/thames|london|surrey|kent|sussex|hampshire|solent|south downs|berkshire|oxford|buckingham/i, "se"], [/yorkshire|humber/i, "yh"], [/cumbria|lancashire|manchester|merseyside|cheshire/i, "nw"], [/north east|northumberland|durham|tees/i, "ne"], [/devon|cornwall|wessex|somerset|dorset|wiltshire|gloucester|bristol/i, "sw"], [/lincolnshire|northampton|east midlands|derby|nottingham|leicester/i, "em"], [/west midlands|shropshire|hereford|worcester|stafford|warwick/i, "wm"]];
async function ea(): Promise<Row[]> {
  const data = JSON.parse(await get("https://environment.data.gov.uk/flood-monitoring/id/floods?min-severity=2"));
  const rows: Row[] = [];
  for (const f of data.items || []) {
    const lvl = Number(f.severityLevel); if (!(lvl >= 1 && lvl <= 2)) continue;
    const where = `${f.description || ""} ${f.eaAreaName || ""} ${f.floodArea?.county || ""}`;
    const region = EA_TO_REGION.find(([re]) => re.test(where))?.[1];
    rows.push({ source: "ea", external_id: String(f.floodAreaID || f["@id"]), country: "GB", regions: region ? [region] : [], area: clip(`${f.description || ""}${f.floodArea?.county ? ", " + f.floodArea.county : ""}`, 160),
      level: lvl, severity: SEV[lvl], event: lvl === 1 ? "Severe flood warning" : "Flood warning", headline: clip(`${lvl === 1 ? "Severe flood warning" : "Flood warning"}: ${f.description}`, 200)!,
      summary: clip(f.message, 400), link: "https://check-for-flooding.service.gov.uk/", issued_at: iso(f.timeRaised) || new Date().toISOString(), expires_at: null });
  }
  return rows;
}

// ---------- US National Weather Service: active Severe and Extreme alerts ----------
async function nws(): Promise<Row[]> {
  const data = JSON.parse(await get("https://api.weather.gov/alerts/active?status=actual&message_type=alert,update&severity=Severe,Extreme", { Accept: "application/geo+json" }, 30000));
  const rows: Row[] = [];
  for (const f of data.features || []) {
    const p = f.properties || {}; if (!p.event) continue;
    const states = Array.from(new Set(((p.geocode?.UGC || []) as string[]).map((u) => u.slice(0, 2)).filter((s) => /^[A-Z]{2}$/.test(s))));
    const level = p.severity === "Extreme" ? 1 : 2;
    rows.push({ source: "nws", external_id: String(p.id).slice(0, 300), country: "US", regions: states, area: clip(p.areaDesc, 160), level, severity: SEV[level], event: clip(p.event, 80)!,
      headline: clip(p.headline || p.event, 200)!, summary: clip(p.description, 400), link: `https://alerts.weather.gov/search?id=${encodeURIComponent(p.id)}`,
      issued_at: iso(p.sent) || new Date().toISOString(), expires_at: iso(p.ends || p.expires) });
  }
  return rows;
}

// ---------- MeteoAlarm: national services across Europe ----------
const MA: Record<string, string> = { "united-kingdom": "GB", austria: "AT", belgium: "BE", "bosnia-herzegovina": "BA", bulgaria: "BG", croatia: "HR", cyprus: "CY", czechia: "CZ", denmark: "DK", estonia: "EE", finland: "FI", france: "FR", germany: "DE", greece: "GR", hungary: "HU", iceland: "IS", ireland: "IE", israel: "IL", italy: "IT", latvia: "LV", lithuania: "LT", luxembourg: "LU", malta: "MT", moldova: "MD", montenegro: "ME", netherlands: "NL", "republic-of-north-macedonia": "MK", norway: "NO", poland: "PL", portugal: "PT", romania: "RO", serbia: "RS", slovakia: "SK", slovenia: "SI", spain: "ES", sweden: "SE", switzerland: "CH", ukraine: "UA" };
async function meteoalarm(errors: string[], failed: string[]): Promise<Row[]> {
  const rows: Row[] = [];
  await Promise.all(Object.entries(MA).map(async ([slug, cc]) => {
    let xml = "";
    try { xml = await get(`https://feeds.meteoalarm.org/feeds/meteoalarm-legacy-atom-${slug}`); } catch (e) { errors.push(`meteoalarm:${slug}: ${String(e).slice(0, 80)}`); failed.push(cc); return; }
    const grouped = new Map<string, { areas: string[]; e: string; row: Row }>();
    for (const en of blocks(xml, "entry")) {
      if (tag(en, "cap:status") !== "Actual") continue;
      const sev = tag(en, "cap:severity"); const level = sev === "Extreme" ? 1 : sev === "Severe" ? 2 : sev === "Moderate" ? 3 : 0;
      if (!level) continue;
      const id = tag(en, "cap:identifier") || tag(en, "id"); const area = tag(en, "cap:areaDesc");
      const key = `${cc}:${id}`;
      if (grouped.has(key)) { grouped.get(key)!.areas.push(area); continue; }
      const linkM = en.match(/<link[^>]*rel="alternate"[^>]*href="([^"]+)"/) || en.match(/<link title="[^"]*" href="([^"]+)"/);
      const title = tag(en, "title").replace(/\s+issued for\s+.*$/i, "");
      const uk = cc === "GB";
      grouped.set(key, { areas: [area], e: tag(en, "cap:event"), row: { source: uk ? "metoffice" : "meteoalarm", external_id: key.slice(0, 300), country: cc, regions: [], area: "", level, severity: SEV[level], event: clip(tag(en, "cap:event") || title, 80)!,
        headline: clip(title || tag(en, "cap:event"), 200)!, summary: null, link: uk ? "https://www.metoffice.gov.uk/weather/warnings-and-advice/uk-warnings" : (linkM ? dec(linkM[1]) : `https://meteoalarm.org?region=${cc}`), issued_at: iso(tag(en, "cap:sent") || tag(en, "published")) || new Date().toISOString(), expires_at: iso(tag(en, "cap:expires")) } });
    }
    for (const g of grouped.values()) {
      const a = Array.from(new Set(g.areas.flatMap((x) => x.split(" | ")).map((x) => x.trim()).filter(Boolean)));
      if (cc === "GB") g.row.regions = Array.from(new Set(a.map((n) => MO_CODES[n]).filter(Boolean) as string[]));
      g.row.area = clip(a.length > 6 ? a.slice(0, 6).join(", ") + ` +${a.length - 6} more` : a.join(", "), 160); rows.push(g.row);
    }
  }));
  return rows;
}

// ---------- GDACS: worldwide disasters (Orange and Red; Green kept as information) ----------
const GD_TYPES: Record<string, string> = { EQ: "Earthquake", TC: "Tropical cyclone", FL: "Flood", VO: "Volcanic activity", DR: "Drought", WF: "Wildfire", TS: "Tsunami" };
async function gdacs(): Promise<Row[]> {
  const xml = await get("https://www.gdacs.org/xml/rss.xml", {}, 30000);
  const rows: Row[] = [];
  for (const it of blocks(xml, "item")) {
    if (tag(it, "gdacs:iscurrent") !== "true") continue;
    const lvlName = tag(it, "gdacs:alertlevel"); const level = lvlName === "Red" ? 1 : lvlName === "Orange" ? 2 : 4;
    const guid = tag(it, "guid"); const type = tag(it, "gdacs:eventtype");
    const iso3s = tag(it, "gdacs:iso3").split(/[,;]/).map((s) => s.trim().toUpperCase()).filter(Boolean);
    const countries = iso3s.map((c) => ISO3[c]).filter(Boolean) as string[];
    if (!countries.length) continue;
    const name = tag(it, "gdacs:eventname");
    for (const cc of Array.from(new Set(countries))) {
      rows.push({ source: "gdacs", external_id: `${guid}:${cc}`, country: cc, regions: [], area: clip(tag(it, "gdacs:country"), 160), level, severity: SEV[level],
        event: (GD_TYPES[type] || "Disaster") + (name ? ` ${name}` : ""), headline: clip(tag(it, "title").replace(/^(Green|Orange|Red)\s+/i, "").replace(/^notification for\s+/i, "").replace(/^\w/, (c) => c.toUpperCase()), 200)!, summary: clip(tag(it, "description"), 400),
        link: tag(it, "link") || "https://www.gdacs.org/", issued_at: iso(tag(it, "gdacs:fromdate") || tag(it, "pubDate")) || new Date().toISOString(), expires_at: null });
    }
  }
  return rows;
}

Deno.serve(async (req: Request) => {
  if (req.method === "OPTIONS") return new Response("ok");
  const supabase = createClient(Deno.env.get("SUPABASE_URL")!, Deno.env.get("SUPABASE_SERVICE_ROLE_KEY")!);
  const { data: setting } = await supabase.from("bsos_settings").select("value").eq("key", "alerts_fetch_key").maybeSingle();
  const given = req.headers.get("x-fetch-key") || new URL(req.url).searchParams.get("key") || "";
  if (!setting?.value || given !== setting.value) return json({ error: "Not allowed" }, 403);

  const run_id = crypto.randomUUID(); const started = new Date().toISOString();
  const { data: runRow } = await supabase.from("bsos_alert_runs").insert({ started_at: started }).select("id").single();
  const counts: Record<string, number> = {}; const errors: string[] = []; const failedCountries: string[] = [];
  const sources: [string, string[], () => Promise<Row[]>][] = [["ea", ["ea"], ea], ["nws", ["nws"], nws], ["meteoalarm", ["meteoalarm", "metoffice"], () => meteoalarm(errors, failedCountries)], ["gdacs", ["gdacs"], gdacs]];
  await Promise.all(sources.map(async ([name, owns, fn]) => {
    let rows: Row[];
    try { rows = await fn(); } catch (e) { errors.push(`${name}: ${String(e).slice(0, 120)}`); return; }
    // de-duplicate by external_id within the source
    const seen = new Set<string>(); rows = rows.filter((r) => (seen.has(r.external_id) ? false : (seen.add(r.external_id), true)));
    for (let i = 0; i < rows.length; i += 200) {
      const chunk = rows.slice(i, i + 200).map((r) => ({ ...r, run_id, active: true, fetched_at: started }));
      const { error } = await supabase.from("bsos_alerts").upsert(chunk, { onConflict: "source,external_id" });
      if (error) { errors.push(`${name} upsert: ${error.message.slice(0, 120)}`); return; }
    }
    // anything from these sources that was not in this run has ended
    for (const src of owns) {
      let q = supabase.from("bsos_alerts").update({ active: false }).eq("source", src).eq("active", true).neq("run_id", run_id);
      if (name === "meteoalarm" && failedCountries.length) q = q.not("country", "in", `(${failedCountries.join(",")})`);  // a feed that failed keeps its last alerts
      const { error: e2 } = await q;
      if (e2) errors.push(`${src} close: ${e2.message.slice(0, 120)}`);
      counts[src] = rows.filter((r) => r.source === src).length;
    }
  }));
  // tidy: drop inactive rows older than 14 days
  await supabase.from("bsos_alerts").delete().eq("active", false).lt("fetched_at", new Date(Date.now() - 14 * 864e5).toISOString());
  if (runRow?.id) await supabase.from("bsos_alert_runs").update({ finished_at: new Date().toISOString(), ok: errors.length === 0, counts, errors }).eq("id", runRow.id);
  return json({ ok: errors.length === 0, run_id, counts, errors });
});

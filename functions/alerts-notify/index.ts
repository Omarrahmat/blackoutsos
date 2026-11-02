// Emails subscribers who asked for warnings when a red or amber alert is in force for their area.
// Runs a couple of minutes after each alerts-fetch (pg_cron, x-fetch-key). One email per person per 6 hours at most,
// each alert emailed to a person once. Logged in bsos_emails (kind "alert", ref = alert id).
import "jsr:@supabase/functions-js/edge-runtime.d.ts";
import { createClient } from "jsr:@supabase/supabase-js@2";
import { CORS, json } from "./_shared.ts";
import { SITE, h, layout, send, unsubUrl } from "./_email.ts";

const NAMES: Record<string, string> = { metoffice: "Met Office", ea: "Environment Agency", nws: "National Weather Service", meteoalarm: "the national weather service", gdacs: "GDACS" };
const FIRST_HOUR: Record<string, string> = {
  flood: "Move cars, documents and medicines above ground-floor level; check the meeting point with everyone in the house; keep the go bag by the door.",
  wind: "Bring in or tie down anything loose outside; charge phones and the power bank now; keep the go bag by the door and the torch to hand.",
  rain: "Check drains and gullies you can safely reach; charge phones now; know where the stopcock is; keep the go bag by the door.",
  snow: "Fill flasks and water containers; charge everything; put the hand warmers and the foil blankets at the top of the bag; check on anyone nearby who is alone.",
  ice: "Fill flasks; charge everything; grit the step; keep the hand warmers at the top of the bag.",
  thunder: "Unplug what you can; charge phones first; keep the torch and glow sticks to hand.",
  heat: "Fill water containers now; close curtains on the sun side; check on anyone nearby who is alone or unwell.",
  fog: "Avoid driving if you can; if you must, lights on and slow down.",
  tornado: "Decide now where you will shelter (lowest floor, interior room, no windows); shoes on; go bag within reach.",
  hurricane: "Fill the bath and water containers; charge everything; fuel the car; follow evacuation orders when they come.",
  fire: "Pack the car with the go bags, documents and medicines; close windows and vents; follow evacuation orders at once.",
};
function firstHour(event: string): string {
  const e = event.toLowerCase();
  for (const k of Object.keys(FIRST_HOUR)) if (e.includes(k)) return FIRST_HOUR[k];
  return "Charge phones and the power bank now; fill a water container; keep the go bag by the door; check on anyone nearby who is alone.";
}

Deno.serve(async (req: Request) => {
  if (req.method === "OPTIONS") return new Response("ok", { headers: CORS });
  const supabase = createClient(Deno.env.get("SUPABASE_URL")!, Deno.env.get("SUPABASE_SERVICE_ROLE_KEY")!);
  const { data: setting } = await supabase.from("bsos_settings").select("value").eq("key", "alerts_fetch_key").maybeSingle();
  const secret = setting?.value || "";
  if (!secret || (req.headers.get("x-fetch-key") || new URL(req.url).searchParams.get("key")) !== secret) return json({ error: "Not allowed" }, 403);

  const { data: subs } = await supabase.from("bsos_subscribers").select("id,email,country,region,last_alert_email_at").eq("alerts_opt_in", true).is("unsubscribed_at", null).not("country", "is", null);
  if (!subs?.length) return json({ ok: true, recipients: 0 });
  const countries = Array.from(new Set(subs.map((s: any) => s.country)));
  const { data: alerts } = await supabase.from("bsos_alerts_public").select("id,source,country,regions,area,level,event,headline,summary,link,issued_at,expires_at").in("country", countries).lte("level", 2).order("level").order("issued_at", { ascending: false });
  if (!alerts?.length) return json({ ok: true, recipients: 0, alerts: 0 });
  const since = new Date(Date.now() - 6 * 3600e3).toISOString();
  const results = { sent: 0, failed: 0, skipped: 0, recipients: 0 };
  for (const s of subs as any[]) {
    if (s.last_alert_email_at && s.last_alert_email_at > since) continue;
    const mine = alerts.filter((a: any) => a.country === s.country && (!s.region || !a.regions?.length || a.regions.includes(s.region)));
    if (!mine.length) continue;
    const { data: done } = await supabase.from("bsos_emails").select("ref").eq("kind", "alert").eq("to_email", s.email);
    const seen = new Set((done || []).map((d: any) => d.ref));
    const fresh = mine.filter((a: any) => !seen.has(String(a.id))).slice(0, 5);
    if (!fresh.length) continue;
    const top = fresh[0];
    const unsub = await unsubUrl(s.email, secret);
    const items = fresh.map((a: any) => `<p style="margin:0 0 12px;padding:12px 14px;border-left:4px solid ${a.level === 1 ? "#ff3b30" : "#ff9f0a"};background:#161616;color:#ededed"><strong>${h.esc(a.event)}</strong><br><span style="color:#b5b5b5">${h.esc(a.area || "")}</span><br><span style="color:#9a9a9a;font-size:13px">${h.esc(NAMES[a.source] || a.source)}${a.expires_at ? " · until " + new Date(a.expires_at).toUTCString().slice(0, 22) + " UTC" : ""} · <a href="${h.esc(a.link || SITE + "/alerts.html")}" style="color:#9a9a9a">details</a></span></p>`).join("");
    const html = layout(`${top.level === 1 ? "Red" : "Amber"} warning for your area`,
      h.h1(`${top.level === 1 ? "Red" : "Amber"} warning: ${top.event}`) + h.p(`In force for ${h.esc(top.area || s.country)}. ${fresh.length > 1 ? `${fresh.length} serious warnings are current for your area.` : ""}`) + items +
      `<p style="margin:18px 0 6px;color:#fff;font-weight:600">The first hour</p>` + h.p(h.esc(firstHour(top.event))) + h.btn(`${SITE}/alerts.html`, "See all warnings for your area") +
      h.small("Official information comes from the agency named on each warning. Follow instructions from your local authorities and emergency services first."), unsub, `${top.event} — ${top.area || ""}`);
    results.recipients++;
    const status = await send(supabase, { to: s.email, kind: "alert", ref: String(top.id), subject: `${top.level === 1 ? "Red" : "Amber"} warning: ${top.event} — ${(top.area || "").slice(0, 60)}`, html, text: `${top.event} — ${top.area}. ${firstHour(top.event)} ${SITE}/alerts.html`, unsub });
    (results as any)[status]++;
    if (status !== "failed") {
      await supabase.from("bsos_subscribers").update({ last_alert_email_at: new Date().toISOString() }).eq("id", s.id);
      for (const a of fresh.slice(1)) await supabase.from("bsos_emails").insert({ kind: "alert", to_email: s.email, subject: "(included)", ref: String(a.id), status });
    }
  }
  return json({ ok: true, ...results });
});

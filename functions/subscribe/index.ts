// POST { email, source, bag, bought, country, region, locale, alerts } -> newsletter, waitlist and warning-email lists.
// One row per email: a later signup adds to it (a waitlist signup never removes an alerts opt-in, and vice versa).
import "jsr:@supabase/functions-js/edge-runtime.d.ts";
import { createClient } from "jsr:@supabase/supabase-js@2";
import { CORS, json } from "../_shared.ts";

Deno.serve(async (req: Request) => {
  if (req.method === "OPTIONS") return new Response("ok", { headers: CORS });
  if (req.method !== "POST") return json({ error: "POST only" }, 405);
  let body: any; try { body = await req.json(); } catch { return json({ error: "Bad request" }, 400); }
  const email = String(body.email || "").trim().toLowerCase();
  if (!/^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(email) || email.length > 254) return json({ error: "That email address doesn't look right." }, 400);
  const clip = (v: unknown, n: number) => (v == null || v === "" ? null : String(v).slice(0, n));
  const supabase = createClient(Deno.env.get("SUPABASE_URL")!, Deno.env.get("SUPABASE_SERVICE_ROLE_KEY")!);

  const { data: existing } = await supabase.from("bsos_subscribers").select("id,source,bag,bought,country,region,alerts_opt_in,locale").eq("email", email).maybeSingle();
  const country = /^[A-Za-z]{2}$/.test(String(body.country || "")) ? String(body.country).toUpperCase() : null;
  const region = clip(body.region, 12);
  const row: any = { email, unsubscribed_at: null, locale: clip(body.locale, 12) ?? existing?.locale ?? null };
  // source: keep the first one, note the latest in a list ("site,waitlist,alerts")
  const src = clip(body.source, 20) || "site";
  row.source = existing?.source ? (existing.source.split(",").includes(src) ? existing.source : (existing.source + "," + src).slice(0, 60)) : src;
  if (body.bag) row.bag = clip(body.bag, 40); else if (existing?.bag) row.bag = existing.bag;
  if (body.bought) row.bought = clip(body.bought, 10); else if (existing?.bought) row.bought = existing.bought;
  if (country) { row.country = country; row.region = region; } else if (existing) { row.country = existing.country; row.region = existing.region; }
  row.alerts_opt_in = body.alerts === "yes" || body.alerts === true ? true : (existing?.alerts_opt_in ?? false);
  const { error } = await supabase.from("bsos_subscribers").upsert(row, { onConflict: "email" });
  if (error) return json({ error: "We couldn't save that. Please try again." }, 500);
  return json({ ok: true });
});

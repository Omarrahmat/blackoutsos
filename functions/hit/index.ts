// POST { s, p, r, c, g, l, d } -> one page view. No cookies: the page sends a random per-tab session id.
// The country and region are the viewer's own choice on the site (first guessed from their device's time zone).
import "jsr:@supabase/functions-js/edge-runtime.d.ts";
import { createClient } from "jsr:@supabase/supabase-js@2";

const CORS = { "Access-Control-Allow-Origin": "*", "Access-Control-Allow-Headers": "content-type", "Access-Control-Allow-Methods": "POST, OPTIONS" };
const ok = () => new Response(null, { status: 204, headers: CORS });

Deno.serve(async (req: Request) => {
  if (req.method === "OPTIONS") return new Response("ok", { headers: CORS });
  if (req.method !== "POST") return ok();
  let b: any; try { b = await req.json(); } catch { return ok(); }
  const clip = (v: unknown, n: number) => (v == null || v === "" ? null : String(v).slice(0, n));
  const session = clip(b.s, 40); const path = clip(b.p, 200);
  if (!session || !path || !/^[A-Za-z0-9_-]{8,40}$/.test(session)) return ok();
  const ua = req.headers.get("user-agent") || "";
  if (/bot|crawl|spider|slurp|facebookexternalhit|preview|headless|lighthouse/i.test(ua)) return ok();
  const ip = (req.headers.get("x-forwarded-for") || "").split(",")[0].trim();
  const day = new Date().toISOString().slice(0, 10);
  const buf = await crypto.subtle.digest("SHA-256", new TextEncoder().encode(`${day}:${ip}:${ua}`));
  const ip_hash = Array.from(new Uint8Array(buf)).slice(0, 8).map((x) => x.toString(16).padStart(2, "0")).join("");
  let referrer = clip(b.r, 200);
  try { if (referrer) { const u = new URL(referrer); referrer = u.hostname.replace(/^www\./, ""); if (/blackoutsos\.com$/.test(referrer)) referrer = null; } } catch { referrer = null; }
  const supabase = createClient(Deno.env.get("SUPABASE_URL")!, Deno.env.get("SUPABASE_SERVICE_ROLE_KEY")!);
  await supabase.from("bsos_visits").insert({
    session, path, referrer, ip_hash,
    country: /^[A-Za-z]{2}$/.test(String(b.c || "")) ? String(b.c).toUpperCase() : null,
    region: clip(b.g, 12), lang: clip(b.l, 12), device: b.d === "m" ? "mobile" : "desktop",
  });
  return ok();
});

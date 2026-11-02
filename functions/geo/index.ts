// GET -> { country, region } for the visitor, from their connection's IP. Nothing is stored.
// US: state code. UK: nearest Met Office warning region. Elsewhere: country only.
import "jsr:@supabase/functions-js/edge-runtime.d.ts";

const CORS = { "Access-Control-Allow-Origin": "*", "Access-Control-Allow-Headers": "content-type", "Access-Control-Allow-Methods": "GET, OPTIONS", "Cache-Control": "private, max-age=3600" };
const UK: [string, number, number][] = [["se", 51.4, -0.4], ["ee", 52.3, 0.8], ["sw", 50.8, -3.6], ["wm", 52.5, -2.1], ["em", 52.9, -1.0], ["yh", 53.8, -1.3], ["nw", 53.7, -2.7], ["ne", 54.9, -1.7], ["wl", 52.2, -3.6], ["ni", 54.6, -6.6], ["st", 55.8, -4.6], ["dg", 55.4, -3.1], ["ta", 56.3, -3.6], ["gr", 57.2, -2.4], ["he", 57.5, -5.2], ["os", 59.6, -2.2]];
function ukRegion(lat: number, lon: number) {
  let best = "se", d = 1e9;
  for (const [c, a, o] of UK) { const x = (lat - a) ** 2 + ((lon - o) * Math.cos(lat * Math.PI / 180)) ** 2; if (x < d) { d = x; best = c; } }
  return best;
}
async function look(ip: string) {
  try {
    const r = await fetch(`https://ipwho.is/${ip}`, { signal: AbortSignal.timeout(3000) }); const j = await r.json();
    if (j.success) return { country: j.country_code, region_code: j.region_code, lat: j.latitude, lon: j.longitude };
  } catch { /* fall through */ }
  try {
    const r = await fetch(`https://ipapi.co/${ip}/json/`, { signal: AbortSignal.timeout(3000) }); const j = await r.json();
    if (j.country_code) return { country: j.country_code, region_code: j.region_code, lat: j.latitude, lon: j.longitude };
  } catch { /* none */ }
  return null;
}
Deno.serve(async (req: Request) => {
  if (req.method === "OPTIONS") return new Response("ok", { headers: CORS });
  const ip = (req.headers.get("x-forwarded-for") || "").split(",")[0].trim();
  const g = ip ? await look(ip) : null;
  if (!g) return new Response(JSON.stringify({ country: null, region: null }), { headers: { ...CORS, "Content-Type": "application/json" } });
  let region: string | null = null;
  if (g.country === "US" && /^[A-Z]{2}$/.test(g.region_code || "")) region = g.region_code;
  if (g.country === "GB" && typeof g.lat === "number") region = ukRegion(g.lat, g.lon);
  return new Response(JSON.stringify({ country: g.country, region }), { headers: { ...CORS, "Content-Type": "application/json" } });
});

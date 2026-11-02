// POST { email, source, bag, bought } -> Be Ready alerts and rotation reminders list.
import "jsr:@supabase/functions-js/edge-runtime.d.ts";
import { createClient } from "jsr:@supabase/supabase-js@2";
import { CORS, json } from "../_shared.ts";

Deno.serve(async (req: Request) => {
  if (req.method === "OPTIONS") return new Response("ok", { headers: CORS });
  if (req.method !== "POST") return json({ error: "POST only" }, 405);
  let body: any; try { body = await req.json(); } catch { return json({ error: "Bad request" }, 400); }
  const email = String(body.email || "").trim().toLowerCase();
  if (!/^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(email) || email.length > 254) return json({ error: "That email address doesn't look right." }, 400);
  const clip = (v: unknown, n: number) => (v == null ? null : String(v).slice(0, n));
  const supabase = createClient(Deno.env.get("SUPABASE_URL")!, Deno.env.get("SUPABASE_SERVICE_ROLE_KEY")!);
  const row: any = { email, source: clip(body.source, 40), unsubscribed_at: null };
  if (body.bag) row.bag = clip(body.bag, 40);
  if (body.bought) row.bought = clip(body.bought, 10);
  const { error } = await supabase.from("bsos_subscribers").upsert(row, { onConflict: "email" });
  if (error) return json({ error: "We couldn't save that. Please try again." }, 500);
  return json({ ok: true });
});

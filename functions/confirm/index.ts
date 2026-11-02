// POST { session_id } -> records the paid order (idempotent). Called by checkout/success.html.
import "jsr:@supabase/functions-js/edge-runtime.d.ts";
import { createClient } from "jsr:@supabase/supabase-js@2";
import { CORS, json, stripeHeaders, recordSession } from "../_shared.ts";

Deno.serve(async (req: Request) => {
  if (req.method === "OPTIONS") return new Response("ok", { headers: CORS });
  if (req.method !== "POST") return json({ error: "POST only" }, 405);
  const key = Deno.env.get("STRIPE_SECRET_KEY");
  if (!key) return json({ error: "Payments are not switched on." }, 503);
  let body: any; try { body = await req.json(); } catch { return json({ error: "Bad request" }, 400); }
  const id = String(body.session_id || "");
  if (!/^cs_[A-Za-z0-9_]+$/.test(id)) return json({ error: "Bad session id" }, 400);
  const r = await fetch(`https://api.stripe.com/v1/checkout/sessions/${id}`, { headers: stripeHeaders(key) });
  const s = await r.json();
  if (!r.ok) return json({ error: "Unknown session" }, 404);
  if (s.payment_status !== "paid") return json({ ok: false, status: s.payment_status });
  const supabase = createClient(Deno.env.get("SUPABASE_URL")!, Deno.env.get("SUPABASE_SERVICE_ROLE_KEY")!);
  const orderId = await recordSession(supabase, s);
  return json({ ok: true, order_id: orderId, email: s.customer_details?.email ?? null });
});

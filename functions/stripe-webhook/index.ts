// Stripe webhook: checkout.session.completed -> record the order. The event is re-fetched from Stripe by id, so no signing secret is needed.
import "jsr:@supabase/functions-js/edge-runtime.d.ts";
import { createClient } from "jsr:@supabase/supabase-js@2";
import { json, stripeHeaders, recordSession } from "../_shared.ts";

Deno.serve(async (req: Request) => {
  if (req.method !== "POST") return json({ error: "POST only" }, 405);
  const key = Deno.env.get("STRIPE_SECRET_KEY");
  if (!key) return json({ error: "Payments are not switched on." }, 503);
  let evt: any; try { evt = await req.json(); } catch { return json({ error: "Bad request" }, 400); }
  const id = String(evt?.id || "");
  if (!/^evt_[A-Za-z0-9_]+$/.test(id)) return json({ error: "Bad event id" }, 400);
  // Verify by fetching the event from Stripe rather than trusting the body.
  const r = await fetch(`https://api.stripe.com/v1/events/${id}`, { headers: stripeHeaders(key) });
  const event = await r.json();
  if (!r.ok) return json({ error: "Unknown event" }, 400);
  if (event.type === "checkout.session.completed" || event.type === "checkout.session.async_payment_succeeded") {
    const s = event.data?.object;
    if (s?.payment_status === "paid") {
      const supabase = createClient(Deno.env.get("SUPABASE_URL")!, Deno.env.get("SUPABASE_SERVICE_ROLE_KEY")!);
      await recordSession(supabase, s);
    }
  }
  return json({ received: true });
});

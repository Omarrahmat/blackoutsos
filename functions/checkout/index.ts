// POST { items: [{sku, qty}], base } -> { url } : creates a Stripe Checkout Session. Prices come from the database, never the browser.
import "jsr:@supabase/functions-js/edge-runtime.d.ts";
import { createClient } from "jsr:@supabase/supabase-js@2";
import { CORS, json, stripeHeaders } from "../_shared.ts";

Deno.serve(async (req: Request) => {
  if (req.method === "OPTIONS") return new Response("ok", { headers: CORS });
  if (req.method !== "POST") return json({ error: "POST only" }, 405);
  const key = Deno.env.get("STRIPE_SECRET_KEY");
  if (!key) return json({ error: "Checkout is not switched on yet. Email hello@blackoutsos.com and we will take your order by hand." }, 503);
  let body: any; try { body = await req.json(); } catch { return json({ error: "Bad request" }, 400); }
  const items: any[] = Array.isArray(body.items) ? body.items.slice(0, 20) : [];
  const base = typeof body.base === "string" && /^https:\/\/[^\s"']+\/$/.test(body.base) ? body.base : "https://blackoutsos.com/";
  if (!items.length) return json({ error: "Your basket is empty." }, 400);

  const supabase = createClient(Deno.env.get("SUPABASE_URL")!, Deno.env.get("SUPABASE_SERVICE_ROLE_KEY")!);
  const skus = [...new Set(items.map((i) => String(i.sku)))];
  const { data: products, error } = await supabase.from("bsos_products").select("sku,name,variant,price_pence,active,stock").in("sku", skus);
  if (error) return json({ error: "The catalogue is unavailable right now." }, 500);
  const by: Record<string, any> = Object.fromEntries((products || []).map((p: any) => [p.sku, p]));

  const p = new URLSearchParams();
  p.set("mode", "payment");
  p.set("success_url", base + "checkout/success.html?session_id={CHECKOUT_SESSION_ID}");
  p.set("cancel_url", base + "checkout/cancel.html");
  p.set("currency", "gbp");
  p.set("shipping_address_collection[allowed_countries][0]", "GB");
  p.set("phone_number_collection[enabled]", "true");
  p.set("billing_address_collection", "auto");
  p.set("customer_creation", "always");
  p.set("allow_promotion_codes", "true");
  p.set("custom_text[submit][message]", "Assembled to order in the UK and dispatched within three working days. Free tracked delivery.");
  let n = 0; const meta: string[] = []; let total = 0;
  for (const it of items) {
    const prod = by[String(it.sku)];
    const qty = Math.max(1, Math.min(10, parseInt(it.qty) || 1));
    if (!prod || !prod.active) return json({ error: `${it.sku} is not available.` }, 400);
    if ((prod.stock || 0) < qty) return json({ error: `${prod.name}${prod.variant ? " (" + prod.variant + ")" : ""} is not in stock yet. Join the list on its page and we will email you the day it is.` }, 409);
    p.set(`line_items[${n}][quantity]`, String(qty));
    p.set(`line_items[${n}][price_data][currency]`, "gbp");
    p.set(`line_items[${n}][price_data][unit_amount]`, String(prod.price_pence));
    p.set(`line_items[${n}][price_data][product_data][name]`, `Blackout SOS ${prod.name}` + (prod.variant ? ` (${prod.variant})` : ""));
    p.set(`line_items[${n}][price_data][product_data][metadata][sku]`, prod.sku);
    meta.push(`${prod.sku}:${qty}`); total += prod.price_pence * qty; n++;
  }
  p.set("metadata[items]", meta.join(","));
  p.set("metadata[source]", "blackoutsos.com");
  const r = await fetch("https://api.stripe.com/v1/checkout/sessions", { method: "POST", headers: stripeHeaders(key), body: p });
  const s = await r.json();
  if (!r.ok) return json({ error: s?.error?.message || "Stripe could not start the checkout." }, 502);
  return json({ url: s.url, id: s.id, total_pence: total });
});

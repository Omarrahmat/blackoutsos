// POST { items: [{sku, qty}], base } -> { url } : creates a Stripe Checkout Session. Prices come from the database, never the browser.
import "jsr:@supabase/functions-js/edge-runtime.d.ts";
import { createClient } from "jsr:@supabase/supabase-js@2";
import { CORS, json, stripeHeaders } from "../_shared.ts";
import { SHIP, quote } from "../_shipping.ts";

Deno.serve(async (req: Request) => {
  if (req.method === "OPTIONS") return new Response("ok", { headers: CORS });
  if (req.method !== "POST") return json({ error: "POST only" }, 405);
  const key = Deno.env.get("STRIPE_SECRET_KEY");
  if (!key) return json({ error: "Checkout is not switched on yet. Email hello@blackoutsos.com and we will take your order by hand." }, 503);
  let body: any; try { body = await req.json(); } catch { return json({ error: "Bad request" }, 400); }
  const items: any[] = Array.isArray(body.items) ? body.items.slice(0, 20) : [];
  const base = typeof body.base === "string" && /^https:\/\/[^\s"']+\/$/.test(body.base) ? body.base : "https://blackoutsos.com/";
  if (!items.length) return json({ error: "Your basket is empty." }, 400);

  const country = /^[A-Za-z]{2}$/.test(String(body.country || "")) ? String(body.country).toUpperCase() : "GB";
  if ((SHIP.noShip as readonly string[]).includes(country)) return json({ error: "We can't deliver to that country yet. Email hello@blackoutsos.com and we will see what we can do." }, 400);
  const supabase = createClient(Deno.env.get("SUPABASE_URL")!, Deno.env.get("SUPABASE_SERVICE_ROLE_KEY")!);
  // Currency: the one the site showed. Same rounding as assets/currency.js so the price charged is the price shown.
  let cur = /^[A-Z]{3}$/.test(String(body.currency || "")) ? String(body.currency) : "GBP";
  let rate = 1;
  if (cur !== "GBP") { const { data: fx } = await supabase.from("bsos_fx").select("per_gbp").eq("code", cur).maybeSingle(); if (fx?.per_gbp) rate = Number(fx.per_gbp); else cur = "GBP"; }
  const ZERO: Record<string, 1> = { JPY: 1, KRW: 1, ISK: 1 };
  const nice = (x: number) => x <= 0 ? 0 : x < 1000 ? Math.ceil((x + 1) / 5) * 5 - 1 : (() => { const m = Math.pow(10, Math.floor(Math.log10(x)) - 1); return Math.ceil(x / m) * m; })();
  const minor = (pence: number) => { if (cur === "GBP") return pence; const v = nice(pence / 100 * rate); return ZERO[cur] ? v : Math.round(v * 100); };
  const skus = [...new Set(items.map((i) => String(i.sku)))];
  const { data: products, error } = await supabase.from("bsos_products").select("sku,name,variant,price_pence,active,stock").in("sku", skus);
  if (error) return json({ error: "The catalogue is unavailable right now." }, 500);
  const by: Record<string, any> = Object.fromEntries((products || []).map((p: any) => [p.sku, p]));

  const p = new URLSearchParams();
  p.set("mode", "payment");
  p.set("success_url", base + "checkout/success.html?session_id={CHECKOUT_SESSION_ID}");
  p.set("cancel_url", base + "checkout/cancel.html");
  p.set("currency", cur.toLowerCase());
  p.set("shipping_address_collection[allowed_countries][0]", country);
  p.set("phone_number_collection[enabled]", "true");
  p.set("billing_address_collection", "auto");
  p.set("customer_creation", "always");
  p.set("allow_promotion_codes", "true");
  // delivery: the rate for the destination chosen on the basket page, standard and express
  const q = quote(country, items.map((i) => ({ sku: String(i.sku), qty: Math.max(1, Math.min(10, parseInt(i.qty) || 1)) })));
  const opts = [[q.standard, country === "GB" ? "Free tracked delivery" : "Tracked delivery", q.days], [q.express, country === "GB" ? "Next working day" : "Express, tracked", q.express_days]];
  opts.forEach(([amount, name, days], i) => {
    p.set(`shipping_options[${i}][shipping_rate_data][type]`, "fixed_amount");
    p.set(`shipping_options[${i}][shipping_rate_data][fixed_amount][amount]`, String(minor(Number(amount))));
    p.set(`shipping_options[${i}][shipping_rate_data][fixed_amount][currency]`, cur.toLowerCase());
    p.set(`shipping_options[${i}][shipping_rate_data][display_name]`, `${name} (${days})`);
  });
  p.set("custom_text[submit][message]", country === "GB"
    ? "Assembled to order in the UK and dispatched within three working days."
    : "Assembled to order in the UK and dispatched within three working days. Prices exclude any import duty or tax charged by your country; the courier collects these on delivery.");
  p.set("metadata[country]", country);
  p.set("metadata[ship_zone]", q.zone);
  p.set("metadata[currency]", cur); p.set("metadata[fx_per_gbp]", String(rate));
  let n = 0; const meta: string[] = []; let total = 0;
  for (const it of items) {
    const prod = by[String(it.sku)];
    const qty = Math.max(1, Math.min(10, parseInt(it.qty) || 1));
    if (!prod || !prod.active) return json({ error: `${it.sku} is not available.` }, 400);
    if ((prod.stock || 0) < qty) return json({ error: `${prod.name}${prod.variant ? " (" + prod.variant + ")" : ""} is not in stock yet. Join the list on its page and we will email you the day it is.` }, 409);
    p.set(`line_items[${n}][quantity]`, String(qty));
    p.set(`line_items[${n}][price_data][currency]`, cur.toLowerCase());
    p.set(`line_items[${n}][price_data][unit_amount]`, String(minor(prod.price_pence)));
    p.set(`line_items[${n}][price_data][product_data][name]`, `Blackout SOS ${prod.name}` + (prod.variant ? ` (${prod.variant})` : ""));
    p.set(`line_items[${n}][price_data][product_data][metadata][sku]`, prod.sku);
    meta.push(`${prod.sku}:${qty}`); total += minor(prod.price_pence) * qty; n++;
  }
  p.set("metadata[items]", meta.join(","));
  p.set("metadata[source]", "blackoutsos.com");
  const r = await fetch("https://api.stripe.com/v1/checkout/sessions", { method: "POST", headers: stripeHeaders(key), body: p });
  const s = await r.json();
  if (!r.ok) return json({ error: s?.error?.message || "Stripe could not start the checkout." }, 502);
  return json({ url: s.url, id: s.id, total_minor: total, currency: cur });
});

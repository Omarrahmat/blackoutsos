// Shared helpers for the Blackout SOS edge functions (copied into each function at deploy).
export const CORS = {
  "Access-Control-Allow-Origin": "*",
  "Access-Control-Allow-Headers": "authorization, x-client-info, apikey, content-type",
  "Access-Control-Allow-Methods": "POST, OPTIONS",
};
export const json = (body: unknown, status = 200) =>
  new Response(JSON.stringify(body), { status, headers: { ...CORS, "Content-Type": "application/json" } });

export function stripeHeaders(key: string) {
  return { Authorization: "Basic " + btoa(key + ":"), "Content-Type": "application/x-www-form-urlencoded" };
}

// Records a paid Stripe Checkout Session as an order, once. Returns the order id.
export async function recordSession(supabase: any, s: any): Promise<string> {
  const { data: existing } = await supabase.from("bsos_orders").select("id").eq("stripe_session_id", s.id).maybeSingle();
  if (existing) return existing.id;
  const items = String(s.metadata?.items || "").split(",").filter(Boolean).map((x: string) => {
    const [sku, q] = x.split(":"); return { sku, qty: Math.max(1, parseInt(q) || 1) };
  });
  const skus = items.map((i: any) => i.sku);
  const { data: products } = skus.length ? await supabase.from("bsos_products").select("sku,price_pence,stock").in("sku", skus) : { data: [] };
  const by: Record<string, any> = Object.fromEntries((products || []).map((p: any) => [p.sku, p]));
  const shipping = s.shipping_details || s.collected_information?.shipping_details || null;
  const pi = typeof s.payment_intent === "string" ? s.payment_intent : (s.payment_intent?.id ?? null);
  const { data: order, error } = await supabase.from("bsos_orders").insert({
    channel: "website",
    stripe_session_id: s.id,
    stripe_payment_intent: pi,
    email: s.customer_details?.email ?? s.customer_email ?? null,
    name: s.customer_details?.name ?? shipping?.name ?? null,
    phone: s.customer_details?.phone ?? null,
    shipping,
    total_pence: s.amount_total ?? 0,
    currency: s.currency ?? "gbp",
    status: "paid",
  }).select("id").single();
  if (error) {
    if (error.code === "23505") {
      const { data: again } = await supabase.from("bsos_orders").select("id").eq("stripe_session_id", s.id).single();
      return again.id;
    }
    throw error;
  }
  const rows = items.map((i: any) => ({ order_id: order.id, sku: i.sku, qty: i.qty, unit_pence: by[i.sku]?.price_pence ?? 0 }));
  if (rows.length) await supabase.from("bsos_order_items").insert(rows);
  for (const i of items) {
    if (!by[i.sku]) continue;
    await supabase.from("bsos_products").update({ stock: (by[i.sku].stock || 0) - i.qty }).eq("sku", i.sku);
    await supabase.from("bsos_stock_moves").insert({ sku: i.sku, delta: -i.qty, reason: "order", ref: order.id });
  }
  return order.id;
}

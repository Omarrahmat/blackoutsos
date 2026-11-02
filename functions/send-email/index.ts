// Outbound mail, called by the back office (admin JWT) or by scheduled jobs (x-fetch-key).
//   { kind: "waitlist", sku }                         -> "It's ready to order" to everyone waiting for that bag
//   { kind: "newsletter", subject, html, text?, country?, test_to? } -> the Blackout Brief / Be Ready alert to the list (or one test address)
//   { kind: "test", to }                               -> a plain test email
import "jsr:@supabase/functions-js/edge-runtime.d.ts";
import { createClient } from "jsr:@supabase/supabase-js@2";
import { CORS, json } from "./_shared.ts";
import { SITE, h, layout, send, unsubUrl } from "./_email.ts";

const BAGS: Record<string, { name: string; url: string; price: string }> = {
  operator: { name: "Operator", url: "bags/operator.html", price: "£199" }, recruit: { name: "Recruit", url: "bags/recruit.html", price: "£89" },
  "cub-1": { name: "Cub", url: "bags/cub.html", price: "£149" }, "cub-2": { name: "Cub", url: "bags/cub.html", price: "£149" }, "cub-3": { name: "Cub", url: "bags/cub.html", price: "£149" },
  unit: { name: "Unit", url: "bags/unit.html", price: "£449" }, "scout-dog": { name: "Scout", url: "bags/scout.html", price: "£99" }, "scout-cat": { name: "Scout", url: "bags/scout.html", price: "£99" },
};

Deno.serve(async (req: Request) => {
  if (req.method === "OPTIONS") return new Response("ok", { headers: CORS });
  if (req.method !== "POST") return json({ error: "POST only" }, 405);
  const supabase = createClient(Deno.env.get("SUPABASE_URL")!, Deno.env.get("SUPABASE_SERVICE_ROLE_KEY")!);
  const { data: setting } = await supabase.from("bsos_settings").select("value").eq("key", "alerts_fetch_key").maybeSingle();
  const secret = setting?.value || "";
  // who is calling: a scheduled job with the key, or a signed-in admin
  let allowed = !!secret && req.headers.get("x-fetch-key") === secret;
  if (!allowed) {
    const auth = req.headers.get("authorization") || "";
    if (auth.startsWith("Bearer ")) {
      const { data: u } = await supabase.auth.getUser(auth.slice(7));
      if (u?.user?.email) { const { data: adm } = await supabase.from("bsos_admins").select("email").eq("email", u.user.email).maybeSingle(); allowed = !!adm; }
    }
  }
  if (!allowed) return json({ error: "Not allowed" }, 403);
  let body: any; try { body = await req.json(); } catch { return json({ error: "Bad request" }, 400); }
  const results = { sent: 0, failed: 0, skipped: 0, recipients: 0 };
  const tally = (s: string) => { (results as any)[s]++; };

  if (body.kind === "test") {
    const to = String(body.to || ""); if (!/^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(to)) return json({ error: "Bad address" }, 400);
    const unsub = await unsubUrl(to, secret);
    tally(await send(supabase, { to, kind: "test", subject: "Blackout SOS — test email", unsub, html: layout("Test", h.h1("Email is working.") + h.p("This is a test from the Blackout SOS back office."), unsub), text: "This is a test from the Blackout SOS back office." }));
    results.recipients = 1; return json({ ok: true, ...results });
  }

  if (body.kind === "waitlist") {
    const sku = String(body.sku || ""); const bag = BAGS[sku]; if (!bag) return json({ error: "Unknown bag" }, 400);
    const { data: prod } = await supabase.from("bsos_products").select("stock,active").eq("sku", sku).maybeSingle();
    if (!prod || !prod.active || (prod.stock || 0) < 1) return json({ error: `${bag.name} is not in stock yet — set the stock first.` }, 409);
    const { data: subs } = await supabase.from("bsos_subscribers").select("email").is("unsubscribed_at", null).ilike("bag", bag.name + "%");
    const { data: done } = await supabase.from("bsos_emails").select("to_email").eq("kind", "waitlist").eq("ref", sku).eq("status", "sent");
    const already = new Set((done || []).map((d: any) => d.to_email));
    const list = (subs || []).map((s: any) => s.email).filter((e: string) => !already.has(e));
    results.recipients = list.length;
    for (const to of list) {
      const unsub = await unsubUrl(to, secret);
      const html = layout(`The ${bag.name} is ready to order`, h.h1(`The ${bag.name} is ready to order.`) + h.p(`You asked us to tell you the day the ${h.esc(bag.name)} was in stock. That's today. The first run is small, and the people on this list hear first.`) + h.btn(`${SITE}/${bag.url}`, `Order the ${bag.name} · ${bag.price}`) + h.small("Assembled in the UK, free UK delivery, dispatched within three working days. Worldwide delivery at checkout."), unsub, `The ${bag.name} is in stock. You're first to know.`);
      tally(await send(supabase, { to, kind: "waitlist", ref: sku, subject: `The ${bag.name} is ready to order`, html, text: `The ${bag.name} is in stock: ${SITE}/${bag.url}`, unsub }));
    }
    return json({ ok: true, ...results });
  }

  if (body.kind === "newsletter") {
    const subject = String(body.subject || "").slice(0, 150); const inner = String(body.html || ""); const text = body.text ? String(body.text) : undefined;
    if (!subject || !inner) return json({ error: "subject and html are required" }, 400);
    let list: string[];
    if (body.test_to) list = [String(body.test_to)];
    else {
      let q = supabase.from("bsos_subscribers").select("email").is("unsubscribed_at", null);
      if (body.country) q = q.eq("country", String(body.country).toUpperCase());
      const { data: subs } = await q; list = (subs || []).map((s: any) => s.email);
    }
    const ref = String(body.ref || `nl-${new Date().toISOString().slice(0, 10)}-${subject.toLowerCase().replace(/[^a-z0-9]+/g, "-").slice(0, 40)}`);
    const { data: done } = await supabase.from("bsos_emails").select("to_email").eq("kind", "newsletter").eq("ref", ref).eq("status", "sent");
    const already = new Set((done || []).map((d: any) => d.to_email));
    list = list.filter((e) => body.test_to || !already.has(e));
    results.recipients = list.length;
    for (const to of list) {
      const unsub = await unsubUrl(to, secret);
      tally(await send(supabase, { to, kind: "newsletter", ref, subject, html: layout(subject, inner, unsub), text, unsub }));
    }
    return json({ ok: true, ref, ...results });
  }
  return json({ error: "Unknown kind" }, 400);
});

// POST contact, organisation and complaint forms -> bsos_enquiries.
import "jsr:@supabase/functions-js/edge-runtime.d.ts";
import { createClient } from "jsr:@supabase/supabase-js@2";
import { CORS, json } from "../_shared.ts";

Deno.serve(async (req: Request) => {
  if (req.method === "OPTIONS") return new Response("ok", { headers: CORS });
  if (req.method !== "POST") return json({ error: "POST only" }, 405);
  let body: any; try { body = await req.json(); } catch { return json({ error: "Bad request" }, 400); }
  const kind = ["contact", "organisation", "complaint"].includes(body.kind) ? body.kind : "contact";
  const email = String(body.email || "").trim().toLowerCase();
  if (!/^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(email)) return json({ error: "Please give an email address we can reply to." }, 400);
  const clip = (v: unknown, n: number) => (v == null || v === "" ? null : String(v).slice(0, n));
  const subject = clip(body.subject, 60);
  const row = {
    kind: subject === "A complaint" ? "complaint" : kind,
    name: clip(body.name, 120), org: clip(body.org, 160), email, phone: clip(body.phone, 40),
    subject, segment: clip(body.segment, 60), bags: clip(body.bags, 200), order_ref: clip(body.order, 40),
    message: clip(body.message, 4000), page: clip(body.page, 200),
  };
  if (!row.message && kind === "contact") return json({ error: "Please write a message." }, 400);
  const supabase = createClient(Deno.env.get("SUPABASE_URL")!, Deno.env.get("SUPABASE_SERVICE_ROLE_KEY")!);
  const { error } = await supabase.from("bsos_enquiries").insert(row);
  if (error) return json({ error: "We couldn't save that. Please email hello@blackoutsos.com." }, 500);
  return json({ ok: true });
});

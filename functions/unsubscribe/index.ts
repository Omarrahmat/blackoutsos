// GET/POST ?e=email&t=token -> marks the subscriber unsubscribed (token from the email's unsubscribe link).
import "jsr:@supabase/functions-js/edge-runtime.d.ts";
import { createClient } from "jsr:@supabase/supabase-js@2";
import { CORS, json } from "./_shared.ts";
import { unsubToken } from "./_email.ts";

Deno.serve(async (req: Request) => {
  if (req.method === "OPTIONS") return new Response("ok", { headers: { ...CORS, "Access-Control-Allow-Methods": "GET, POST, OPTIONS" } });
  const u = new URL(req.url);
  let email = u.searchParams.get("e") || ""; let token = u.searchParams.get("t") || "";
  if (req.method === "POST" && !email) { try { const b = await req.json(); email = b.e || b.email || ""; token = b.t || b.token || ""; } catch { /* form post from List-Unsubscribe has no body we need */ } }
  email = email.trim().toLowerCase();
  const supabase = createClient(Deno.env.get("SUPABASE_URL")!, Deno.env.get("SUPABASE_SERVICE_ROLE_KEY")!);
  const { data: setting } = await supabase.from("bsos_settings").select("value").eq("key", "alerts_fetch_key").maybeSingle();
  if (!email || !setting?.value || token !== (await unsubToken(email, setting.value))) return json({ error: "That link isn't valid. Email hello@blackoutsos.com and we will remove you by hand." }, 400);
  await supabase.from("bsos_subscribers").update({ unsubscribed_at: new Date().toISOString(), alerts_opt_in: false }).eq("email", email);
  return json({ ok: true });
});

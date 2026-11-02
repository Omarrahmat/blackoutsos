// Email sending for Blackout SOS edge functions (copied into each function at deploy).
// Provider: AgentMail, inbox hello@blackoutsos.com.
// Without a key nothing is sent: every attempt is logged in bsos_emails as "skipped" so the back office can show it.
export const SITE = "https://blackoutsos.com";

export async function sha(s: string): Promise<string> {
  const b = await crypto.subtle.digest("SHA-256", new TextEncoder().encode(s));
  return Array.from(new Uint8Array(b)).map((x) => x.toString(16).padStart(2, "0")).join("");
}
export async function unsubToken(email: string, secret: string) { return (await sha(`unsub:${email.toLowerCase()}:${secret}`)).slice(0, 24); }
export async function unsubUrl(email: string, secret: string) { return `${SITE}/unsubscribe.html?e=${encodeURIComponent(email)}&t=${await unsubToken(email, secret)}`; }

const esc = (s: string) => String(s ?? "").replace(/[&<>"]/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]!));

export function layout(title: string, bodyHtml: string, unsub: string, preheader = ""): string {
  return `<div style="font-family:Helvetica,Arial,sans-serif;font-size:16px;line-height:1.55;color:#222;max-width:560px">
<span style="display:none;max-height:0;overflow:hidden">${esc(preheader)}</span>
${bodyHtml}
<p style="margin:22px 0 0;color:#888;font-size:12px;line-height:1.6">You are receiving this because you asked for it on blackoutsos.com. <a href="${unsub}" style="color:#888">Unsubscribe</a> in one click.</p></div>`;
}
export const h = { p: (s: string) => `<p style="margin:0 0 14px">${s}</p>`, h1: (s: string) => `<h1 style="margin:0 0 14px;font-size:22px;line-height:1.25">${esc(s)}</h1>`,
  btn: (href: string, s: string) => `<p style="margin:22px 0 6px"><a href="${href}" style="display:inline-block;background:#0a0a0a;color:#ffffff;text-decoration:none;font-weight:600;padding:13px 22px;border-radius:999px">${esc(s)}</a></p>`,
  small: (s: string) => `<p style="margin:14px 0 0;color:#666;font-size:13px">${s}</p>`, esc };

export type Mail = { to: string; subject: string; html: string; text?: string; kind: string; ref?: string | null; unsub: string };

// Sends one email from hello@blackoutsos.com through AgentMail (key in bsos_settings) and logs it.
// AgentMail adds the team signature, so templates end with the message itself.
let AM_KEY: string | null | undefined;
export async function send(supabase: any, m: Mail): Promise<"sent" | "failed" | "skipped"> {
  if (AM_KEY === undefined) { const { data } = await supabase.from("bsos_settings").select("value").eq("key", "agentmail_api_key").maybeSingle(); AM_KEY = data?.value || null; }
  const inbox = Deno.env.get("EMAIL_INBOX") || "hello@blackoutsos.com";
  const log = { kind: m.kind, to_email: m.to, subject: m.subject, ref: m.ref ?? null };
  if (!AM_KEY) { await supabase.from("bsos_emails").insert({ ...log, status: "skipped", error: "AgentMail key not set" }); return "skipped"; }
  try {
    const r = await fetch(`https://api.agentmail.to/v0/inboxes/${encodeURIComponent(inbox)}/messages/send`, { method: "POST", headers: { Authorization: `Bearer ${AM_KEY}`, "Content-Type": "application/json" },
      body: JSON.stringify({ to: [m.to], subject: m.subject, html: m.html, text: m.text || m.subject, labels: ["automated", m.kind], headers: { "List-Unsubscribe": `<${m.unsub}>`, "List-Unsubscribe-Post": "List-Unsubscribe=One-Click" } }) });
    const j = await r.json().catch(() => ({}));
    if (!r.ok) { await supabase.from("bsos_emails").insert({ ...log, status: "failed", error: String(j?.message || j?.error || r.status).slice(0, 300) }); return "failed"; }
    await supabase.from("bsos_emails").insert({ ...log, status: "sent", provider_id: j?.messageId || j?.message_id || null }); return "sent";
  } catch (e) { await supabase.from("bsos_emails").insert({ ...log, status: "failed", error: String(e).slice(0, 300) }); return "failed"; }
}

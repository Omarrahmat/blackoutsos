// Email sending for Blackout SOS edge functions (copied into each function at deploy).
// Provider: Resend (https://resend.com). Set RESEND_API_KEY and, once the domain is verified, EMAIL_FROM.
// Without a key nothing is sent: every attempt is logged in bsos_emails as "skipped" so the back office can show it.
export const SITE = "https://blackoutsos.com";
const FROM_DEFAULT = "Blackout SOS <alerts@blackoutsos.com>";

export async function sha(s: string): Promise<string> {
  const b = await crypto.subtle.digest("SHA-256", new TextEncoder().encode(s));
  return Array.from(new Uint8Array(b)).map((x) => x.toString(16).padStart(2, "0")).join("");
}
export async function unsubToken(email: string, secret: string) { return (await sha(`unsub:${email.toLowerCase()}:${secret}`)).slice(0, 24); }
export async function unsubUrl(email: string, secret: string) { return `${SITE}/unsubscribe.html?e=${encodeURIComponent(email)}&t=${await unsubToken(email, secret)}`; }

const esc = (s: string) => String(s ?? "").replace(/[&<>"]/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]!));

export function layout(title: string, bodyHtml: string, unsub: string, preheader = ""): string {
  return `<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width"><title>${esc(title)}</title></head>
<body style="margin:0;background:#0a0a0a;color:#ededed;font-family:Inter,Helvetica,Arial,sans-serif;font-size:16px;line-height:1.55">
<span style="display:none;max-height:0;overflow:hidden;color:#0a0a0a">${esc(preheader)}</span>
<table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="background:#0a0a0a"><tr><td align="center" style="padding:28px 16px">
<table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="max-width:560px">
<tr><td style="padding:0 0 22px;font-weight:800;letter-spacing:2px;font-size:20px;color:#fff">BLACKOUT SOS <span style="color:#9a9a9a;font-weight:400;letter-spacing:4px;font-size:12px">&nbsp;··· ––– ···</span></td></tr>
<tr><td style="background:#111;border:1px solid #1e1e1e;border-radius:16px;padding:28px">${bodyHtml}</td></tr>
<tr><td style="padding:22px 4px 0;color:#6f6f6f;font-size:12px;line-height:1.6">Blackout SOS · London · <a href="${SITE}" style="color:#9a9a9a">blackoutsos.com</a><br>
You are receiving this because you asked for it on blackoutsos.com. <a href="${unsub}" style="color:#9a9a9a">Unsubscribe</a> in one click. In an emergency follow the instructions of your local authorities.</td></tr>
</table></td></tr></table></body></html>`;
}
export const h = { p: (s: string) => `<p style="margin:0 0 14px;color:#d6d6d6">${s}</p>`, h1: (s: string) => `<h1 style="margin:0 0 14px;font-size:24px;line-height:1.2;color:#fff">${esc(s)}</h1>`,
  btn: (href: string, s: string) => `<p style="margin:22px 0 6px"><a href="${href}" style="display:inline-block;background:#ededed;color:#0a0a0a;text-decoration:none;font-weight:600;padding:14px 22px;border-radius:999px">${esc(s)}</a></p>`,
  small: (s: string) => `<p style="margin:14px 0 0;color:#9a9a9a;font-size:13px">${s}</p>`, esc };

export type Mail = { to: string; subject: string; html: string; text?: string; kind: string; ref?: string | null; unsub: string };

// Sends one email through Resend and logs it. Returns the log status.
export async function send(supabase: any, m: Mail): Promise<"sent" | "failed" | "skipped"> {
  const key = Deno.env.get("RESEND_API_KEY");
  const from = Deno.env.get("EMAIL_FROM") || FROM_DEFAULT;
  const log = { kind: m.kind, to_email: m.to, subject: m.subject, ref: m.ref ?? null };
  if (!key) { await supabase.from("bsos_emails").insert({ ...log, status: "skipped", error: "RESEND_API_KEY not set" }); return "skipped"; }
  try {
    const r = await fetch("https://api.resend.com/emails", { method: "POST", headers: { Authorization: `Bearer ${key}`, "Content-Type": "application/json" },
      body: JSON.stringify({ from, to: [m.to], subject: m.subject, html: m.html, text: m.text, headers: { "List-Unsubscribe": `<${m.unsub}>`, "List-Unsubscribe-Post": "List-Unsubscribe=One-Click" } }) });
    const j = await r.json().catch(() => ({}));
    if (!r.ok) { await supabase.from("bsos_emails").insert({ ...log, status: "failed", error: String(j?.message || r.status).slice(0, 300) }); return "failed"; }
    await supabase.from("bsos_emails").insert({ ...log, status: "sent", provider_id: j?.id ?? null }); return "sent";
  } catch (e) { await supabase.from("bsos_emails").insert({ ...log, status: "failed", error: String(e).slice(0, 300) }); return "failed"; }
}

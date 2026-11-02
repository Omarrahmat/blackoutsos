# Blackout SOS — blackoutsos.com

72-hour go bags, assembled in the UK. One bag per person, one colour per bag.

## What this is
- A hand-built static site (plain HTML, CSS and JS) hosted on GitHub Pages at the custom domain **blackoutsos.com**.
- The shop: basket in the browser, payment on Stripe Checkout, orders recorded in Supabase.
- The back office at `/admin/` (sign in with the admin email and password).

## Layout
- `index.html`, `bags/`, `guides/`, `refills.html`, `organisations.html`, `about.html`, `delivery-returns.html`, `contact.html`, `privacy.html`, `terms.html`, `basket.html`, `checkout/` — generated pages.
- `assets/site.css`, `assets/site.js` — the one stylesheet and the basket/checkout/forms script.
- `admin/index.html` — the back office (reads Supabase directly, admin-only through row-level security).
- `tools/build.py`, `tools/content_bags.py`, `tools/content_guides.py` — the generator and the content. Edit the content files, run `python3 tools/build.py`, commit.
- `functions/` — the Supabase Edge Functions as deployed: `checkout`, `confirm`, `stripe-webhook`, `subscribe`, `enquiry`.

## Switching the shop on
1. Supabase → Edge Functions → Secrets: add `STRIPE_SECRET_KEY` (a restricted key with Checkout Sessions write and Events read is enough).
2. Stripe → Developers → Webhooks: add `https://vbgustjtxjmjlgukzcfa.supabase.co/functions/v1/stripe-webhook` for the event `checkout.session.completed`. (Orders are also recorded from the success page, so the webhook is a safety net.)
3. Stripe → Settings → Emails: turn on customer receipts.
4. Put stock in: `/admin/` → Stock → adjust.

## Domain
GitHub Pages → Settings → Pages → Custom domain `blackoutsos.com` (the `CNAME` file in this repo). At the registrar: `A` records for `blackoutsos.com` to GitHub Pages' four IPs and a `CNAME` for `www` to `omarrahmat.github.io`. Enforce HTTPS once the certificate is issued. Point `blackoutsos.co.uk` at the same.

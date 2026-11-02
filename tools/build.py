#!/usr/bin/env python3
"""Builds blackoutsos.com as plain HTML. Run: python3 tools/build.py
Every page is written from the content modules so the header, footer and links stay consistent."""
import os, json, datetime, html as H
from content_bags import BAGS, ORDER
from content_guides import GUIDES, CATS
from hero import hero_html, HERO_CSS

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = "https://blackoutsos.com"
YEAR = datetime.date.today().year
UPDATED = datetime.date.today().strftime("%B %Y")

FAVICON = "data:image/svg+xml," + H.escape("<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 64 64'><rect width='64' height='64' rx='14' fill='#0a0a0a'/><g fill='#ededed'><rect x='10' y='29' width='5' height='6' rx='1'/><rect x='17' y='29' width='5' height='6' rx='1'/><rect x='24' y='29' width='5' height='6' rx='1'/><rect x='33' y='29' width='9' height='6' rx='1'/><rect x='44' y='29' width='9' height='6' rx='1'/></g></svg>", quote=True)

def gbp(p): return "£" + (f"{p/100:.2f}" if p % 100 else f"{p//100}")

def morse():
    d = '<i></i>' * 3; l = '<i class="l"></i>' * 3
    return f'<span class="morse" aria-hidden="true">{d}<b></b>{l}<b></b>{d}</span>'

def head(title, desc, path, r, extra=""):
    canonical = f"{SITE}/{path}".replace("/index.html", "/")
    return f"""<!doctype html>
<html lang="en-GB">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{H.escape(title)}</title>
<meta name="description" content="{H.escape(desc)}">
<link rel="canonical" href="{canonical}">
<meta property="og:title" content="{H.escape(title)}">
<meta property="og:description" content="{H.escape(desc)}">
<meta property="og:type" content="website">
<meta property="og:url" content="{canonical}">
<meta property="og:site_name" content="Blackout SOS">
<meta name="theme-color" content="#0a0a0a">
<link rel="icon" href="{FAVICON}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Barlow+Condensed:wght@500;700&family=Inter:wght@400;500;600&display=swap">
<link rel="stylesheet" href="{r}assets/site.css">
{extra}
</head>
<body>
"""

def nav(r):
    return f"""<a class="banner" href="{r}guides/the-72-hour-list-explained.html">Be Ready: the Government advises every household to hold three days of supplies. Read the 72-hour checklist →</a>
<header class="nav">
<a class="brand" href="{r}index.html" aria-label="Blackout SOS home"><span class="word">Blackout SOS</span>{morse()}</a>
<nav class="nav-links" aria-label="Main">
<a href="{r}bags/index.html">Bags</a>
<a href="{r}guides/index.html">Guides</a>
<a href="{r}refills.html">Refills</a>
<a href="{r}organisations.html">For organisations</a>
<a href="{r}about.html">Our story</a>
</nav>
<div class="nav-right"><a class="basket-link" href="{r}basket.html" data-basket-count>Basket · 0</a></div>
</header>
<main>
"""

def footer(r):
    return f"""</main>
<footer>
<div class="wrap">
<div class="foot">
<div class="stack" style="max-width:320px"><span class="display" style="font-size:26px;letter-spacing:2px">Blackout SOS</span><p class="p small">Designed in London. Assembled in the UK. Three dots, three dashes, three days.</p></div>
<div class="col"><span>Shop</span><a href="{r}bags/operator.html">Operator</a><a href="{r}bags/recruit.html">Recruit</a><a href="{r}bags/cub.html">Cub</a><a href="{r}bags/unit.html">Unit</a><a href="{r}bags/scout.html">Scout</a><a href="{r}refills.html">Refills</a></div>
<div class="col"><span>Learn</span><a href="{r}guides/index.html">Guides</a><a href="{r}guides/the-72-hour-list-explained.html">72-hour checklist</a><a href="{r}bags/operator.html#inside">What's in the bag</a><a href="{r}refills.html">Rotation dates</a></div>
<div class="col"><span>Company</span><a href="{r}about.html">Our story</a><a href="{r}organisations.html">For organisations</a><a href="{r}delivery-returns.html">Delivery and returns</a><a href="{r}contact.html">Contact</a><a href="{r}privacy.html">Privacy</a><a href="{r}terms.html">Terms</a></div>
</div>
<p class="legal">© {YEAR} Blackout SOS. Blackout SOS is a trading name of Urban Carers Ltd, company number 15419139, registered in England and Wales. blackoutsos.com · In an emergency call 999. This site gives general preparedness advice, not emergency instructions from the authorities.</p>
</div>
</footer>
<script src="{r}assets/site.js"></script>
</body>
</html>
"""

def write(path, html_text):
    full = os.path.join(ROOT, path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, "w") as f: f.write(html_text)

def page(path, title, desc, body, extra_head=""):
    depth = path.count("/")
    r = "../" * depth
    write(path, head(title, desc, path, r, extra_head) + nav(r) + body + footer(r))

# ---------- SVG bag art ----------
def svg_operator(c, h=None, label="Operator go bag, front view"):
    return f"""<svg viewBox="0 0 400 520" role="img" aria-label="{label}"{' style="height:'+h+'"' if h else ''}><path d="M150 66 C150 34 250 34 250 66" fill="none" stroke="#1d1d1d" stroke-width="12" stroke-linecap="round"/><rect x="60" y="60" width="280" height="430" rx="56" fill="#161616" stroke="#262626" stroke-width="2"/><path d="M70 140 Q70 76 200 72 Q330 76 330 140" fill="none" stroke="#2b2b2b" stroke-width="4" stroke-dasharray="2 3"/><rect x="156" y="96" width="88" height="32" rx="7" fill="#0f0f0f" stroke="#2a2a2a" stroke-width="1.5"/><rect x="163" y="103" width="74" height="18" rx="3" fill="#1d1d1d" stroke="#333"/><rect x="296" y="110" width="6" height="24" rx="2" fill="{c}"/><rect x="62" y="204" width="36" height="176" rx="15" fill="#121212" stroke="#272727" stroke-width="2"/><rect x="72" y="178" width="16" height="30" rx="5" fill="#1b1b1b" stroke="#2a2a2a"/><g fill="#0b0b0b"><rect x="312" y="200" width="14" height="6" rx="2"/><rect x="312" y="210" width="14" height="6" rx="2"/><rect x="312" y="220" width="14" height="6" rx="2"/><rect x="312" y="236" width="14" height="16" rx="2"/><rect x="312" y="256" width="14" height="16" rx="2"/><rect x="312" y="276" width="14" height="16" rx="2"/><rect x="312" y="302" width="14" height="6" rx="2"/><rect x="312" y="312" width="14" height="6" rx="2"/><rect x="312" y="322" width="14" height="6" rx="2"/></g><rect x="100" y="180" width="200" height="250" rx="30" fill="#131313" stroke="#232323" stroke-width="2"/><rect x="150" y="224" width="100" height="56" rx="6" fill="#1a1a1a" stroke="#222"/><text x="200" y="350" text-anchor="middle" fill="#2e2e2e" font-size="16" letter-spacing="4" font-family="Barlow Condensed, sans-serif" font-weight="700">BLACKOUT SOS</text><g fill="#2e2e2e"><rect x="151" y="359" width="4" height="4" rx="1"/><rect x="158" y="359" width="4" height="4" rx="1"/><rect x="165" y="359" width="4" height="4" rx="1"/><rect x="179" y="359" width="12" height="4" rx="1"/><rect x="194" y="359" width="12" height="4" rx="1"/><rect x="209" y="359" width="12" height="4" rx="1"/><rect x="231" y="359" width="4" height="4" rx="1"/><rect x="238" y="359" width="4" height="4" rx="1"/><rect x="245" y="359" width="4" height="4" rx="1"/></g><rect x="336" y="172" width="10" height="30" rx="2" fill="{c}"/><path d="M92 472 Q200 486 308 472" fill="none" stroke="#222" stroke-width="2"/></svg>"""

def svg_small(c, h=None, ring=False, label="Go bag"):
    extra = '<circle cx="70" cy="150" r="12" fill="none" stroke="#3a3a3a" stroke-width="5"/>' if ring else ''
    return f"""<svg viewBox="0 0 400 520" role="img" aria-label="{label}"{' style="height:'+h+'"' if h else ''}><path d="M150 66 C150 34 250 34 250 66" fill="none" stroke="#1d1d1d" stroke-width="12" stroke-linecap="round"/><rect x="60" y="60" width="280" height="430" rx="56" fill="#161616" stroke="#2a2a2a" stroke-width="2"/><rect x="156" y="96" width="88" height="32" rx="7" fill="#0f0f0f" stroke="#2a2a2a" stroke-width="1.5"/><rect x="100" y="180" width="200" height="250" rx="30" fill="#131313" stroke="#262626" stroke-width="2"/><rect x="62" y="204" width="36" height="160" rx="15" fill="#121212" stroke="#272727" stroke-width="2"/>{extra}<text x="200" y="350" text-anchor="middle" fill="#2e2e2e" font-size="16" letter-spacing="4" font-family="Barlow Condensed, sans-serif" font-weight="700">BLACKOUT SOS</text><rect x="296" y="110" width="6" height="24" rx="2" fill="{c}"/><rect x="336" y="172" width="12" height="34" rx="2" fill="{c}"/></svg>"""

def svg_cub(c, h=None, label="Cub baby go bag"):
    return f"""<svg viewBox="0 0 400 520" role="img" aria-label="{label}"{' style="height:'+h+'"' if h else ''}><path d="M150 66 C150 34 250 34 250 66" fill="none" stroke="#1d1d1d" stroke-width="12" stroke-linecap="round"/><rect x="60" y="60" width="280" height="410" rx="70" fill="#161616" stroke="#2a2a2a" stroke-width="2"/><rect x="156" y="96" width="88" height="32" rx="7" fill="#0f0f0f" stroke="#2a2a2a" stroke-width="1.5"/><rect x="104" y="180" width="192" height="220" rx="60" fill="#131313" stroke="#262626" stroke-width="2"/><rect x="90" y="452" width="220" height="30" rx="15" fill="#141414" stroke="#2a2a2a" stroke-width="2"/><text x="200" y="330" text-anchor="middle" fill="#2e2e2e" font-size="16" letter-spacing="4" font-family="Barlow Condensed, sans-serif" font-weight="700">BLACKOUT SOS</text><rect x="296" y="110" width="6" height="24" rx="2" fill="{c}"/><rect x="336" y="172" width="12" height="34" rx="2" fill="{c}"/><g fill="{c}"><circle cx="342" cy="216" r="2.5"/><circle cx="342" cy="224" r="2.5"/></g></svg>"""

def svg_unit(c, h=None, label="Unit family duffel"):
    return f"""<svg viewBox="0 0 400 260" role="img" aria-label="{label}"{' style="height:'+h+'"' if h else ''}><rect x="20" y="64" width="360" height="180" rx="70" fill="#161616" stroke="#2a2a2a" stroke-width="2"/><rect x="120" y="120" width="160" height="96" rx="20" fill="#131313" stroke="#262626" stroke-width="2"/><rect x="96" y="64" width="12" height="180" fill="#0e0e0e"/><rect x="292" y="64" width="12" height="180" fill="#0e0e0e"/><path d="M150 64 C150 30 250 30 250 64" fill="none" stroke="#1d1d1d" stroke-width="12" stroke-linecap="round"/><text x="200" y="176" text-anchor="middle" fill="#2e2e2e" font-size="14" letter-spacing="4" font-family="Barlow Condensed, sans-serif" font-weight="700">BLACKOUT SOS</text><rect x="374" y="130" width="12" height="30" rx="2" fill="{c}"/></svg>"""

def art(slug, h=None):
    b = BAGS[slug]; c = b["colour"]; lab = f"{b['name']} go bag"
    if slug == "operator": return svg_operator(c, h, lab + ", front view")
    if slug == "cub": return svg_cub(c, h, lab)
    if slug == "unit": return svg_unit(c, h, lab)
    return svg_small(c, h, ring=(slug == "scout"), label=lab)

# ---------- pieces ----------
def bag_card(slug, r):
    b = BAGS[slug]
    heights = {"operator": "200px", "recruit": "150px", "cub": "170px", "unit": "130px", "scout": "150px"}
    if b.get("variants"):
        cta = f'<a class="pill sm solid" href="{r}bags/{slug}.html" style="flex:1 1 auto">Choose {"stage" if slug=="cub" else "dog or cat"}</a>'
    else:
        cta = f'<button type="button" class="pill sm solid" data-add="{b["sku"]}" style="flex:1 1 auto">Add to basket</button>'
    return f"""<div class="card" style="flex:1 1 260px;padding:24px">
<a href="{r}bags/{slug}.html" style="display:flex;flex-direction:column;gap:18px">
<div style="height:220px;display:flex;align-items:flex-end;justify-content:center">{art(slug, heights[slug])}</div>
<div style="display:flex;justify-content:space-between;align-items:baseline"><span class="display" style="font-size:30px">{b['name']}</span><span class="tag" style="background:{b['colour']}"></span></div>
<p class="p small">{b['card']}</p>
</a>
<div style="display:flex;justify-content:space-between;align-items:center;gap:12px;margin-top:auto"><span style="font-size:20px;font-weight:600">{gbp(b['price'])}</span>{cta}</div>
<a href="{r}bags/{slug}.html" class="muted small" style="align-self:flex-start;border-bottom:1px solid var(--line3)">What's inside →</a>
</div>"""

def subscribe_form(r, source="site"):
    return f"""<form class="form-row" data-api="/subscribe" style="flex:1 1 420px">
<input type="hidden" name="source" value="{source}">
<label class="sr" for="email-{source}">Email address</label>
<input id="email-{source}" name="email" type="email" required placeholder="you@example.com" style="flex:1 1 240px">
<button type="submit" class="pill solid">Sign up</button>
<p class="p small ok" data-done hidden style="flex:1 1 100%">You're on the list. One short message when it matters, nothing else.</p>
</form>"""

# ---------- HOME ----------
def home():
    r = ""
    cards = "".join(bag_card(s, r) for s in ORDER)
    pouches = [("#5c6a3a", "Olive · water and food", "3 × 500 ml water pouches<br>Purification tablets, 50<br>750 ml bottle, side pocket<br>2 × 2,325 kcal rations<br>Comfort pack<br>Spork"),
               ("#6b6b6b", "Grey · shelter and warmth", "Reusable bivvy bag<br>2 foil blankets<br>Hooded poncho<br>4 hand warmers<br>Beanie and gloves<br>Socks"),
               ("#2f7d4a", "Green · first aid", "BS 8599-1 first aid kit<br>Trauma dressing<br>Your medication pouch<br>2 FFP2 masks<br>Nitrile gloves"),
               ("#2a2a2a", "Black · hygiene and tools", "Wipes, sanitiser, toilet roll<br>Toothbrush, pads, bags<br>UK-legal multi-tool<br>Tape, paracord, cable ties<br>Ferro rod, pen, notepad<br>Document pouch and map"),
               ("#ededed", "Lid · light, power, signal", "Head torch, lithium batteries<br>Wind-up radio<br>10,000 mAh power bank<br>Whistle, on the strap too<br>2 glow sticks<br>Contents and first-hour cards")]
    pouch_html = "".join(f'<div class="card" style="flex:1 1 240px;padding:24px;gap:14px"><div style="display:flex;align-items:center;gap:10px"><span class="tag" style="width:14px;height:14px;background:{c};{"border:1px solid #3a3a3a" if c=="#2a2a2a" else ""}"></span><span class="eyebrow" style="letter-spacing:2px">{t}</span></div><p class="items" style="font-size:15px">{i}</p></div>' for c, t, i in pouches)
    chips = [("flooding-before-during-after", "Flooding"), ("storms-and-high-wind", "Storms and high wind"), ("cyber-outage-cards-cash-and-comms", "Cyber outage: cards, cash, comms"), ("water-treating-storing-rationing", "Water: treating, storing, rationing"), ("teaching-your-child-the-bag", "Teaching your child the bag"), ("pets-in-an-emergency", "Pets"), ("medication-and-medical-devices", "Medication and medical devices"), ("the-family-meeting-point", "The family meeting point")]
    chips_html = "".join(f'<a class="chip" href="guides/{s}.html">{t}</a>' for s, t in chips)
    schema = json.dumps({"@context": "https://schema.org", "@type": "Organization", "name": "Blackout SOS", "url": SITE, "legalName": "Urban Carers Ltd", "description": "72-hour go bags assembled in the UK. One bag per person, one colour per bag.", "contactPoint": {"@type": "ContactPoint", "email": "hello@blackoutsos.com", "contactType": "customer service", "areaServed": "GB"}})
    body = f"""
{hero_html(r, art, BAGS, gbp)}
<section class="strip"><span>Assembled in the UK</span><span>Waterproof TPU Cordura</span><span>15-year rations</span><span>Vegan · made without nuts</span><span>One tag per person</span><span>Refills when it's time</span></section>
<section class="section"><div class="wrap stack" style="gap:40px">
<div style="display:flex;flex-wrap:wrap;justify-content:space-between;align-items:flex-end;gap:16px">
<div class="stack" style="gap:10px"><p class="eyebrow">Shop the range</p><h2 class="h2">One bag per person. One colour per bag.</h2></div>
<p class="p" style="max-width:420px">Blue for adults, red for children, yellow for the baby, green for the family duffel, orange for the pet. In the dark, at the door, everyone grabs the right one.</p>
</div>
<div class="grid">{cards}</div>
</div></section>
<section class="section band"><div class="wrap stack" style="gap:56px">
<div style="display:flex;flex-wrap:wrap;gap:40px;align-items:flex-end;justify-content:space-between">
<h2 class="h2" style="max-width:720px">Built for the dark, not for the shelf.</h2>
<p class="p" style="max-width:460px">Most kits are a rucksack with things thrown in. Ours is a system: every item has a pouch, every pouch has a place, and the bag itself is built to be found, opened and emptied with one hand in the rain.</p>
</div>
<div class="grid">
<div class="stack" style="flex:1 1 300px;border-top:1px solid var(--line2);padding-top:22px"><p class="eyebrow">01 · Waterproof</p><h3 class="sans" style="font-size:22px;font-weight:600">TPU-laminated Cordura, taped seams, AquaGuard zips</h3><p class="p">The shell is the same waterproof laminate used on expedition packs. Ten minutes under a shower head, nothing inside gets wet.</p></div>
<div class="stack" style="flex:1 1 300px;border-top:1px solid var(--line2);padding-top:22px"><p class="eyebrow">02 · The Morse mark</p><h3 class="sans" style="font-size:22px;font-weight:600">Three short, three long, three short</h3><p class="p">SOS, laser-cut into the side panel and raised on the patch. Anyone who knows it, knows. Everyone else sees a clean black bag.</p></div>
<div class="stack" style="flex:1 1 300px;border-top:1px solid var(--line2);padding-top:22px"><p class="eyebrow">03 · Found in the dark</p><h3 class="sans" style="font-size:22px;font-weight:600">Name window, colour tag, reflective piping</h3><p class="p">Your name and medical notes by the handle. A tag colour per person. Piping that reads black by day and lights up in a torch beam.</p></div>
<div class="stack" style="flex:1 1 300px;border-top:1px solid var(--line2);padding-top:22px"><p class="eyebrow">04 · Honest food</p><h3 class="sans" style="font-size:22px;font-weight:600">15-year rations, vegan, made without nuts</h3><p class="p">Every bag is vegan and gluten-free on the food. The only exception is the Cub's infant formula, and we say so on the box.</p></div>
</div>
<div class="grid" style="border-top:1px solid var(--line2);border-bottom:1px solid var(--line2);padding:32px 0">
<div class="stat"><span class="n">72</span><span class="l">hours covered</span></div>
<div class="stat"><span class="n">37</span><span class="l">items in the Operator</span></div>
<div class="stat"><span class="n">7.2 kg</span><span class="l">packed, with 20 L to spare</span></div>
<div class="stat"><span class="n">15 yrs</span><span class="l">ration shelf life</span></div>
</div>
</div></section>
<section class="section"><div class="wrap stack" style="gap:40px">
<div class="stack" style="gap:10px"><p class="eyebrow">Inside the Operator</p><h2 class="h2">Four pouches. Nothing to think about.</h2></div>
<div class="grid">{pouch_html}</div>
<a class="pill" href="bags/operator.html#inside" style="align-self:flex-start;height:50px">Full contents list and weights</a>
</div></section>
<section class="section light"><div class="wrap stack" style="gap:40px">
<div style="display:flex;flex-wrap:wrap;justify-content:space-between;align-items:flex-end;gap:16px">
<div class="stack" style="gap:10px"><p class="eyebrow">Guides</p><h2 class="h2">Know what to do before you need to.</h2></div>
<a href="guides/index.html" style="font-weight:600;font-size:15px;border-bottom:2px solid var(--bg);padding-bottom:2px">All guides →</a>
</div>
<div class="grid">
<a class="card dark" href="guides/power-cut-the-first-hour.html" style="flex:2 1 420px;padding:32px;justify-content:space-between;gap:48px;min-height:320px"><span class="eyebrow">Featured · 6 min read</span><span class="stack"><span class="display" style="font-size:44px">Power cut: the first hour</span><span class="p" style="color:#b5b5b5">What to do in the first five minutes, the first thirty, and the first hour. When to call 105, what never to bring indoors, and which pouch to open first.</span></span></a>
<a class="card" href="guides/the-72-hour-list-explained.html" style="flex:1 1 260px;justify-content:space-between;gap:32px"><span class="eyebrow">Checklist</span><span class="stack" style="gap:10px"><span class="display" style="font-size:30px">The Government's 72-hour list, explained</span><span class="p small">Line by line, with what's already in your bag and what you still need at home.</span></span></a>
<a class="card" href="guides/leaving-the-house-with-a-baby.html" style="flex:1 1 260px;justify-content:space-between;gap:32px"><span class="eyebrow">Family</span><span class="stack" style="gap:10px"><span class="display" style="font-size:30px">Leaving the house with a baby</span><span class="p small">Feeding without a kettle, the pram-or-wrap decision, and what goes on your back.</span></span></a>
</div>
<div class="chips">{chips_html}</div>
</div></section>
<section class="section"><div class="wrap grid">
<div class="card" style="flex:1 1 420px;padding:40px;gap:18px"><p class="eyebrow">Refills and rotation</p><h3 class="h3">Your bag tells you when it's time.</h3><p class="p">Every bag carries a rotation card and a QR code. Scan it once and we'll remind you when the water, the rations or the batteries are due, and when the power bank wants charging. Cub owners get a stage refill as their baby grows: Cub 1, Cub 2, Cub 3.</p><a href="refills.html" style="align-self:flex-start;font-weight:600;font-size:15px;border-bottom:1px solid var(--ink);padding-bottom:2px">See refill packs</a></div>
<div class="card" style="flex:1 1 420px;padding:40px;gap:18px"><p class="eyebrow">For organisations</p><h3 class="h3">One bag per placement, per desk, per home.</h3><p class="p">Children's homes, fostering agencies, councils, schools and housing associations buy in tens and hundreds, with the policy wording written for them and a rotation schedule we manage.</p><a href="organisations.html" style="align-self:flex-start;font-weight:600;font-size:15px;border-bottom:1px solid var(--ink);padding-bottom:2px">Request a quote</a></div>
</div></section>
<section class="section tight" style="border-top:1px solid var(--line)"><div class="wrap" style="display:flex;flex-wrap:wrap;gap:32px;align-items:center;justify-content:space-between">
<div class="stack" style="flex:1 1 420px;gap:10px"><h3 class="h3">Be Ready alerts</h3><p class="p">When a storm, a cold snap or an official warning is coming, we send one short message with what to check. No marketing, no noise.</p></div>
{subscribe_form(r, 'home')}
</div></section>
"""
    page("index.html", "Blackout SOS — 72-hour go bags, assembled in the UK", "A go bag for every person in your house: Operator, Recruit, Cub, Unit and Scout. Waterproof, vegan, made without nuts, 15-year rations. Three dots. Three dashes. Three days.", body, f'<script type="application/ld+json">{schema}</script>')

# ---------- RANGE ----------
def range_page():
    r = "../"
    cards = "".join(bag_card(s, r) for s in ORDER)
    rows = ""
    for s in ORDER:
        b = BAGS[s]
        rows += f'<tr><td><span style="display:inline-flex;align-items:center;gap:8px"><span class="tag" style="background:{b["colour"]}"></span><a href="{s}.html"><strong>{b["name"]}</strong></a></span></td><td>{b["who"]}</td><td>{b["specs"][1]}</td><td>{b["specs"][2]}</td><td>{b["specs"][3]}</td><td>{gbp(b["price"])}</td></tr>'
    body = f"""
<section class="section top"><div class="wrap stack" style="gap:28px">
<div class="crumbs"><a href="../index.html">Home</a><span>/</span><span class="here">Bags</span></div>
<p class="eyebrow">The range</p>
<h1 class="h1" style="max-width:1000px">One bag per person. One colour per bag.</h1>
<p class="lede">Blue for adults, red for children, yellow for the baby, green for the family duffel, orange for the pet. Every bag is waterproof, vegan and made without nut ingredients, with a write-on name card by the handle and a whistle inside. In the dark, at the door, everyone grabs the right one.</p>
</div></section>
<section class="section tight"><div class="wrap grid">{cards}</div></section>
<section class="section band"><div class="wrap stack" style="gap:28px">
<h2 class="h2">Which bag for whom</h2>
<div style="overflow-x:auto"><table class="list"><thead><tr><th>Bag</th><th>For</th><th>Capacity</th><th>Packed</th><th>Size</th><th>Price</th></tr></thead><tbody>{rows}</tbody></table></div>
<p class="p" style="max-width:760px">A household of two adults, a child of seven, a baby and a dog is two Operators, a Recruit, a Cub and a Scout, with the Cub and the Scout clipped onto the Operators so the adults' hands stay free. Add a Unit if you would leave by car or shelter at home. Prices include VAT and UK delivery.</p>
</div></section>
<section class="section"><div class="wrap grid">
<div class="card" style="flex:1 1 300px"><p class="eyebrow">Standard build</p><h3 class="h4 sans" style="font-weight:600">Every bag, every time</h3><p class="p">500D TPU-laminated Cordura, taped seams, YKK AquaGuard zips, a 1000D base. Name window by the handle with a write-on card and marker. Side bottle pocket. Whistle on a lanyard and one in the buckle. Reflective piping. The Morse SOS cut into the side.</p></div>
<div class="card" style="flex:1 1 300px"><p class="eyebrow">Honest food</p><h3 class="h4 sans" style="font-weight:600">Vegan, made without nut ingredients</h3><p class="p">NRG-5 Zero rations: 2,325 kcal per 500 g, labelled vegan and gluten-free, 15-year date. No sweets in a child's bag. The Cub's infant formula is the one exception in the range and the box says so.</p></div>
<div class="card" style="flex:1 1 300px"><p class="eyebrow">Nothing bespoke</p><h3 class="h4 sans" style="font-weight:600">Ships the day you order</h3><p class="p">Names go on the card with the marker in the lid, by you. Nothing is printed to order, so every bag is a standard product, in stock, assembled in the UK and dispatched within three working days.</p></div>
</div></section>
"""
    page("bags/index.html", "The range — Blackout SOS go bags", "Operator for adults, Recruit for children, Cub for babies, Unit for the family, Scout for the dog or cat. One bag per person, one colour per bag.", body)

# ---------- PRODUCT ----------
def product(slug):
    b = BAGS[slug]; r = "../"
    variants = ""
    if b.get("variants"):
        variants = '<div class="stack" style="gap:8px"><span class="eyebrow">Choose</span><div class="variants">' + "".join(
            f'<button type="button" class="variant" data-sku="{sku}" data-label="{lbl}" aria-pressed="{"true" if sku==b["sku"] else "false"}">{nm} · {lbl}</button>' for sku, nm, lbl in b["variants"]) + "</div></div>"
    pouches = "".join(f'<div class="stack" style="flex:1 1 230px;gap:12px"><div class="pouch"><span class="tag" style="background:{col};{"border:1px solid #3a3a3a" if col in ("#2a2a2a","#3a3a3a") else ""}"></span><span>{name} · {what}</span></div><p class="items">{"<br>".join(items)}</p></div>' for (name, col), what, items in b["pouches"])
    stages = ""
    if b.get("stages"):
        stages = '<div class="stack" style="gap:0;border-top:1px solid var(--line2)">' + "".join(f'<div class="row" style="flex-wrap:wrap"><strong style="flex:0 0 220px">{t}</strong><span style="flex:1 1 300px;text-align:left;color:var(--soft)">{d}</span></div>' for t, d in b["stages"]) + "</div>"
    carry = ""
    if b.get("carry"):
        carry = f'<section class="section"><div class="wrap stack" style="gap:28px"><div class="stack" style="gap:10px"><p class="eyebrow">Carry system</p><h2 class="h2">{b["carry_title"]}</h2></div><div class="grid">' + "".join(f'<div class="card" style="flex:1 1 280px"><h3 class="h4 sans" style="font-weight:600">{t}</h3><p class="p">{d}</p></div>' for t, d in b["carry"]) + "</div></div></section>"
    build_rows = b["build"]; half = (len(build_rows) + 1) // 2
    def rows(rs): return "".join(f'<div class="row"><span>{k}</span><span>{v}</span></div>' for k, v in rs)
    rotation = "".join(f'<div class="row"><span>{k}</span><span>{v}</span></div>' for k, v in b["rotation"])
    faq = "".join(f'<div class="faq"><p>{q}</p><p class="p small">{a}</p></div>' for q, a in b["faq"])
    pairs = "".join(f'<a class="card" href="{p}.html" style="flex:1 1 300px;flex-direction:row;justify-content:space-between;align-items:center;gap:20px"><span class="stack" style="gap:6px"><span class="display" style="font-size:30px">{BAGS[p]["name"]}</span><span class="p small">{line} {gbp(BAGS[p]["price"])}</span></span><span class="tag" style="background:{BAGS[p]["colour"]}"></span></a>' for p, line in b["pairs"])
    notes = "".join(f'<p>{n}</p>' for n in b["notes"])
    schema = json.dumps({"@context": "https://schema.org", "@type": "Product", "name": f"Blackout SOS {b['name']}", "description": b["card"], "brand": {"@type": "Brand", "name": "Blackout SOS"}, "offers": {"@type": "Offer", "priceCurrency": "GBP", "price": f"{b['price']/100:.2f}", "availability": "https://schema.org/PreOrder", "url": f"{SITE}/bags/{slug}.html"}})
    body = f"""
<div class="wrap crumbs" style="padding-top:24px"><a href="../index.html">Home</a><span>/</span><a href="index.html">Bags</a><span>/</span><span class="here">{b['name']}</span></div>
<section class="wrap split" style="padding-top:32px;padding-bottom:clamp(56px,7vw,96px)">
<div class="stack" style="flex:1 1 520px;gap:14px"><div class="bag-art">{art(slug)}</div><div class="thumbs"><div>Front</div><div>Open</div><div>Side</div><div>Detail</div><div>Worn</div></div></div>
<div class="stack" style="flex:1 1 420px;gap:24px">
<div class="stack" style="gap:10px"><div class="eyebrow" style="display:flex;align-items:center;gap:10px"><span class="tag" style="width:10px;height:10px;background:{b['colour']}"></span>{b['who']} · {b['colour_name']} tag</div><h1 class="h1" style="font-size:clamp(56px,7vw,96px)">{b['name']}</h1><p class="lede" style="font-size:17px">{b['lede']}</p></div>
<div class="muted small" style="display:flex;flex-wrap:wrap;gap:8px 24px;border-top:1px solid var(--line);border-bottom:1px solid var(--line);padding:14px 0">{"".join(f"<span>{s}</span>" for s in b["specs"])}</div>
<div style="display:flex;align-items:baseline;gap:14px"><span class="price">{gbp(b['price'])}</span><span class="muted small">inc. VAT · free UK delivery</span></div>
<form class="stack" style="gap:14px" data-product="{b['sku']}">
{variants}
<button type="submit" class="pill solid" style="height:58px;font-size:16px">Add to basket — {gbp(b['price'])}</button>
<p class="p small">Write-on name card and marker included. Nothing to personalise, nothing to wait for.</p>
</form>
<div class="stack" style="gap:10px;font-size:14px;line-height:1.5;color:var(--soft)">{notes}</div>
<div class="anchor-list" style="border-top:1px solid var(--line)"><a href="#inside"><span>What's inside</span><span>{len([i for p in b['pouches'] for i in p[2]])} lines</span></a><a href="#build"><span>The bag</span><span>Materials and build</span></a><a href="#rotation"><span>Rotation and refills</span><span>5 to 15 years</span></a><a href="#faq"><span>Questions</span><span>Straight answers</span></a></div>
</div>
</section>
<section id="inside" class="section band"><div class="wrap stack" style="gap:36px">
<div class="stack" style="gap:10px"><p class="eyebrow">What's inside</p><h2 class="h2">{b['inside_title']}</h2></div>
<div class="grid">{pouches}</div>
{stages}
<p class="p" style="max-width:760px">{b['you_add']}</p>
</div></section>
{carry}
<section id="build" class="section"><div class="wrap split">
<div class="stack" style="flex:1 1 360px;gap:14px"><p class="eyebrow">The bag</p><h2 class="h2">{b['build_title']}</h2><p class="p">{b['build_text']}</p></div>
<div style="flex:2 1 520px;display:flex;flex-wrap:wrap;gap:0 40px"><div class="rows" style="flex:1 1 240px">{rows(build_rows[:half])}</div><div class="rows" style="flex:1 1 240px">{rows(build_rows[half:])}</div></div>
</div></section>
<section id="rotation" class="section band"><div class="wrap split">
<div class="stack" style="flex:1 1 360px;gap:14px"><p class="eyebrow">Rotation and refills</p><h2 class="h2">Buy it once. We'll keep it alive.</h2><p class="p">Scan the card in the lid and we remember your dates. When something is due, a refill pack arrives with exactly what to swap and nothing else. <a href="../refills.html" style="border-bottom:1px solid var(--muted)">How refills work</a>.</p></div>
<div class="rows" style="flex:1 1 420px">{rotation}</div>
</div></section>
<section id="faq" class="section"><div class="wrap split">
<div style="flex:1 1 300px"><p class="eyebrow" style="margin-bottom:10px">Questions</p><h2 class="h2">Straight answers.</h2></div>
<div style="flex:2 1 560px;display:flex;flex-direction:column">{faq}</div>
</div></section>
<section class="section tight" style="border-top:1px solid var(--line)"><div class="wrap stack" style="gap:28px"><h2 class="h3">Pairs with</h2><div class="grid">{pairs}</div></div></section>
"""
    page(f"bags/{slug}.html", f"{b['name']} go bag — {b['who']} · Blackout SOS", b["card"], body, f'<script type="application/ld+json">{schema}</script>')

# ---------- GUIDES ----------
def guide_card(g, r):
    return f'<a class="card outline" href="{r}guides/{g["slug"]}.html" style="flex:1 1 300px;padding:24px;gap:14px;min-height:180px"><span class="eyebrow" style="letter-spacing:2px">{g["cat"]} · {g["mins"]} min</span><span class="display" style="font-size:28px;line-height:1">{g["plain"]}</span><span class="p small">{g["summary"]}</span></a>'

def guides_index():
    r = "../"
    by = {g["slug"]: g for g in GUIDES}
    cards = "".join(guide_card(g, r) for g in GUIDES)
    chips = "".join(f'<a class="chip" href="#all" style="padding:8px 14px;font-size:13px">{c}</a>' for c in CATS)
    numbers = [("999", "Emergency: life at risk, fire, crime in progress"), ("105", "Power cut: free, any network, connects to your local operator"), ("111", "NHS: urgent but not life-threatening"), ("0345 988 1188", "Floodline: warnings and advice, 24 hours"), ("0800 111 999", "Gas emergency: smell gas, open windows, get out, call")]
    nums = "".join(f'<div class="card" style="flex:1 1 240px;padding:22px;gap:6px"><span class="display" style="font-size:{"44px" if len(n)<5 else "30px"};line-height:1.1">{n}</span><span class="p small">{d}</span></div>' for n, d in numbers)
    body = f"""
<section class="section top"><div class="wrap stack" style="gap:28px">
<p class="eyebrow">Guides</p>
<h1 class="h1" style="max-width:1000px">Know what to do before you need to.</h1>
<p class="lede">Short, practical guides written for the UK, checked against official advice, and tied to what's in your bag. Read them once now; print the one-page versions for the lid pocket.</p>
</div></section>
<section class="wrap grid" style="padding-bottom:clamp(56px,7vw,96px)">
<a class="card" href="power-cut-the-first-hour.html" style="flex:2 1 480px;padding:40px;justify-content:space-between;gap:64px;min-height:380px"><span class="eyebrow" style="display:flex;justify-content:space-between"><span>Featured · Power</span><span>6 min read</span></span><span class="stack" style="gap:14px"><span class="display h2">Power cut: the first hour</span><span class="p" style="color:var(--soft);font-size:16px;max-width:560px">The first five minutes, the first thirty, the first hour. When to call 105, what never to bring indoors, and which pouch to open first.</span><span style="font-weight:600;font-size:15px">Read the guide →</span></span></a>
<div class="stack" style="flex:1 1 320px;gap:20px">
<a class="card light" href="the-72-hour-list-explained.html" style="flex:1;padding:32px;justify-content:space-between;gap:32px;border-color:var(--ink)"><span class="eyebrow">Official · Checklist</span><span class="stack" style="gap:10px"><span class="display" style="font-size:34px">The Government's 72-hour list, explained</span><span class="p small">Every line of the Be Ready advice, what's already in your bag, what you still need at home. Printable.</span></span></a>
<a class="card" href="leaving-the-house-with-a-baby.html" style="flex:1;padding:32px;justify-content:space-between;gap:32px"><span class="eyebrow">Family · 7 min</span><span class="stack" style="gap:10px"><span class="display" style="font-size:34px">Leaving the house with a baby</span><span class="p small">Feeding without a kettle, the pram-or-wrap decision, what goes on your back.</span></span></a>
</div>
</section>
<section id="all" class="section band"><div class="wrap stack" style="gap:32px">
<div style="display:flex;flex-wrap:wrap;justify-content:space-between;align-items:flex-end;gap:16px"><h2 class="h2">All guides</h2><div class="chips">{chips}</div></div>
<div class="grid" style="gap:16px">{cards}</div>
</div></section>
<section class="section"><div class="wrap split">
<div class="stack" style="flex:1 1 320px;gap:12px"><p class="eyebrow">Official numbers</p><h2 class="h2">Who to call. Write these on the card.</h2><p class="p">These are the UK numbers that matter in the first hour. They are printed on the contacts card in every bag.</p></div>
<div style="flex:2 1 560px;display:flex;flex-wrap:wrap;gap:14px">{nums}<a class="card light" href="https://prepare.campaign.gov.uk/" rel="noopener" style="flex:1 1 240px;padding:22px;gap:6px;border-color:var(--ink)"><span class="display" style="font-size:30px;line-height:1.1">gov.uk Prepare</span><span class="p small">The official household guidance this site is built around →</span></a></div>
</div></section>
"""
    page("guides/index.html", "Emergency guides for UK households — Blackout SOS", "Power cuts, flooding, storms, water, babies, children, pets, medication and the 72-hour list: short UK guides checked against official advice.", body)

def guide_page(g):
    by = {x["slug"]: x for x in GUIDES}; r = "../"
    secs = ""
    for label, unit, heading, items in g["sections"]:
        lis = "".join(f"<li>{i}</li>" for i in items)
        secs += f'<div class="stack" style="gap:16px"><div class="step-n"><span class="n">{label}</span><span class="u">{unit}</span></div><h2 class="sub">{heading}</h2><ol>{lis}</ol></div>'
        if g.get("never") and label == g["sections"][1][0]:
            secs += f'<div class="never"><p class="eyebrow">{g["never"][0]}</p><p>{g["never"][1]}</p></div>'
    if g.get("after"):
        secs += f'<div class="stack" style="gap:10px;border-top:1px solid var(--line);padding-top:24px"><p class="eyebrow">{g["after"][0]}</p><p class="body">{g["after"][1]}</p></div>'
    frombag = "".join(f'<div style="display:flex;gap:10px;align-items:flex-start"><span class="tag" style="width:10px;height:10px;background:{c};margin-top:5px;{"border:1px solid #3a3a3a" if c in ("#2a2a2a","#3a3a3a") else ""}"></span><span><strong>{k}</strong> {v}</span></div>' for c, k, v in g["frombag"] if not c.startswith("Unit"))
    frombag += "".join(f'<div style="display:flex;gap:10px;align-items:flex-start"><span class="tag" style="width:10px;height:10px;background:#2BA84A;margin-top:5px"></span><span><strong>{k}</strong> {v}</span></div>' for c, k, v in g["frombag"] if c.startswith("Unit"))
    numbers = "".join(f'<div class="kv"><span>{k}</span><strong>{v}</strong></div>' for k, v in g["numbers"])
    nxt = "".join(f'<a href="{s}.html">{by[s]["plain"]} →</a>' for s in g["next"])
    sources = "".join(f'<li><a href="{u}" rel="noopener" style="border-bottom:1px solid var(--line3)">{t}</a></li>' for t, u in g["sources"])
    cta_slug, cta_title, cta_line = g["cta"]
    schema = json.dumps({"@context": "https://schema.org", "@type": "Article", "headline": g["plain"], "description": g["summary"], "author": {"@type": "Organization", "name": "Blackout SOS"}, "publisher": {"@type": "Organization", "name": "Blackout SOS"}, "dateModified": datetime.date.today().isoformat(), "mainEntityOfPage": f"{SITE}/guides/{g['slug']}.html"})
    body = f"""
<section class="section top" style="padding-bottom:clamp(32px,4vw,56px)"><div class="wrap stack" style="gap:22px">
<div class="crumbs"><a href="index.html">Guides</a><span>/</span><span>{g['cat']}</span></div>
<h1 class="h1" style="max-width:1000px">{g['title']}</h1>
<p class="lede">{g['lede']}</p>
<div class="muted small" style="display:flex;flex-wrap:wrap;gap:10px 24px;border-top:1px solid var(--line);padding-top:16px"><span>{g['mins']} min read</span><span>{g['checked']}</span><span>Updated {UPDATED}</span><a href="javascript:window.print()" style="margin-left:auto;font-weight:600;color:var(--ink)">Print this guide</a></div>
</div></section>
<section class="wrap split" style="padding-bottom:clamp(56px,7vw,96px);gap:56px">
<article class="stack" style="flex:2 1 560px;max-width:760px;gap:40px">
{secs}
<div class="stack" style="gap:10px;border-top:1px solid var(--line);padding-top:24px"><p class="eyebrow">Sources, checked {UPDATED}</p><ul style="gap:6px;font-size:14px">{sources}</ul></div>
</article>
<aside class="stack" style="flex:1 1 300px;gap:20px">
<div class="aside-card"><p class="eyebrow">From your bag, in order</p><div class="stack" style="gap:10px;font-size:14px;line-height:1.5">{frombag}</div></div>
<div class="aside-card"><p class="eyebrow">Numbers</p>{numbers}</div>
<a class="aside-card light" href="../bags/{cta_slug}.html" style="gap:8px"><span class="eyebrow">Don't have the bag yet?</span><span class="display" style="font-size:30px;line-height:1">{cta_title}</span><span class="p small">{cta_line}</span></a>
<div class="stack next" style="gap:10px"><p class="eyebrow">Read next</p>{nxt}</div>
</aside>
</section>
"""
    page(f"guides/{g['slug']}.html", f"{g['plain']} — Blackout SOS guides", g["summary"], body, f'<script type="application/ld+json">{schema}</script>')

# ---------- OTHER PAGES ----------
def basket():
    body = """
<section class="section top"><div class="wrap stack" style="gap:28px">
<h1 class="h1">Basket</h1>
<div data-basket class="stack" style="gap:0;border-top:1px solid var(--line)"></div>
<div data-basket-empty class="stack" style="gap:16px"><p class="lede">Your basket is empty.</p><a class="pill solid" href="bags/index.html" style="align-self:flex-start">Shop the range</a></div>
<div data-basket-summary hidden class="stack" style="gap:20px;max-width:520px;margin-left:auto;width:100%">
<div class="row" style="font-size:18px"><span>Total, inc. VAT</span><strong data-basket-total>£0</strong></div>
<p class="p small">Free UK delivery. Assembled to order and dispatched within three working days. Payment is taken on Stripe's secure page: cards, Apple Pay and Google Pay.</p>
<button type="button" class="pill solid" data-checkout style="height:58px;font-size:16px">Checkout</button>
<p class="notice" data-checkout-msg hidden></p>
<p class="p small">Buying for an organisation? <a href="organisations.html" style="border-bottom:1px solid var(--muted)">Ask for a quote and invoice terms</a>.</p>
</div>
</div></section>
"""
    page("basket.html", "Basket — Blackout SOS", "Your Blackout SOS basket.", body)

def checkout_pages():
    page("checkout/success.html", "Order received — Blackout SOS", "Thank you. Your order is being assembled.", """
<section class="section top"><div class="wrap stack" style="gap:20px;max-width:760px" data-order-success>
<p class="eyebrow">Order received</p>
<h1 class="h1">Thank you.</h1>
<p class="lede">Your bag is being assembled in the UK and will be dispatched within three working days. Stripe has emailed your receipt; we'll email tracking when it leaves.</p>
<p class="notice" data-order-ref hidden></p>
<p class="p">Two things to do while you wait: read <a href="../guides/the-72-hour-list-explained.html" style="border-bottom:1px solid var(--muted)">the 72-hour list, explained</a>, and sign up for Be Ready alerts below so the bag gets used before it's needed.</p>
<a class="pill" href="../guides/index.html" style="align-self:flex-start">Read the guides</a>
</div></section>
""")
    page("checkout/cancel.html", "Checkout cancelled — Blackout SOS", "Your basket is still here.", """
<section class="section top"><div class="wrap stack" style="gap:20px;max-width:760px">
<p class="eyebrow">Checkout cancelled</p>
<h1 class="h1">Nothing was charged.</h1>
<p class="lede">Your basket is exactly as you left it. If something went wrong on the payment page, try again, or email hello@blackoutsos.com and we'll take the order by hand.</p>
<a class="pill solid" href="../basket.html" style="align-self:flex-start">Back to the basket</a>
</div></section>
""")

def refills():
    packs = [("Six-month check", "Free", "A checklist by email: batteries, medicines, baby sizes, phone numbers, the power bank charge. Nothing to buy.", "Every six months, when the clocks change"),
             ("Water and first aid refill", "From launch", "Fresh 5-year water pouches and a new BS 8599-1 kit, with the old ones' dates on the card.", "Years 3 and 5"),
             ("Cub stage refill", "From launch", "The nappies, the feeding and the tag dots for the next stage. The bag stays.", "When your baby moves up a stage"),
             ("Full refresh", "From launch", "Rations, water, batteries, power bank, hand warmers, glow sticks, wipes: everything with a date, replaced in one box.", "Year 5, and year 10"),
             ("Comfort pack", "From launch", "Glucose, oat bars, electrolytes and sweets, vegan and made without nut ingredients.", "Every 12 to 18 months")]
    rows = "".join(f'<div class="card" style="flex:1 1 300px"><div style="display:flex;justify-content:space-between;gap:12px"><h3 class="h4 sans" style="font-weight:600">{n}</h3><span class="muted small" style="white-space:nowrap">{p}</span></div><p class="p">{d}</p><p class="eyebrow" style="letter-spacing:2px">{w}</p></div>' for n, p, d, w in packs)
    body = f"""
<section class="section top"><div class="wrap stack" style="gap:28px">
<p class="eyebrow">Refills and rotation</p>
<h1 class="h1" style="max-width:1000px">Your bag tells you when it's time.</h1>
<p class="lede">Every bag carries a rotation card and a QR code. Scan it once, tell us which bag and when you bought it, and we'll remind you when the water, the rations or the batteries are due and when the power bank wants charging. When something is due, a refill pack arrives with exactly what to swap and nothing else.</p>
</div></section>
<section class="section band"><div class="wrap stack" style="gap:28px"><h2 class="h2">The packs</h2><div class="grid">{rows}</div><p class="p">Refill packs go on sale with the first bags. Register below and we'll tell you the day they do.</p></div></section>
<section class="section"><div class="wrap split">
<div class="stack" style="flex:1 1 360px;gap:14px"><p class="eyebrow">Register your bag</p><h2 class="h2">Reminders, not marketing.</h2><p class="p">One email when something in your bag is due, and one when a storm or an official warning is coming. Nothing else, and you can stop them any time.</p></div>
<form class="stack" style="flex:1 1 420px;gap:14px" data-api="/subscribe">
<input type="hidden" name="source" value="refills">
<div class="form-row">
<label class="field">Email<input name="email" type="email" required placeholder="you@example.com"></label>
<label class="field">Which bag<select name="bag"><option value="">Choose</option><option>Operator</option><option>Recruit</option><option>Cub 1</option><option>Cub 2</option><option>Cub 3</option><option>Unit</option><option>Scout Dog</option><option>Scout Cat</option><option>Not yet</option></select></label>
</div>
<label class="field">Month you bought it<input name="bought" type="month"></label>
<button type="submit" class="pill solid" style="align-self:flex-start">Register</button>
<p class="p small ok" data-done hidden>Registered. We'll remind you when it's time.</p>
</form>
</div></section>
"""
    page("refills.html", "Refills and rotation — Blackout SOS", "Register your bag and we remind you when the water, rations, batteries and baby sizes are due. Refill packs with exactly what to swap.", body)

def organisations():
    segs = [("Children's homes", "A Recruit for every child and a Unit for every home, written into the home's emergency policy and the welcome pack. We supply the policy wording."),
            ("Fostering agencies", "A Recruit per placement at agency pricing, with the carer guides. A line in the placement checklist, not another task."),
            ("Councils and resilience forums", "Operators for vulnerable residents in flood-risk wards, grab bags for wardens and rest-centre teams. Pilots from 50."),
            ("Charities and foodbanks", "A give-back scheme: one bag donated for every twenty sold, and co-branded Be Ready alerts for the people you support."),
            ("Animal rehoming", "A Scout with every adoption, with a co-branded pet card. The dog or cat leaves with its own bag."),
            ("Workplaces and housing", "A bag per desk or per flat, a rotation schedule we manage, and a yearly check-in so the kit is live when the building isn't.")]
    seg_html = "".join(f'<div class="card" style="flex:1 1 300px"><h3 class="h4 sans" style="font-weight:600">{n}</h3><p class="p">{d}</p></div>' for n, d in segs)
    body = f"""
<section class="section top"><div class="wrap stack" style="gap:28px">
<p class="eyebrow">For organisations</p>
<h1 class="h1" style="max-width:1100px">One bag per placement, per desk, per home.</h1>
<p class="lede">Children's homes, fostering agencies, councils, charities, rehoming centres and workplaces buy in tens and hundreds. Volume pricing from ten bags, invoice terms for public bodies and charities, the emergency-policy wording written for you, and a rotation schedule we manage so the bags are live when they're needed.</p>
</div></section>
<section class="section band"><div class="wrap stack" style="gap:28px"><h2 class="h2">Who we work with</h2><div class="grid">{seg_html}</div></div></section>
<section class="section"><div class="wrap split">
<div class="stack" style="flex:1 1 360px;gap:14px"><p class="eyebrow">How it works</p><h2 class="h2">Ask, and we'll write the policy with you.</h2>
<ol class="body" style="padding-left:22px;display:flex;flex-direction:column;gap:10px"><li>Tell us who the bags are for and how many.</li><li>We send a quote, a sample bag if you want one, and the policy wording for your emergency plan.</li><li>Bags arrive assembled, with write-on name cards, in one delivery or staggered.</li><li>We hold the rotation dates and send the refills when they're due, invoiced the same way.</li></ol></div>
<form class="stack" style="flex:1 1 420px;gap:14px" data-api="/enquiry">
<input type="hidden" name="kind" value="organisation">
<div class="form-row"><label class="field">Organisation<input name="org" required></label><label class="field">Your name<input name="name" required></label></div>
<div class="form-row"><label class="field">Email<input name="email" type="email" required></label><label class="field">Phone<input name="phone" type="tel"></label></div>
<div class="form-row"><label class="field">Type<select name="segment"><option>Children's home</option><option>Fostering agency</option><option>Council or resilience forum</option><option>Charity or foodbank</option><option>Animal rehoming</option><option>Workplace or housing</option><option>Retailer</option><option>Other</option></select></label><label class="field">How many bags, roughly<input name="bags" placeholder="e.g. 40 Recruits, 6 Units"></label></div>
<label class="field">Anything else<textarea name="message" placeholder="Who the bags are for, when you need them, whether you'd like a sample."></textarea></label>
<button type="submit" class="pill solid" style="align-self:flex-start">Request a quote</button>
<p class="p small ok" data-done hidden>Received. Omar will reply within two working days.</p>
</form>
</div></section>
"""
    page("organisations.html", "For organisations — Blackout SOS", "Go bags for children's homes, fostering agencies, councils, charities, rehoming centres and workplaces. Volume pricing, invoice terms, policy wording, managed rotation.", body)

def about():
    body = """
<section class="section top"><div class="wrap stack" style="gap:28px">
<p class="eyebrow">Our story</p>
<h1 class="h1" style="max-width:1000px">Built by a foster carer who kept a bag by the door.</h1>
<p class="lede">Blackout SOS was started in London in 2026 by Omar Rahmat, a foster carer of seven years who runs supported accommodation for young people leaving care. In a house of five people and a cat, with children who had already lived through enough, the question was never whether to have a go bag. It was why the ones you could buy were so bad.</p>
</div></section>
<section class="section band"><div class="wrap grid">
<div class="card" style="flex:1 1 300px"><p class="eyebrow">The problem</p><p class="p">The kits on sale were a rucksack with things thrown in: a cheap torch, a foil blanket, a tin of biscuits with nuts in it, camouflage on the outside and nothing for a child, a baby or a dog. When the Government asked every household to hold three days of supplies, the answer on the shelf was a bag you'd be embarrassed to carry and couldn't find the plasters in.</p></div>
<div class="card" style="flex:1 1 300px"><p class="eyebrow">The idea</p><p class="p">One bag per person, because an emergency doesn't happen to households, it happens to people. One colour per bag, so a seven-year-old grabs the right one in the dark. Four pouches with a colour each, so the first aid is where it was last time. Food everyone can eat. A bag you'd carry on the Tube.</p></div>
<div class="card" style="flex:1 1 300px"><p class="eyebrow">The rules</p><p class="p">We don't sell fear. We point to 999 and the authorities first, we check every guide against official advice, and we don't make a claim the label can't back. Vegan and made without nut ingredients means we can show you the paperwork. Waterproof means ten minutes under a shower head.</p></div>
</div></section>
<section class="section"><div class="wrap split">
<div class="stack" style="flex:1 1 360px;gap:14px"><p class="eyebrow">How we make them</p><h2 class="h2">Designed in London. Assembled in the UK.</h2></div>
<div class="stack" style="flex:2 1 520px;gap:16px"><p class="body">The bags are made to our drawings from the same TPU-laminated Cordura, taped seams and YKK AquaGuard zips as expedition packs. The contents are sourced from UK suppliers wherever one exists, checked against the claims on the box, and packed by hand in the UK into pouches with a place for everything. Every bag leaves with a rotation card, and we hold the dates so you don't have to.</p>
<p class="body">The company behind the brand is Urban Carers Ltd, registered in England and Wales. If you want to talk to the person who packed your bag, <a href="contact.html" style="border-bottom:1px solid var(--muted)">write to us</a>: it will be a short conversation, because we are a small team, and a useful one.</p></div>
</div></section>
"""
    page("about.html", "Our story — Blackout SOS", "Blackout SOS was started in London by a foster carer who couldn't find a go bag worth keeping by the door. One bag per person, one colour per bag.", body)

def delivery():
    body = """
<section class="section top"><div class="wrap stack" style="gap:28px"><p class="eyebrow">Delivery and returns</p><h1 class="h1">Three working days, free, tracked.</h1>
<p class="lede">Every bag is assembled to order in the UK and dispatched within three working days. UK delivery is free and tracked: Royal Mail Tracked 48 for the backpacks, a courier for the Unit. You get the tracking number by email when it leaves.</p></div></section>
<section class="section band"><div class="wrap grid">
<div class="card" style="flex:1 1 300px"><p class="eyebrow">Delivery</p><p class="p">Free, tracked, to any UK address including Northern Ireland, the Highlands and the islands. Signed for on delivery for the Unit. International delivery is coming with our US and European launches; until then, email us and we'll quote.</p></div>
<div class="card" style="flex:1 1 300px"><p class="eyebrow">What's inside, and the post</p><p class="p">Bags contain lithium batteries and a power bank, which travel by ground under the carrier's rules, and no matches or lighters, which can't be posted at all. The multi-tool is UK-carry-legal: non-locking, blade under 7.62 cm.</p></div>
<div class="card" style="flex:1 1 300px"><p class="eyebrow">Returns</p><p class="p">Thirty days to return an unopened bag for a full refund: seals intact, contents unused. Under the Consumer Contracts Regulations you can cancel within 14 days of receiving your order for any reason; sealed hygiene and food items that have been unsealed can't be returned. Faulty items are replaced first, refunded second.</p></div>
</div></section>
<section class="section"><div class="wrap stack" style="gap:16px;max-width:760px"><h2 class="h3">How to return something</h2><p class="body">Email hello@blackoutsos.com with your order number and what's wrong. We send a prepaid label the same working day for faults, and a returns address for changes of mind. Refunds reach your card within five working days of the bag reaching us.</p></div></section>
"""
    page("delivery-returns.html", "Delivery and returns — Blackout SOS", "Free tracked UK delivery within three working days. Thirty-day returns on unopened bags. Faults replaced first.", body)

def contact():
    body = """
<section class="section top"><div class="wrap split">
<div class="stack" style="flex:1 1 360px;gap:20px"><p class="eyebrow">Contact</p><h1 class="h1">Talk to the people who packed it.</h1>
<p class="lede">Questions, orders, complaints, press and partnerships all come to one inbox and get a human reply within one working day. Complaints are acknowledged within four working hours and resolved within 48.</p>
<div class="rows"><div class="row"><span>Email</span><span>hello@blackoutsos.com</span></div><div class="row"><span>Organisations</span><span><a href="organisations.html">Request a quote</a></span></div><div class="row"><span>Company</span><span>Urban Carers Ltd, England and Wales, 15419139</span></div></div>
<p class="p small">In an emergency, call 999. This inbox is not monitored around the clock and we are not the emergency services.</p></div>
<form class="stack" style="flex:1 1 420px;gap:14px" data-api="/enquiry">
<input type="hidden" name="kind" value="contact">
<div class="form-row"><label class="field">Your name<input name="name" required></label><label class="field">Email<input name="email" type="email" required></label></div>
<div class="form-row"><label class="field">About<select name="subject"><option>A question</option><option>My order</option><option>A complaint</option><option>Press</option><option>A partnership</option><option>Something else</option></select></label><label class="field">Order number, if you have one<input name="order"></label></div>
<label class="field">Message<textarea name="message" required></textarea></label>
<button type="submit" class="pill solid" style="align-self:flex-start">Send</button>
<p class="p small ok" data-done hidden>Received. You'll hear from a person within one working day.</p>
</form>
</div></section>
"""
    page("contact.html", "Contact — Blackout SOS", "Questions, orders, complaints, press and partnerships: one inbox, a human reply within one working day.", body)

def privacy():
    body = f"""
<section class="section top"><div class="wrap stack" style="gap:20px;max-width:800px"><p class="eyebrow">Privacy</p><h1 class="h1">What we keep, and why.</h1>
<p class="lede">Blackout SOS is a trading name of Urban Carers Ltd (company 15419139), the data controller for this site. We keep as little as a shop can.</p>
<div class="stack body" style="gap:14px">
<p><strong>When you buy.</strong> Your name, email, delivery address and what you bought are stored in our order system so we can assemble, dispatch and support your order, and for the six years tax law requires. Payment is taken by Stripe on its own secure page; we never see your card number. Stripe's privacy policy covers what it holds.</p>
<p><strong>When you sign up for alerts or register a bag.</strong> Your email, which bag and when you bought it, so we can send the rotation reminders and Be Ready alerts you asked for. Every email has an unsubscribe link, and we delete the record when you use it.</p>
<p><strong>When you write to us.</strong> Your message and contact details, kept while we deal with it and for a year afterwards.</p>
<p><strong>Cookies and tracking.</strong> None for advertising. Your basket is kept in your own browser's storage until you check out. We measure traffic with privacy-respecting analytics that don't identify you.</p>
<p><strong>Where it lives.</strong> Orders, sign-ups and messages are held with our database provider, Supabase; email with our email provider; payments with Stripe. Each processes data under a written contract.</p>
<p><strong>Your rights.</strong> You can ask for a copy of what we hold, correct it, or have it deleted, by emailing hello@blackoutsos.com. You can complain to the Information Commissioner's Office at ico.org.uk.</p>
<p class="p small">Last updated {UPDATED}.</p>
</div></div></section>
"""
    page("privacy.html", "Privacy — Blackout SOS", "What Blackout SOS keeps about you, why, and your rights.", body)

def terms():
    body = f"""
<section class="section top"><div class="wrap stack" style="gap:20px;max-width:800px"><p class="eyebrow">Terms</p><h1 class="h1">The plain version.</h1>
<div class="stack body" style="gap:14px">
<p><strong>Who you are buying from.</strong> Urban Carers Ltd, trading as Blackout SOS, registered in England and Wales, company number 15419139. Email hello@blackoutsos.com.</p>
<p><strong>Prices and payment.</strong> Prices are in pounds sterling and include VAT and UK delivery. Payment is taken in full at checkout by Stripe. A contract is formed when we email to confirm dispatch; until then we can cancel and refund if, for example, an item is out of stock or a price was shown wrongly.</p>
<p><strong>Delivery.</strong> Within three working days of your order, tracked, to UK addresses. Risk passes to you on delivery.</p>
<p><strong>Cancelling and returning.</strong> You may cancel within 14 days of receiving your order for any reason and return it at your cost for a full refund, provided seals are intact; sealed food, hygiene and first-aid items that have been unsealed cannot be returned for hygiene reasons. We extend this to 30 days for unopened bags. Faulty goods are repaired, replaced or refunded as the Consumer Rights Act 2015 requires.</p>
<p><strong>What the bag is, and isn't.</strong> Our bags and guides are general preparedness products and advice. They are not a substitute for the emergency services or official instructions, and we don't guarantee any outcome in an emergency. You are responsible for checking the contents against your own medical, dietary and legal needs, keeping the rotation dates, and adding your own medication and documents.</p>
<p><strong>Allergens and diet.</strong> Rations and comfort items are labelled vegan and gluten-free and are made without nut ingredients; the Cub's infant formula is dairy-based. Always read the label on the item itself, which is the legally binding one.</p>
<p><strong>Liability.</strong> Nothing in these terms limits liability for death or personal injury caused by negligence, or anything else the law doesn't let us limit. Otherwise our liability for an order is limited to the price you paid for it.</p>
<p><strong>Law.</strong> These terms are governed by the law of England and Wales and the courts of England and Wales.</p>
<p class="p small">Last updated {UPDATED}.</p>
</div></div></section>
"""
    page("terms.html", "Terms — Blackout SOS", "The plain terms of buying from Blackout SOS.", body)

def notfound():
    page("404.html", "Page not found — Blackout SOS", "That page isn't here.", """
<section class="section top"><div class="wrap stack" style="gap:20px"><p class="eyebrow">404</p><h1 class="h1">That page isn't here.</h1><p class="lede">Three dots, three dashes, three days: try the <a href="index.html" style="border-bottom:1px solid var(--muted)">home page</a>, the <a href="bags/index.html" style="border-bottom:1px solid var(--muted)">bags</a> or the <a href="guides/index.html" style="border-bottom:1px solid var(--muted)">guides</a>.</p></div></section>
""")

def meta_files():
    urls = ["", "bags/", "bags/operator.html", "bags/recruit.html", "bags/cub.html", "bags/unit.html", "bags/scout.html", "guides/"] + [f"guides/{g['slug']}.html" for g in GUIDES] + ["refills.html", "organisations.html", "about.html", "delivery-returns.html", "contact.html", "privacy.html", "terms.html"]
    today = datetime.date.today().isoformat()
    sm = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + "".join(f"<url><loc>{SITE}/{u}</loc><lastmod>{today}</lastmod></url>\n" for u in urls) + "</urlset>\n"
    write("sitemap.xml", sm)
    write("robots.txt", f"User-agent: *\nAllow: /\nDisallow: /admin/\nDisallow: /checkout/\nSitemap: {SITE}/sitemap.xml\n")
    write(".nojekyll", "")

if __name__ == "__main__":
    home(); range_page()
    for s in ORDER: product(s)
    guides_index()
    for g in GUIDES: guide_page(g)
    basket(); checkout_pages(); refills(); organisations(); about(); delivery(); contact(); privacy(); terms(); notfound(); meta_files()
    print("built")

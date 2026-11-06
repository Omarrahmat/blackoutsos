"""Standard Issue: the single launch go bag (Nov 2026).
The full range (Operator, Recruit, Cub, Unit, Scout) is kept in content_bags.py and on the git branch range-v1;
its pages are replaced by redirects to the Standard Issue until the range launches."""
import json

SI = dict(
    name="Standard Issue", sku="standard-issue", price=13900, who="One adult, 72 hours",
    lede="Everything one adult needs for the first 72 hours of a power cut, flood, storm or evacuation, packed by hand in the UK into a plain black 30-litre rucksack. A roll-top liner and three colour-coded dry bags inside keep the kit dry in the rain. Pick it up and go.",
    specs=["72 hours", "1 adult", "30 L", "About 5.5 kg packed", "Contents stay dry", "Packed in the UK"],
    groups=[
        ("#2f7d4a", "Green dry bag · water and food", ["3 × 500 ml emergency water pouches, 5-year", "Water purification tablets", "750 ml water bottle, in the side pocket", "2 emergency ration bars, about 2,400 kcal each, 5-year", "Spork"]),
        ("#2a2a2a", "Black dry bag · warmth and shelter", ["Reusable emergency bivvy bag", "2 foil blankets", "Reusable rain poncho", "4 hand warmers", "Beanie and gloves"]),
        ("#c0392b", "Red dry bag · first aid and hygiene", ["Compact first aid kit", "2 FFP2 masks, 2 pairs of nitrile gloves", "Wet wipes and hand sanitiser", "Tissues, toothbrush and paste", "Sanitary pads, bin bags and zip bags"]),
        ("#bfbfbf", "Top of the bag · light, power, signal", ["Wind-up and solar radio with torch and USB power bank", "Head torch, batteries fitted", "Whistle", "2 glow sticks"]),
        ("#7a7a7a", "Front pocket · tools and documents", ["Multi-tool, UK-legal non-locking blade", "Mini duct tape, 10 m paracord, cable ties", "Waterproof document pouch, pen and notepad", "Contents card and first-hour card"]),
    ],
    you_add="What you add: your medicines, copies of important documents, some cash, a phone charger cable, a change of clothes and anything you can't be without for three days.",
    bag_rows=[("Bag", "Plain black 30-litre rucksack"), ("Straps", "Padded, adjustable, with grab handle"), ("Pockets", "Main compartment, front zip pocket, side mesh pockets"),
              ("Keeping dry", "Roll-top liner inside, plus three roll-top dry bags"), ("Packed weight", "About 5.5 kg"), ("Packed", "By hand in the UK, each bag checked against its contents card")],
    rotation=[("Water pouches", "5 years; we email you"), ("Ration bars", "5 years; we email you"), ("Batteries", "Check every year; we remind you"), ("Hand warmers and glow sticks", "Replace every 3 to 4 years"), ("First aid kit", "Check dates every year")],
    faq=[
        ("Is the bag waterproof?", "The kit stays dry. The rucksack fabric sheds rain, and inside it everything sits in a roll-top waterproof liner, with the food, warmth and first aid each in their own roll-top dry bag. Don't submerge it."),
        ("Who is it for?", "One adult for 72 hours. Buy one per adult in the house. Bags for children, babies, families and pets are coming in 2027."),
        ("How is this different from the Operator range?", "The Standard Issue is our launch bag: a plain rucksack packed with a complete 72-hour kit. The Operator range, coming in 2027, adds our own purpose-built bags, colour-coded per person, that clip together."),
        ("How long does it last?", "The water and the ration bars keep for five years. Sign up when you order and we email you when anything is due to be replaced."),
        ("Is there enough water?", "No bag can carry three days of water for drinking and washing: that's about 9 litres. The Standard Issue carries 1.5 litres plus a bottle and purification tablets so you can make more safe water as you go."),
        ("When will it arrive?", "Packed and dispatched within three working days. UK delivery is free and tracked."),
    ],
)

def standard_bag_svg(h="420px", label="Blackout SOS Standard Issue go bag"):
    return f'''<svg viewBox="0 0 300 380" style="height:{h};width:auto;max-width:100%" role="img" aria-label="{label}">
<rect x="70" y="18" width="160" height="28" rx="14" fill="none" stroke="#2a2a2a" stroke-width="10"/>
<rect x="40" y="40" width="220" height="320" rx="48" fill="#141414" stroke="#2c2c2c" stroke-width="2"/>
<path d="M54 120 Q150 92 246 120" fill="none" stroke="#333" stroke-width="2" stroke-dasharray="3 4"/>
<rect x="78" y="180" width="144" height="140" rx="22" fill="#101010" stroke="#2e2e2e" stroke-width="2"/>
<path d="M90 194 H210" stroke="#3a3a3a" stroke-width="2" stroke-dasharray="3 4"/>
<rect x="196" y="190" width="8" height="18" rx="2" fill="#2a2a2a"/>
<rect x="20" y="210" width="34" height="120" rx="10" fill="#161616" stroke="#2c2c2c" stroke-width="2"/>
<path d="M22 222 H52 M22 236 H52 M22 250 H52 M22 264 H52 M22 278 H52 M22 292 H52 M22 306 H52" stroke="#262626" stroke-width="1.5"/>
<rect x="26" y="150" width="22" height="70" rx="8" fill="#0d0d0d" stroke="#333" stroke-width="1.5"/>
<rect x="246" y="210" width="34" height="120" rx="10" fill="#161616" stroke="#2c2c2c" stroke-width="2"/>
<path d="M248 222 H278 M248 236 H278 M248 250 H278 M248 264 H278 M248 278 H278 M248 292 H278 M248 306 H278" stroke="#262626" stroke-width="1.5"/>
<path d="M120 46 Q132 30 150 30 Q168 30 180 46" fill="none" stroke="#e06a2a" stroke-width="6" stroke-linecap="round" opacity=".85"/>
<rect x="96" y="352" width="108" height="10" rx="5" fill="#000" opacity=".5"/>
</svg>'''

def si_card(r):
    b = SI
    buy = f'<button type="button" class="pill solid" data-add="{b["sku"]}" style="flex:1 1 auto">Add to basket</button>'
    cta = (f'<span data-avail="{b["sku"]}" data-when="in" hidden style="display:contents">{buy}</span>'
           f'<a data-avail="{b["sku"]}" data-when="out" class="pill" href="{r}bags/standard-issue.html#notify" style="flex:1 1 auto">Sold out · Notify me</a>')
    return cta

def build_standard(page, px, gbp, SITE, subscribe_form, hero_extra=""):
    """Writes the homepage, the Standard Issue product page and redirect stubs for the range pages."""
    b = SI
    groups = "".join(f'<div class="card" style="flex:1 1 240px;padding:24px;gap:14px"><div style="display:flex;align-items:center;gap:10px"><span class="tag" style="width:14px;height:14px;background:{c};{"border:1px solid #3a3a3a" if c=="#2a2a2a" else ""}"></span><span class="eyebrow" style="letter-spacing:2px">{t}</span></div><p class="items" style="font-size:15px">{"<br>".join(i)}</p></div>' for c, t, i in b["groups"])
    count = sum(len(i) for _, _, i in b["groups"])
    rows = lambda rs: "".join(f'<div class="row"><span>{k}</span><span>{v}</span></div>' for k, v in rs)
    faq = "".join(f'<div class="faq"><p>{q}</p><p class="p small">{a}</p></div>' for q, a in b["faq"])
    features = [("<circle cx=\"12\" cy=\"12\" r=\"9\"/><path d=\"M3 12h18M12 3c2.5 2.6 3.8 5.6 3.8 9s-1.3 6.4-3.8 9c-2.5-2.6-3.8-5.6-3.8-9S9.5 5.6 12 3z\"/>", "Packed in the UK", "By hand, checked item by item"),
                ("<path d=\"M12 3s6 6.4 6 11a6 6 0 0 1-12 0c0-4.6 6-11 6-11z\"/><path d=\"M9.5 14.5a2.5 2.5 0 0 0 2.5 2.5\"/>", "Contents stay dry", "Roll-top liner and dry bags"),
                ("<circle cx=\"12\" cy=\"13\" r=\"8\"/><path d=\"M12 9v4l2.5 2.5M9 2h6\"/>", "Food and water", "5-year shelf life"),
                ("<path d=\"M9 18h6M10 21h4M12 3a6 6 0 0 0-4 10.5V16h8v-2.5A6 6 0 0 0 12 3z\"/>", "Light, radio, power", "Wind-up, no mains needed"),
                ("<path d=\"M12 4v16M4 12h16\"/><rect x=\"3\" y=\"3\" width=\"18\" height=\"18\" rx=\"3\"/>", "First aid included", "Plus hygiene and tools"),
                ("<path d=\"M6 16V11a6 6 0 0 1 12 0v5l2 2H4l2-2z\"/><path d=\"M10 20a2 2 0 0 0 4 0\"/>", "Reminders when it's time", "We email before anything expires")]
    feat = '<section class="features" aria-label="Why the Standard Issue"><ul>' + "".join(f'<li><svg viewBox="0 0 24 24" aria-hidden="true">{p}</svg><b>{t}</b><span>{d}</span></li>' for p, t, d in features) + '</ul></section>'
    product_schema = json.dumps({"@context": "https://schema.org", "@type": "Product", "name": "Blackout SOS Standard Issue go bag", "description": b["lede"], "brand": {"@type": "Brand", "name": "Blackout SOS"},
                                 "offers": {"@type": "Offer", "priceCurrency": "GBP", "price": f"{b['price']/100:.2f}", "availability": "https://schema.org/InStock", "url": f"{SITE}/bags/standard-issue.html"}})

    # ---- HOME ----
    r = ""
    hero = f"""
<section class="si-hero" aria-label="The Standard Issue go bag">
<img class="si-bg" src="assets/standard-issue.jpg" srcset="assets/standard-issue-1000.jpg 1000w, assets/standard-issue.jpg 1536w" sizes="100vw" width="1536" height="1024" alt="The Blackout SOS Standard Issue: a plain black rucksack with its contents laid out beside it" fetchpriority="high">
<div class="wrap si-hero-in">
<div class="stack si-copy">
<p class="morse" aria-label="S O S: three dots, three dashes, three days"><span class="m-d"></span><span class="m-d"></span><span class="m-d"></span><span class="m-l"></span><span class="m-l"></span><span class="m-l"></span><span class="m-d"></span><span class="m-d"></span><span class="m-d"></span><span class="m-t">Three dots · three dashes · three days</span></p>
<h1 class="h1">Standard Issue.<br>72 hours, packed and ready.</h1>
<p class="lede">One plain black rucksack with everything an adult needs to get through a power cut, flood or evacuation: water, food, warmth, first aid, light and a radio. Kept dry inside, packed by hand in the UK.</p>
<div style="display:flex;align-items:baseline;gap:14px;flex-wrap:wrap"><span class="price">{px(b['price'])}</span><span class="muted small" data-ship-line-hero>Free UK delivery. Dispatched in three working days.</span></div>
<div class="hero-ctas">{si_card(r)}<a class="pill" href="bags/standard-issue.html#inside">What's inside</a></div>
</div>
</div>
</section>"""
    body = f"""{hero}
{feat}
<section id="inside" class="section"><div class="wrap stack" style="gap:40px">
<div style="display:flex;flex-wrap:wrap;justify-content:space-between;align-items:flex-end;gap:16px">
<div class="stack" style="gap:10px"><p class="eyebrow">What's inside</p><h2 class="h2">{count} items. Nothing to think about.</h2></div>
<p class="p" style="max-width:440px">Three colour-coded dry bags inside a roll-top liner: green for water and food, black for warmth, red for first aid. Light, radio and tools on top, where your hand finds them.</p>
</div>
<div class="grid">{groups}</div>
<p class="p" style="max-width:760px">{b['you_add']}</p>
</div></section>
<section class="section band"><div class="wrap stack" style="gap:40px">
<div class="grid" style="border-top:1px solid var(--line2);border-bottom:1px solid var(--line2);padding:32px 0">
<div class="stat"><span class="n">72</span><span class="l">hours covered</span></div>
<div class="stat"><span class="n">{count}</span><span class="l">items, packed and checked</span></div>
<div class="stat"><span class="n">5.5 kg</span><span class="l">packed, about</span></div>
<div class="stat"><span class="n">5 yrs</span><span class="l">water and food shelf life</span></div>
</div>
<div class="split">
<div class="stack" style="flex:1 1 360px;gap:14px"><p class="eyebrow">Why have one</p><h2 class="h2">Three days, ready by the door.</h2><p class="p">Governments now ask every household to be able to manage for three days on its own. Most people never get round to building a kit. The Standard Issue is the whole list, done, in one bag you can grab in the dark.</p><a class="pill solid" href="bags/standard-issue.html" style="align-self:flex-start;height:50px">See the Standard Issue</a></div>
<div class="rows" style="flex:1 1 420px">{rows(b['bag_rows'])}</div>
</div>
</div></section>
<section class="section light"><div class="wrap stack" style="gap:40px">
<div style="display:flex;flex-wrap:wrap;justify-content:space-between;align-items:flex-end;gap:16px">
<div class="stack" style="gap:10px"><p class="eyebrow">Guides</p><h2 class="h2">Know what to do before you need to.</h2></div>
<a href="guides/index.html" style="font-weight:600;font-size:15px;border-bottom:2px solid var(--bg);padding-bottom:2px">All guides →</a>
</div>
<div class="grid">
<a class="card dark" href="guides/power-cut-the-first-hour.html" style="flex:2 1 420px;padding:32px;justify-content:space-between;gap:48px;min-height:300px"><span class="eyebrow">Featured · 6 min read</span><span class="stack"><span class="display" style="font-size:44px">Power cut: the first hour</span><span class="p" style="color:#b5b5b5">What to do in the first five minutes, the first thirty, and the first hour.</span></span></a>
<a class="card" href="guides/the-72-hour-list-explained.html" style="flex:1 1 260px;justify-content:space-between;gap:32px"><span class="eyebrow">Checklist</span><span class="stack" style="gap:10px"><span class="display" style="font-size:30px">The 72-hour list, explained</span><span class="p small">Line by line: what three days actually takes.</span></span></a>
<a class="card" href="guides/flooding-before-during-after.html" style="flex:1 1 260px;justify-content:space-between;gap:32px"><span class="eyebrow">Flooding</span><span class="stack" style="gap:10px"><span class="display" style="font-size:30px">Before, during, after</span><span class="p small">What to move, what to switch off, when to leave.</span></span></a>
</div>
</div></section>
<section class="section"><div class="wrap grid">
<div class="card" style="flex:1 1 420px;padding:40px;gap:18px"><p class="eyebrow">Coming 2027</p><h3 class="h3">A bag for every person in your house.</h3><p class="p">Our own purpose-built range is on its way: bags for adults, children, babies, families and pets, colour-coded per person, with the smaller bags clipping onto the adult's. Join the list to hear first.</p>
<form class="form-row" data-api="/subscribe"><input type="hidden" name="source" value="range-2027"><label class="sr" for="email-range">Email address</label><input id="email-range" name="email" type="email" required placeholder="you@example.com" style="flex:1 1 220px"><button type="submit" class="pill solid">Join the list</button><p class="p small ok" data-done hidden style="flex:1 1 100%">You're on the list. We'll email you when the range launches.</p></form></div>
<div class="card" style="flex:1 1 420px;padding:40px;gap:18px"><p class="eyebrow">For organisations</p><h3 class="h3">One bag per desk, per room, per person.</h3><p class="p">Workplaces, schools, hotels and property managers buy the Standard Issue in tens and hundreds, with volume pricing, invoice terms and reminders when contents are due.</p><a href="organisations.html" style="align-self:flex-start;font-weight:600;font-size:15px;border-bottom:1px solid var(--ink);padding-bottom:2px">Request a quote</a></div>
</div></section>
<section class="section tight" style="border-top:1px solid var(--line)"><div class="wrap" style="display:flex;flex-wrap:wrap;gap:32px;align-items:center;justify-content:space-between">
<div class="stack" style="flex:1 1 420px;gap:10px"><h3 class="h3">Be Ready alerts</h3><p class="p">When a storm, a cold snap or an official warning is coming, we send one short message with what to check. No marketing, no noise.</p></div>
{subscribe_form(r, 'home')}
</div></section>
"""
    org = json.dumps({"@context": "https://schema.org", "@type": "Organization", "name": "Blackout SOS", "url": SITE, "description": "72-hour go bags packed in the UK.", "contactPoint": {"@type": "ContactPoint", "email": "hello@blackoutsos.com", "contactType": "customer service", "areaServed": "GB"}})
    page("index.html", "Blackout SOS Standard Issue — 72-hour go bag, packed in the UK", "The Standard Issue: a plain black rucksack packed with everything one adult needs for 72 hours: water, food, warmth, first aid, light and radio. £139, free UK delivery.", body,
         f'<script type="application/ld+json">{org}</script><script type="application/ld+json">{product_schema}</script>')

    # ---- PRODUCT ----
    r = "../"
    pbody = f"""
<div class="wrap crumbs" style="padding-top:24px"><a href="../index.html">Home</a><span>/</span><span class="here">Standard Issue</span></div>
<section class="wrap split" style="padding-top:32px;padding-bottom:clamp(56px,7vw,96px)">
<div class="stack" style="flex:1 1 520px;gap:14px"><img class="si-product" src="../assets/standard-issue.jpg" srcset="../assets/standard-issue-1000.jpg 1000w, ../assets/standard-issue.jpg 1536w" sizes="(max-width:760px) 100vw, 55vw" width="1536" height="1024" alt="The Blackout SOS Standard Issue go bag with its contents laid out beside it"></div>
<div class="stack" style="flex:1 1 420px;gap:24px">
<div class="stack" style="gap:10px"><div class="eyebrow">{b['who']}</div><h1 class="h1" style="font-size:clamp(52px,6.5vw,88px)">Standard Issue</h1><p class="lede" style="font-size:17px">{b['lede']}</p></div>
<div class="muted small" style="display:flex;flex-wrap:wrap;gap:8px 24px;border-top:1px solid var(--line);border-bottom:1px solid var(--line);padding:14px 0">{"".join(f"<span>{s}</span>" for s in b["specs"])}</div>
<div style="display:flex;align-items:baseline;gap:14px;flex-wrap:wrap"><span class="price">{px(b['price'])}</span><span class="muted small" data-ship-line>free UK delivery · ships worldwide</span></div>
<form class="stack" style="gap:14px" data-product="{b['sku']}">
<div data-avail="{b['sku']}" data-when="in" hidden style="display:contents">
<button type="submit" class="pill solid" style="height:58px;font-size:16px">Add to basket &nbsp;—&nbsp;{px(b['price'])}</button>
<p class="p small">Packed by hand and dispatched within three working days. Write-on name card included.</p>
</div>
</form>
<div id="notify" data-avail="{b['sku']}" data-when="out" class="card stack" style="gap:12px;padding:22px">
<p class="eyebrow">Sold out for now</p>
<p class="p">We're packing the next batch. Leave your email and you'll hear the day it's back.</p>
<form class="form-row" data-api="/subscribe"><input type="hidden" name="source" value="waitlist"><input type="hidden" name="bag" value="Standard Issue"><label class="sr" for="notify-email">Email address</label><input id="notify-email" name="email" type="email" required placeholder="you@example.com" style="flex:1 1 220px"><button type="submit" class="pill solid">Notify me</button><p class="p small ok" data-done hidden style="flex:1 1 100%">You're on the list. We'll email you when it's back.</p></form>
</div>
<div class="anchor-list" style="border-top:1px solid var(--line)"><a href="#inside"><span>What's inside</span><span>{count} items</span></a><a href="#build"><span>The bag</span><span>Size and build</span></a><a href="#rotation"><span>Rotation dates</span><span>5 years</span></a><a href="#faq"><span>Questions</span><span>Straight answers</span></a></div>
</div>
</section>
<section id="inside" class="section band"><div class="wrap stack" style="gap:36px">
<div class="stack" style="gap:10px"><p class="eyebrow">What's inside</p><h2 class="h2">{count} items, packed by hand.</h2></div>
<div class="grid">{groups}</div>
<p class="p" style="max-width:760px">{b['you_add']}</p>
</div></section>
<section id="build" class="section"><div class="wrap split">
<div class="stack" style="flex:1 1 360px;gap:14px"><p class="eyebrow">The bag</p><h2 class="h2">Plain on the outside. Dry on the inside.</h2><p class="p">A plain black rucksack that doesn't look like an emergency kit, with a roll-top waterproof liner inside and the kit split into three roll-top dry bags, so rain and spills stay out.</p></div>
<div class="rows" style="flex:2 1 520px">{rows(b['bag_rows'])}</div>
</div></section>
<section id="rotation" class="section band"><div class="wrap split">
<div class="stack" style="flex:1 1 360px;gap:14px"><p class="eyebrow">Rotation dates</p><h2 class="h2">Buy it once. We'll tell you when.</h2><p class="p">We remember when you bought it. When something is due, we email you exactly what to swap and nothing else.</p></div>
<div class="rows" style="flex:1 1 420px">{rows(b['rotation'])}</div>
</div></section>
<section id="faq" class="section"><div class="wrap split">
<div style="flex:1 1 300px"><p class="eyebrow" style="margin-bottom:10px">Questions</p><h2 class="h2">Straight answers.</h2></div>
<div style="flex:2 1 560px;display:flex;flex-direction:column">{faq}</div>
</div></section>
"""
    page("bags/standard-issue.html", "Standard Issue 72-hour go bag — Blackout SOS", "Everything one adult needs for 72 hours, packed in a plain black 30-litre rucksack with the contents kept dry. £139, free UK delivery.", pbody, f'<script type="application/ld+json">{product_schema}</script>')

def write_redirects(write, SITE):
    for p in ["bags/index.html", "bags/operator.html", "bags/recruit.html", "bags/cub.html", "bags/unit.html", "bags/scout.html", "refills.html"]:
        depth = "../" if p.startswith("bags/") else ""
        target = "standard-issue.html" if p.startswith("bags/") else "bags/standard-issue.html"
        write(p, f'<!doctype html><html lang="en-GB"><head><meta charset="utf-8"><title>Blackout SOS Standard Issue</title><meta name="robots" content="noindex"><link rel="canonical" href="{SITE}/bags/standard-issue.html"><meta http-equiv="refresh" content="0; url={target}"></head><body><p><a href="{target}">The Standard Issue go bag</a></p></body></html>\n')

SI_CSS = """
.si-hero{position:relative;overflow:hidden;background:#050505;border-bottom:1px solid var(--line)}
.si-bg{position:absolute;top:0;right:0;width:72%;height:100%;object-fit:cover;object-position:75% center}
.si-hero::after{content:"";position:absolute;inset:0;background:linear-gradient(90deg,#050505 0%,#050505 36%,rgba(5,5,5,0) 54%);pointer-events:none}
.si-hero-in{position:relative;z-index:1;min-height:clamp(560px,52vw,760px);display:flex;align-items:center;padding-top:48px;padding-bottom:48px}
.si-copy{max-width:520px;gap:20px}
.si-copy .h1{font-size:clamp(40px,4.6vw,68px)}
.si-copy .lede{font-size:17px;color:var(--ink)}
.si-product{display:block;width:100%;height:auto;border-radius:16px;border:1px solid var(--line)}
@media(max-width:860px){.si-bg{position:static;display:block;width:100%;height:auto;aspect-ratio:3/2;object-position:62% center}.si-hero::after{display:none}.si-hero-in{min-height:0;padding-top:28px;padding-bottom:40px}.si-copy .h1{font-size:clamp(40px,11vw,60px)}}
"""

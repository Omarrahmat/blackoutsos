# The storefront hero: the five bags on a studio floor, names and prices, shop-first copy.
# A real photograph dropped in at assets/hero.jpg replaces the drawn lineup automatically.

HERO_CSS = """
.hero{position:relative;background:#050505;overflow:hidden;border-bottom:1px solid var(--line);display:flex;flex-direction:column}
.hero-top{display:flex;flex-wrap:wrap;align-items:flex-end;justify-content:space-between;gap:20px 48px;padding-top:clamp(32px,4vw,48px)}
.hero-top .h1{font-size:clamp(38px,4.6vw,64px);max-width:16ch}
.hero-top .lede{max-width:460px;font-size:16px}
.hero-ctas{display:flex;flex-wrap:wrap;gap:12px;align-items:center}
.hero-trust{display:flex;flex-wrap:wrap;gap:8px 24px;font-size:13px;color:var(--muted)}
.studio{position:relative;margin-top:clamp(20px,2.5vw,32px);background:radial-gradient(120% 90% at 50% 100%,#262626 0%,#121212 45%,#050505 100%)}
.studio::before{content:"";position:absolute;left:0;right:0;top:0;height:40%;background:linear-gradient(180deg,#050505,transparent);pointer-events:none}
.studio-link{display:block;position:relative}
.studio-photo{display:block;width:100%;height:auto;max-height:min(640px,70vh);object-fit:cover;object-position:50% 62%}
.studio-link+.lineup{display:none}
.hero-foot a{display:inline-flex;align-items:center;gap:10px;padding:8px 0}
.hero-foot .nm{font-family:'Barlow Condensed',sans-serif;font-weight:700;font-size:20px;letter-spacing:1px;color:var(--ink)}
.hero-foot .pr{text-transform:none;letter-spacing:0;font-size:13px}
.hero-foot .tag{width:9px;height:9px}
.lineup{position:relative;display:flex;align-items:flex-end;justify-content:center;gap:clamp(8px,2vw,28px);padding:clamp(28px,3.5vw,48px) clamp(16px,4vw,48px) 96px;max-width:1344px;margin:0 auto}
.lineup a{display:flex;flex-direction:column;align-items:center;gap:0;flex:0 1 auto;min-width:0;text-align:center}
.lineup .fig{position:relative;display:block}
.lineup .fig>svg{display:block;height:var(--h);width:auto;filter:brightness(1.35) contrast(1.05) drop-shadow(0 30px 24px rgba(0,0,0,.6))}
.lineup .fig .mirror{position:absolute;left:0;top:100%;display:block;height:var(--h);width:auto;transform:scaleY(-1);opacity:.2;filter:blur(1px);-webkit-mask-image:linear-gradient(180deg,rgba(0,0,0,0) 50%,rgba(0,0,0,.9) 100%);mask-image:linear-gradient(180deg,rgba(0,0,0,0) 50%,rgba(0,0,0,.9) 100%);margin-top:-2px;pointer-events:none}
.lineup .cap{position:absolute;left:50%;top:calc(100% + 16px);transform:translateX(-50%);z-index:2;display:flex;flex-direction:column;align-items:center;gap:6px;white-space:nowrap}
.lineup .cap .nm{display:inline-flex;align-items:center;gap:8px;font-family:'Barlow Condensed',sans-serif;font-weight:700;font-size:clamp(16px,1.6vw,24px);text-transform:uppercase;letter-spacing:1px}
.lineup .cap .pr{font-size:13px;color:var(--muted)}
.lineup .cap .tag{width:9px;height:9px}
.lineup a:hover .cap .pr{color:var(--ink)}
.floor{height:1px;background:linear-gradient(90deg,transparent,#2a2a2a 20%,#2a2a2a 80%,transparent);max-width:1344px;margin:0 auto}
.hero-foot{display:flex;flex-wrap:wrap;justify-content:center;gap:6px 36px;padding:14px clamp(16px,4vw,48px) 20px;font-size:12px;letter-spacing:2px;text-transform:uppercase;color:var(--muted)}
@media(max-width:860px){.lineup{overflow-x:auto;justify-content:flex-start;gap:28px;padding-bottom:84px;scroll-snap-type:x mandatory;scrollbar-width:none}.lineup::-webkit-scrollbar{display:none}.lineup a{scroll-snap-align:center;flex:0 0 auto}.lineup .fig svg,.lineup .fig .mirror{height:calc(var(--h) * .8)}}
@media(max-width:760px){.hero-top .h1{font-size:clamp(44px,12vw,72px)}.studio:has(.studio-link){order:-1;margin-top:0}.studio-photo{max-height:none;height:auto;aspect-ratio:3/2;object-fit:cover;object-position:50% 70%}.hero-top{padding-top:28px}.hero-foot{flex-wrap:nowrap;justify-content:flex-start;overflow-x:auto;gap:22px;padding:10px 16px 14px;scrollbar-width:none}.hero-foot::-webkit-scrollbar{display:none}.hero-foot a{white-space:nowrap}}
"""

def hero_html(r="", art=None, bags=None, gbp=None):
    """art(slug) returns the bag SVG; bags is the content dict; gbp formats pence."""
    heights = {"recruit": "262px", "operator": "340px", "cub": "304px", "unit": "190px", "scout": "262px"}
    order = ["recruit", "operator", "cub", "unit", "scout"]
    items = ""
    for s in order:
        b = bags[s]
        items += f"""<a href="{r}bags/{s}.html" style="--h:{heights[s]}" aria-label="{b['name']}, {b['who']}, {gbp(b['price'])}"><span class="fig">{art(s)}<span class="mirror" aria-hidden="true">{art(s)}</span><span class="cap"><span class="nm"><span class="tag" style="background:{b['colour']}"></span>{b['name']}</span><span class="pr">{b['who']} · {gbp(b['price'])}</span></span></span></a>"""
    strip = "".join(f'<a href="{r}bags/{s2}.html"><span class="tag" style="background:{bags[s2]["colour"]}"></span><span class="nm">{bags[s2]["name"]}</span><span class="pr">{bags[s2]["who"]} · {gbp(bags[s2]["price"])}</span></a>' for s2 in order)
    return f"""
<section class="hero" aria-label="Blackout SOS go bags">
<div class="wrap hero-top">
<div class="stack" style="gap:18px;flex:1 1 520px">
<p class="eyebrow">Three dots · three dashes · three days</p>
<h1 class="h1">A 72-hour go bag for every person in your house.</h1>
</div>
<div class="stack" style="gap:18px;flex:0 1 420px">
<p class="lede">Five bags, one colour each, from £89. Packed in the UK with 15-year rations, waterproof, vegan and made without nuts. Free UK delivery, dispatched in three working days.</p>
<div class="hero-ctas"><a class="pill solid" href="{r}bags/index.html">Shop the range</a><a class="pill" href="{r}bags/operator.html">The Operator, £199</a></div>
</div>
</div>
<div class="studio">
<a href="{r}bags/index.html" class="studio-link"><img class="studio-photo" src="{r}assets/hero.jpg" srcset="{r}assets/hero-1000.jpg 1000w, {r}assets/hero.jpg 1536w" sizes="100vw" width="1536" height="1024" alt="The Blackout SOS range: Recruit, Operator, Cub, Unit and Scout go bags on a dark studio floor" fetchpriority="high" onerror="this.parentNode.remove()"></a>
<div class="lineup">{items}</div>
<div class="floor"></div>
<div class="hero-foot">{strip}</div>
</div>
</section>
"""

# The widescreen hero: a night scene drawn in SVG (torch beam, rain, the Operator with reflective piping),
# with a drop-in slot for a real photograph at assets/hero.jpg.

HERO_CSS = """
.hero{position:relative;min-height:84vh;display:flex;align-items:center;overflow:hidden;background:#050505;isolation:isolate}
.hero-scene{position:absolute;inset:0;z-index:0}
.hero-scene svg{width:100%;height:100%;display:block}
.hero-photo{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;object-position:70% 50%;z-index:1;opacity:.92}
.hero-shade{position:absolute;inset:0;z-index:2;background:linear-gradient(90deg,rgba(5,5,5,.92) 0%,rgba(5,5,5,.78) 34%,rgba(5,5,5,.12) 62%,rgba(5,5,5,0) 100%),linear-gradient(180deg,rgba(5,5,5,.35) 0%,rgba(5,5,5,0) 30%,rgba(5,5,5,0) 70%,rgba(5,5,5,.9) 100%)}
.hero-copy{position:relative;z-index:3;width:100%;display:flex;flex-direction:column;gap:28px;padding:clamp(56px,7vw,100px) clamp(16px,6vw,96px) clamp(88px,8vw,110px);max-width:1400px;margin:0}
.hero-copy .h1{font-size:clamp(56px,8vw,128px);max-width:13ch;text-shadow:0 2px 24px rgba(0,0,0,.6)}
.hero-copy .lede{max-width:540px;text-shadow:0 1px 12px rgba(0,0,0,.6)}
.hero-cue{position:absolute;left:50%;bottom:22px;transform:translateX(-50%);z-index:3;display:flex;flex-direction:column;align-items:center;gap:8px;font-size:11px;letter-spacing:3px;text-transform:uppercase;color:var(--muted)}
.hero-cue i{display:block;width:1px;height:36px;background:linear-gradient(180deg,var(--muted),transparent)}
.hero-morse{position:absolute;right:clamp(16px,4vw,48px);top:28px;z-index:3;display:flex;align-items:center;gap:4px;opacity:.5}
.hero-morse i{display:block;height:5px;width:5px;background:#ededed;border-radius:1px}.hero-morse i.l{width:15px}.hero-morse b{display:block;width:6px}
@media(prefers-reduced-motion:no-preference){.rain{animation:rain 1.6s linear infinite}@keyframes rain{from{transform:translateY(-120px)}to{transform:translateY(0)}}.beam{animation:flicker 9s ease-in-out infinite}@keyframes flicker{0%,100%{opacity:1}47%{opacity:.86}52%{opacity:.98}}}
@media(max-width:760px){.hero{min-height:0;flex-direction:column;align-items:stretch}.hero-scene{position:relative;height:460px;order:2}.hero-photo{position:absolute}.hero-shade{background:linear-gradient(180deg,rgba(5,5,5,0) 0%,rgba(5,5,5,0) 55%,rgba(5,5,5,.95) 100%)}.hero-copy{padding:56px 16px 24px}.hero-copy .h1{font-size:clamp(56px,16vw,96px)}.hero-cue{display:none}}
"""

def hero_scene():
    # 1600 x 900 scene. The bag sits right of centre so it survives a centre crop on phones.
    bag = """
<g id="bag" transform="translate(950 250) scale(1.15)">
 <ellipse cx="200" cy="520" rx="210" ry="22" fill="#000" opacity=".65" filter="url(#soft)"/>
 <path d="M150 66 C150 34 250 34 250 66" fill="none" stroke="#2a2a2a" stroke-width="13" stroke-linecap="round"/>
 <path d="M150 66 C150 34 250 34 250 66" fill="none" stroke="#5a5a5a" stroke-width="3" stroke-linecap="round" opacity=".8"/>
 <rect x="60" y="60" width="280" height="430" rx="56" fill="url(#body)" stroke="#303030" stroke-width="2"/>
 <path d="M70 140 Q70 76 200 72 Q330 76 330 140" fill="none" stroke="#3a3a3a" stroke-width="4" stroke-dasharray="2 3"/>
 <path d="M96 62 Q60 110 62 200 L62 470 Q62 488 80 490" fill="none" stroke="url(#pipeL)" stroke-width="2.5" opacity=".55"/>
 <path d="M304 62 Q340 110 338 200 L338 470 Q338 488 320 490" fill="none" stroke="#f2f2f2" stroke-width="3" filter="url(#glow)" opacity=".95"/>
 <path d="M100 182 Q100 180 130 180 L270 180 Q300 180 300 210 L300 400 Q300 430 270 430 L130 430 Q100 430 100 400 Z" fill="url(#panel)" stroke="#2c2c2c" stroke-width="2"/>
 <path d="M300 210 L300 400 Q300 430 270 430" fill="none" stroke="#f2f2f2" stroke-width="2.5" filter="url(#glow)" opacity=".9"/>
 <rect x="156" y="96" width="88" height="32" rx="7" fill="#0f0f0f" stroke="#3a3a3a" stroke-width="1.5"/>
 <rect x="163" y="103" width="74" height="18" rx="3" fill="#e9e6dc" opacity=".92"/>
 <rect x="170" y="108" width="40" height="2" fill="#777" opacity=".8"/><rect x="170" y="114" width="56" height="2" fill="#777" opacity=".6"/>
 <rect x="296" y="110" width="7" height="26" rx="2" fill="#1F5FBF"/>
 <rect x="336" y="172" width="11" height="32" rx="2" fill="#1F5FBF"/>
 <rect x="62" y="204" width="36" height="176" rx="15" fill="#141414" stroke="#2a2a2a" stroke-width="2"/>
 <rect x="72" y="178" width="16" height="30" rx="5" fill="#1b1b1b" stroke="#2a2a2a"/>
 <g fill="#070707"><rect x="312" y="200" width="14" height="6" rx="2"/><rect x="312" y="210" width="14" height="6" rx="2"/><rect x="312" y="220" width="14" height="6" rx="2"/><rect x="312" y="236" width="14" height="16" rx="2"/><rect x="312" y="256" width="14" height="16" rx="2"/><rect x="312" y="276" width="14" height="16" rx="2"/><rect x="312" y="302" width="14" height="6" rx="2"/><rect x="312" y="312" width="14" height="6" rx="2"/><rect x="312" y="322" width="14" height="6" rx="2"/></g>
 <rect x="150" y="224" width="100" height="56" rx="6" fill="#1f1f1f" stroke="#2a2a2a"/>
 <text x="200" y="350" text-anchor="middle" fill="#3c3c3c" font-size="16" letter-spacing="4" font-family="Barlow Condensed, sans-serif" font-weight="700">BLACKOUT SOS</text>
 <g fill="#3c3c3c"><rect x="151" y="359" width="4" height="4" rx="1"/><rect x="158" y="359" width="4" height="4" rx="1"/><rect x="165" y="359" width="4" height="4" rx="1"/><rect x="179" y="359" width="12" height="4" rx="1"/><rect x="194" y="359" width="12" height="4" rx="1"/><rect x="209" y="359" width="12" height="4" rx="1"/><rect x="231" y="359" width="4" height="4" rx="1"/><rect x="238" y="359" width="4" height="4" rx="1"/><rect x="245" y="359" width="4" height="4" rx="1"/></g>
 <path d="M92 472 Q200 486 308 472" fill="none" stroke="#2a2a2a" stroke-width="2"/>
 <path d="M60 300 Q60 470 90 486" fill="none" stroke="#000" stroke-width="18" opacity=".35" filter="url(#soft)"/>
</g>"""
    return f"""<svg viewBox="0 0 1600 900" preserveAspectRatio="xMaxYMid slice" role="img" aria-label="Night scene: the Operator go bag lit by a torch beam in the rain, its reflective piping catching the light">
<defs>
 <linearGradient id="sky" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#0c0c0d"/><stop offset="1" stop-color="#040404"/></linearGradient>
 <linearGradient id="beam" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#dfe6ee" stop-opacity=".30"/><stop offset=".55" stop-color="#cfd6de" stop-opacity=".10"/><stop offset="1" stop-color="#cfd6de" stop-opacity="0"/></linearGradient>
 <radialGradient id="pool" cx=".5" cy=".5" r=".5"><stop offset="0" stop-color="#d9dee5" stop-opacity=".28"/><stop offset="1" stop-color="#d9dee5" stop-opacity="0"/></radialGradient>
 <radialGradient id="fog" cx=".5" cy=".5" r=".5"><stop offset="0" stop-color="#9aa3ad" stop-opacity=".16"/><stop offset="1" stop-color="#9aa3ad" stop-opacity="0"/></radialGradient>
 <linearGradient id="body" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#101010"/><stop offset=".55" stop-color="#171717"/><stop offset="1" stop-color="#262626"/></linearGradient>
 <linearGradient id="panel" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#0f0f0f"/><stop offset="1" stop-color="#1e1e1e"/></linearGradient>
 <linearGradient id="pipeL" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#6b6b6b"/><stop offset="1" stop-color="#2a2a2a"/></linearGradient>
 <filter id="glow" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="2.2" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
 <filter id="soft" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="14"/></filter>
 <filter id="blur40" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="40"/></filter>
 <filter id="grain"><feTurbulence type="fractalNoise" baseFrequency=".9" numOctaves="2" stitchTiles="stitch"/><feColorMatrix values="0 0 0 0 0.5 0 0 0 0 0.5 0 0 0 0 0.5 0 0 0 .55 0"/></filter>
 <pattern id="rainp" width="140" height="120" patternUnits="userSpaceOnUse" patternTransform="rotate(12)"><g stroke="#ffffff" stroke-width="1.1" stroke-linecap="round" opacity=".55"><line x1="10" y1="0" x2="10" y2="26"/><line x1="48" y1="40" x2="48" y2="58"/><line x1="92" y1="10" x2="92" y2="42"/><line x1="124" y1="66" x2="124" y2="88"/><line x1="30" y1="84" x2="30" y2="104"/><line x1="70" y1="96" x2="70" y2="118"/><line x1="110" y1="100" x2="110" y2="112"/></g></pattern>
 <clipPath id="cone"><polygon points="1250,-120 1450,-120 1700,900 680,900"/></clipPath>
</defs>
<rect width="1600" height="900" fill="url(#sky)"/>
<g class="beam"><polygon points="1300,-160 1400,-160 1700,900 700,900" fill="url(#beam)"/><ellipse cx="1180" cy="812" rx="520" ry="70" fill="url(#pool)"/></g>
<ellipse cx="1180" cy="660" rx="520" ry="260" fill="url(#fog)" filter="url(#blur40)"/>
<g clip-path="url(#cone)" opacity=".5"><rect class="rain" x="0" y="-120" width="1600" height="1140" fill="url(#rainp)"/></g>
<g opacity=".07" fill="#ededed"><rect x="80" y="800" width="14" height="14" rx="2"/><rect x="104" y="800" width="14" height="14" rx="2"/><rect x="128" y="800" width="14" height="14" rx="2"/><rect x="166" y="800" width="42" height="14" rx="2"/><rect x="218" y="800" width="42" height="14" rx="2"/><rect x="270" y="800" width="42" height="14" rx="2"/><rect x="336" y="800" width="14" height="14" rx="2"/><rect x="360" y="800" width="14" height="14" rx="2"/><rect x="384" y="800" width="14" height="14" rx="2"/></g>
<line x1="0" y1="814" x2="1600" y2="814" stroke="#1a1a1a" stroke-width="1"/>
{bag}
<rect width="1600" height="900" filter="url(#grain)" opacity=".07"/>
</svg>"""

def hero_html(r=""):
    return f"""
<section class="hero" aria-label="Blackout SOS">
<div class="hero-scene">{hero_scene()}</div>
<img class="hero-photo" src="{r}assets/hero.jpg" alt="" onerror="this.remove()">
<div class="hero-shade"></div>
<div class="hero-morse" aria-hidden="true"><i></i><i></i><i></i><b></b><i class="l"></i><i class="l"></i><i class="l"></i><b></b><i></i><i></i><i></i></div>
<div class="hero-copy">
<p class="eyebrow">72-hour go bags · assembled in the UK</p>
<h1 class="h1">Three dots.<br>Three dashes.<br>Three days.</h1>
<p class="lede">A go bag for every person in your house, packed by people who have done the thinking so you never have to. Plain from a distance. Fully kitted up close. Ready by the door.</p>
<div style="display:flex;flex-wrap:wrap;gap:14px"><a class="pill solid" href="{r}bags/index.html">Shop the range</a><a class="pill" href="{r}guides/the-72-hour-list-explained.html" style="border-color:#5a5a5a">The 72-hour checklist</a></div>
<div class="muted small" style="display:flex;flex-wrap:wrap;gap:10px 28px"><span>Waterproof Cordura</span><span>15-year rations</span><span>Vegan, made without nuts</span><span>Free UK delivery</span></div>
</div>
<div class="hero-cue" aria-hidden="true"><span>The range</span><i></i></div>
</section>
"""

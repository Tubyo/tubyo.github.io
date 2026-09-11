#!/usr/bin/env python3
"""Generate crawlable, localized landing pages without runtime dependencies."""
from pathlib import Path
from html import escape as e
import json
ROOT=Path(__file__).resolve().parents[1]
DOC=ROOT/'docs'
DATA=json.loads((ROOT/'content/site.json').read_text())
META=json.loads((ROOT/'content/slides.json').read_text())
ORIGIN='https://tubyo.github.io'
CONTACT='mailto:tubyoapp@gmail.com'
def page(lang):
 d=DATA[lang]; loc=d['locale']; url=f'{ORIGIN}/{lang}/'
 alternates=''.join(f'<link rel="alternate" hreflang="{l}" href="{ORIGIN}/{l}/">' for l in DATA)+f'<link rel="alternate" hreflang="x-default" href="{ORIGIN}/">'
 languages=''.join(f'<a href="/{l}/" lang="{l}" hreflang="{l}"'+(' aria-current="page"' if l==lang else '')+f'>{v["name"]}</a>' for l,v in DATA.items())
 nav=''.join(f'<a href="#{anchor}">{e(label)}</a>' for anchor,label in zip(['experience','gallery','kids','free'],d['nav']))
 icons=['▣','◈','▤','↺']
 cards=''.join(f'<article class="feature"><span class="feature-icon" aria-hidden="true">{icons[i]}</span><h3>{e(t)}</h3><p>{e(body)}</p></article>' for i,(t,body) in enumerate(d['features']))
 slides=''.join(f'''<a class="poster" href="/assets/screens/{loc}/iphone/{key}.webp" data-key="{key}"><img src="/assets/screens/{loc}/iphone/{key}.webp" width="660" height="1434" loading="lazy" decoding="async" alt="{e(title)} — Tubyo · iPhone"><span>{i+1:02d} <b>{e(title)}</b><span aria-hidden="true">↗</span></span></a>''' for i,(key,title,subtitle) in enumerate(META[loc]['slides']))
 faq=''.join(f'<details><summary>{e(q)}<span aria-hidden="true">+</span></summary><p>{e(a)}</p></details>' for q,a in d['faq'])
 points=''.join(f'<li><span aria-hidden="true">✓</span>{e(t)}</li>' for t in d['kidsPoints'])
 schema={'@context':'https://schema.org','@type':'WebSite','name':'Tubyo','url':url,'inLanguage':lang,'description':d['description'],'publisher':{'@type':'Organization','name':'Tubyo','url':ORIGIN,'email':'tubyoapp@gmail.com'}}
 return f'''<!doctype html>
<html lang="{lang}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="description" content="{e(d['description'])}"><meta name="theme-color" content="#0b1715"><meta name="referrer" content="strict-origin-when-cross-origin"><title>{e(d['title'])}</title><link rel="icon" href="/assets/brand.png"><link rel="canonical" href="{url}">{alternates}<meta property="og:type" content="website"><meta property="og:title" content="{e(d['title'])}"><meta property="og:description" content="{e(d['description'])}"><meta property="og:url" content="{url}"><meta property="og:locale" content="{loc.replace('-','_')}"><link rel="stylesheet" href="/assets/landing.css"><script type="application/ld+json">{json.dumps(schema,ensure_ascii=False)}</script><script src="/assets/landing.js" defer></script></head>
<body data-locale="{loc}"><a class="skip" href="#main">{e(d['skip'])}</a><header class="header"><a href="/{lang}/" class="wordmark" aria-label="Tubyo">Tuby<img src="/assets/brand.png" width="36" height="36" alt="o"></a><nav aria-label="Tubyo">{nav}</nav><details class="languages"><summary aria-label="{e(d['language'])}"><span aria-hidden="true">◎</span> {lang.upper()} <span aria-hidden="true">⌄</span></summary><div>{languages}</div></details></header>
<main id="main"><section class="hero wrap"><div class="hero-copy"><p class="eyebrow">{d['eyebrow']}</p><h1>{d['headline']}</h1><p class="intro">{e(d['intro'])}</p><p class="free-line"><span aria-hidden="true">✓</span> {e(d['free'])}</p><div class="cta-row"><a class="button" href="#gallery">{e(d['discover'])}<span aria-hidden="true">↗</span></a><a class="text-link" href="{CONTACT}">{e(d['contact'])}</a></div><div class="stores"><span>{e(d['apple'])}</span><span>{e(d['android'])}</span></div></div><div class="hero-art"><div class="orbit" aria-hidden="true"></div><img class="phone phone-back" src="/assets/screens/{loc}/hero-youtube.webp" width="390" height="844" alt="{e(META[loc]['slides'][2][1])}" decoding="async"><img class="phone phone-front" src="/assets/screens/{loc}/hero-home.webp" width="390" height="844" alt="{e(META[loc]['slides'][0][1])}" fetchpriority="high"></div></section>
<div class="platform-strip wrap"><span>{e(d['platforms'])}</span><div>YouTube <i>·</i> Twitch <i>·</i> TikTok <i>·</i> Instagram</div></div>
<section id="experience" class="section wrap"><p class="eyebrow">TUBYO</p><h2>{d['featuresTitle']}</h2><div class="features">{cards}</div></section>
<section id="gallery" class="gallery-section"><div class="wrap gallery-heading"><div><p class="eyebrow">IPHONE & IPAD</p><h2>{e(d['galleryTitle'])}</h2><p>{e(d['galleryText'])}</p></div><div class="device-switch" role="group" aria-label="iPhone / iPad"><button type="button" data-device="iphone" aria-pressed="true">iPhone</button><button type="button" data-device="ipad" aria-pressed="false">iPad</button></div></div><div class="posters wrap">{slides}</div></section>
<section id="kids" class="kids section wrap"><div class="kids-art"><img src="/assets/screens/{loc}/ipad/kids.webp" width="800" height="1067" loading="lazy" decoding="async" alt="{e(META[loc]['slides'][6][1])}"></div><div><span class="kids-word" aria-label="Kids"><b>k</b><b>i</b><b>d</b><b>s</b></span><p class="eyebrow">{e(d['kidsTag'])}</p><h2>{d['kidsTitle']}</h2><p class="intro">{e(d['kidsText'])}</p><ul class="checks">{points}</ul></div></section>
<section id="free" class="pricing section wrap"><div><p class="eyebrow">{e(d['priceTag'])}</p><h2>{d['priceTitle']}</h2><p class="intro">{e(d['priceText'])}</p></div><div class="price-card"><div class="zero">0<span>€</span></div><h3>{e(d['free'])}</h3><div class="divider"></div><h4>{e(d['optional'])}</h4><p>{e(d['optionalText'])}</p></div></section>
<section class="faq section wrap"><h2>{e(d['faqTitle'])}</h2><div>{faq}</div></section><section class="closing wrap"><p class="eyebrow">TUBYO</p><h2>{d['endTitle']}</h2><a class="button" href="{CONTACT}">{e(d['contact'])}<span aria-hidden="true">↗</span></a><p>{e(d['apple'])} · {e(d['android'])}</p></section></main>
<footer class="wrap"><div class="footer-top"><a href="/{lang}/" class="wordmark" aria-label="Tubyo">Tuby<img src="/assets/brand.png" width="36" height="36" alt="o"></a><a href="{CONTACT}">tubyoapp@gmail.com</a></div><div class="footer-bottom"><span>© 2026 Tubyo</span><nav><a href="/support/">{e(d['support'])}</a><a href="/privacy/">{e(d['privacy'])}</a><a href="/terms/">{e(d['terms'])}</a></nav></div><p>{e(d['independent'])}</p><small>{e(d['legalLang'])}</small><div class="footer-languages">{languages}</div></footer>
<dialog id="image-viewer"><button class="close" type="button" aria-label="{e(d['close'])}">×</button><img alt=""></dialog></body></html>'''
for lang in DATA:
 dest=DOC/lang;dest.mkdir(exist_ok=True)
 (dest/'index.html').write_text(page(lang))
root=page('en').replace(f'<link rel="canonical" href="{ORIGIN}/en/">',f'<link rel="canonical" href="{ORIGIN}/">').replace('"url": "https://tubyo.github.io/en/"','"url": "https://tubyo.github.io/"')
(DOC/'index.html').write_text(root)
urls=['/']+[f'/{l}/' for l in DATA]+['/support/','/privacy/','/terms/']
(DOC/'sitemap.xml').write_text('<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'+''.join(f'<url><loc>{ORIGIN}{p}</loc></url>' for p in urls)+'</urlset>')
(DOC/'robots.txt').write_text(f'User-agent: *\nAllow: /\nSitemap: {ORIGIN}/sitemap.xml\n')
print('Generated five localized pages, root, sitemap and robots.txt')

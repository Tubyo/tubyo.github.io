#!/usr/bin/env python3
"""Generate crawlable, localized landing pages without runtime dependencies."""
from pathlib import Path
from html import escape as e
import json
ROOT=Path(__file__).resolve().parents[1]
DOC=ROOT/'docs'
DATA=json.loads((ROOT/'content/site.json').read_text())
META=json.loads((ROOT/'content/slides.json').read_text())
GUIDES=json.loads((ROOT/'content/guides.json').read_text())
ORIGIN='https://tubyo.github.io'
CONTACT='mailto:tubyoapp@gmail.com'
VERIFICATION='xyOvGSgZWc9kIYk8hIXy34WhQBgsn3dlGP6D8vuxXgI'
# Second ownership tag for the Search Console URL-prefix property of tubyo.github.io;
# both tags are emitted so neither property loses its verification.
VERIFICATION_TAGS=f'<meta name="google-site-verification" content="{VERIFICATION}"><meta name="google-site-verification" content="zgApB9B-ibKJ69RhR8z00YOoB2r1AowAPKY0ffsqHds">'
GUIDE_ORDER=['pip','adblock','chromecast','kids','platforms']
GUIDE_SECTION={'fr':'Guides pratiques','en':'Practical guides','es':'Guías prácticas','de':'Praktische Anleitungen','nl':'Praktische gidsen'}
GUIDE_CARD={
 'fr':{'pip':'Image dans l’image','adblock':'Filtrage publicitaire','chromecast':'Chromecast','kids':'Mode enfant','platforms':'Android, iPhone, iPad'},
 'en':{'pip':'Picture in Picture','adblock':'Ad filtering','chromecast':'Chromecast','kids':'Child mode','platforms':'Android, iPhone, iPad'},
 'es':{'pip':'Imagen dentro de imagen','adblock':'Filtrado de anuncios','chromecast':'Chromecast','kids':'Modo infantil','platforms':'Android, iPhone, iPad'},
 'de':{'pip':'Bild-in-Bild','adblock':'Werbefilter','chromecast':'Chromecast','kids':'Kindermodus','platforms':'Android, iPhone, iPad'},
 'nl':{'pip':'Beeld-in-beeld','adblock':'Advertentiefilter','chromecast':'Chromecast','kids':'Kindermodus','platforms':'Android, iPhone, iPad'},
}
def locale_url(lang):
 return ORIGIN+'/' if lang=='en' else f'{ORIGIN}/{lang}/'
def path_url(lang, path):
 return f'/{path}/' if lang=='en' else f'/{lang}/{path}/'
def guide_url(lang, key):
 return ORIGIN+path_url(lang, GUIDES[key][lang]['slug'])
def guide_cards(lang):
 d=DATA[lang]
 return ''.join(f'<a class="guide-card" href="{path_url(lang, GUIDES[key][lang]["slug"])}"><h3>{e(GUIDE_CARD[lang][key])}</h3><p>{e(GUIDES[key][lang]["lead"])}</p><span aria-hidden="true">↗</span></a>' for key in GUIDE_ORDER)
def guide_footer_links(lang):
 return ''.join(f'<a href="{path_url(lang, GUIDES[key][lang]["slug"])}">{e(GUIDE_CARD[lang][key])}</a>' for key in GUIDE_ORDER)
def page(lang):
 d=DATA[lang]; loc=d['locale']; url=locale_url(lang)
 alternates=''.join(f'<link rel="alternate" hreflang="{l}" href="{locale_url(l)}">' for l in DATA)+f'<link rel="alternate" hreflang="x-default" href="{ORIGIN}/">'
 languages=''.join(f'<a href="/{l}/" lang="{l}" hreflang="{l}"'+(' aria-current="page"' if l==lang else '')+f'>{v["name"]}</a>' for l,v in DATA.items())
 nav=''.join(f'<a href="#{anchor}">{e(label)}</a>' for anchor,label in zip(['experience','gallery','kids','free'],d['nav']))
 icons=['▣','◈','▤','↺']
 cards=''.join(f'<article class="feature"><span class="feature-icon" aria-hidden="true">{icons[i]}</span><h3>{e(t)}</h3><p>{e(body)}</p></article>' for i,(t,body) in enumerate(d['features']))
 slides=''.join(f'''<a class="poster" href="/assets/screens/{loc}/iphone/{key}.webp" data-key="{key}"><img src="/assets/screens/{loc}/iphone/{key}.webp" width="660" height="1434" loading="lazy" decoding="async" alt="{e(title)} — Tubyo · iPhone"><span>{i+1:02d} <b>{e(title)}</b><span aria-hidden="true">↗</span></span></a>''' for i,(key,title,subtitle) in enumerate(META[loc]['slides']))
 faq=''.join(f'<details><summary>{e(q)}<span aria-hidden="true">+</span></summary><p>{e(a)}</p></details>' for q,a in d['faq'])
 points=''.join(f'<li><span aria-hidden="true">✓</span>{e(t)}</li>' for t in d['kidsPoints'])
 intents=''.join(f'<article class="intent"><h3>{e(t)}</h3><p>{e(body)}</p></article>' for t,body in d['intents'])
 og_image=f'{ORIGIN}/assets/og/{loc}.png'
 organization={'@type':'Organization','@id':f'{ORIGIN}/#organization','name':'Tubyo','url':f'{ORIGIN}/','email':'tubyoapp@gmail.com','logo':{'@type':'ImageObject','url':f'{ORIGIN}/assets/brand.png','width':1024,'height':1024}}
 website={'@type':'WebSite','@id':f'{url}#website','name':'Tubyo','alternateName':['Tubyo app','Tubyo video app'],'url':url,'inLanguage':loc,'description':d['description'],'publisher':{'@id':f'{ORIGIN}/#organization'}}
 application={'@type':'MobileApplication','@id':f'{ORIGIN}/#app','name':'Tubyo','alternateName':'Tubyo — PiP, filtrage publicitaire et mode enfant','applicationCategory':'MultimediaApplication','applicationSubCategory':'Video player','operatingSystem':'iOS, iPadOS, Android','url':url,'image':og_image,'description':d['description'],'inLanguage':loc,'offers':{'@type':'Offer','price':'0','priceCurrency':'EUR'},'publisher':{'@id':f'{ORIGIN}/#organization'}}
 faq_page={'@type':'FAQPage','@id':f'{url}#faq','inLanguage':loc,'mainEntity':[{'@type':'Question','name':q,'acceptedAnswer':{'@type':'Answer','text':a}} for q,a in d['faq']]}
 schema={'@context':'https://schema.org','@graph':[organization,website,application,faq_page]}
 return f'''<!doctype html>
<html lang="{lang}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="description" content="{e(d['description'])}">{VERIFICATION_TAGS}<meta name="robots" content="index,follow,max-image-preview:large"><meta name="theme-color" content="#0b1715"><meta name="referrer" content="strict-origin-when-cross-origin"><title>{e(d['title'])}</title><link rel="icon" href="/assets/brand.png"><link rel="apple-touch-icon" href="/assets/brand.png"><link rel="canonical" href="{url}">{alternates}<meta property="og:type" content="website"><meta property="og:site_name" content="Tubyo"><meta property="og:title" content="{e(d['title'])}"><meta property="og:description" content="{e(d['description'])}"><meta property="og:url" content="{url}"><meta property="og:locale" content="{loc.replace('-','_')}"><meta property="og:image" content="{og_image}"><meta property="og:image:width" content="1200"><meta property="og:image:height" content="630"><meta property="og:image:alt" content="{e(d['title'])}"><meta name="twitter:card" content="summary_large_image"><meta name="twitter:title" content="{e(d['title'])}"><meta name="twitter:description" content="{e(d['description'])}"><meta name="twitter:image" content="{og_image}"><link rel="stylesheet" href="/assets/landing.css"><link rel="stylesheet" href="/assets/intents.css"><script type="application/ld+json">{json.dumps(schema,ensure_ascii=False)}</script><script src="/assets/landing.js" defer></script></head>
<body data-locale="{loc}"><a class="skip" href="#main">{e(d['skip'])}</a><header class="header"><a href="/{lang}/" class="wordmark" aria-label="Tubyo">Tuby<img src="/assets/brand.png" width="36" height="36" alt="o"></a><nav aria-label="Tubyo">{nav}</nav><details class="languages"><summary aria-label="{e(d['language'])}"><span aria-hidden="true">◎</span> {lang.upper()} <span aria-hidden="true">⌄</span></summary><div>{languages}</div></details></header>
<main id="main"><section class="hero wrap"><div class="hero-copy"><p class="eyebrow">{d['eyebrow']}</p><h1>{d['headline']}</h1><p class="intro">{e(d['intro'])}</p><p class="free-line"><span aria-hidden="true">✓</span> {e(d['free'])}</p><div class="cta-row"><a class="button" href="#gallery">{e(d['discover'])}<span aria-hidden="true">↗</span></a><a class="text-link" href="{CONTACT}">{e(d['contact'])}</a></div><div class="stores"><span>{e(d['apple'])}</span><span>{e(d['android'])}</span></div></div><div class="hero-art"><div class="orbit" aria-hidden="true"></div><img class="phone phone-back" src="/assets/screens/{loc}/hero-youtube.webp" width="390" height="844" alt="{e(META[loc]['slides'][2][1])}" decoding="async"><img class="phone phone-front" src="/assets/screens/{loc}/hero-home.webp" width="390" height="844" alt="{e(META[loc]['slides'][0][1])}" fetchpriority="high"></div></section>
<div class="platform-strip wrap"><span>{e(d['platforms'])}</span><div>YouTube <i>·</i> Twitch <i>·</i> TikTok <i>·</i> Instagram</div></div>
<section id="experience" class="section wrap"><p class="eyebrow">TUBYO</p><h2>{d['featuresTitle']}</h2><div class="features">{cards}</div><div class="intents">{intents}</div></section>
<section id="gallery" class="gallery-section"><div class="wrap gallery-heading"><div><p class="eyebrow">IPHONE & IPAD</p><h2>{e(d['galleryTitle'])}</h2><p>{e(d['galleryText'])}</p></div><div class="device-switch" role="group" aria-label="iPhone / iPad"><button type="button" data-device="iphone" aria-pressed="true">iPhone</button><button type="button" data-device="ipad" aria-pressed="false">iPad</button></div></div><div class="posters wrap">{slides}</div></section>
<section id="kids" class="kids section wrap"><div class="kids-art"><img src="/assets/screens/{loc}/ipad/kids.webp" width="800" height="1067" loading="lazy" decoding="async" alt="{e(META[loc]['slides'][6][1])}"></div><div><span class="kids-word" aria-label="Kids"><b>k</b><b>i</b><b>d</b><b>s</b></span><p class="eyebrow">{e(d['kidsTag'])}</p><h2>{d['kidsTitle']}</h2><p class="intro">{e(d['kidsText'])}</p><ul class="checks">{points}</ul></div></section>
<section id="free" class="pricing section wrap"><div><p class="eyebrow">{e(d['priceTag'])}</p><h2>{d['priceTitle']}</h2><p class="intro">{e(d['priceText'])}</p></div><div class="price-card"><div class="zero">0<span>€</span></div><h3>{e(d['free'])}</h3><div class="divider"></div><h4>{e(d['optional'])}</h4><p>{e(d['optionalText'])}</p></div></section>
<section class="faq section wrap"><h2>{e(d['faqTitle'])}</h2><div>{faq}</div></section><section id="guides" class="section wrap"><p class="eyebrow">{e(GUIDE_SECTION[lang])}</p><div class="guides">{guide_cards(lang)}</div></section><section class="closing wrap"><p class="eyebrow">TUBYO</p><h2>{d['endTitle']}</h2><a class="button" href="{CONTACT}">{e(d['contact'])}<span aria-hidden="true">↗</span></a><p>{e(d['apple'])} · {e(d['android'])}</p></section></main>
<footer class="wrap"><div class="footer-top"><a href="/{lang}/" class="wordmark" aria-label="Tubyo">Tuby<img src="/assets/brand.png" width="36" height="36" alt="o"></a><a href="{CONTACT}">tubyoapp@gmail.com</a></div><div class="footer-guides">{guide_footer_links(lang)}</div><div class="footer-bottom"><span>© 2026 Tubyo</span><nav><a href="/support/">{e(d['support'])}</a><a href="/privacy/">{e(d['privacy'])}</a><a href="/terms/">{e(d['terms'])}</a></nav></div><p>{e(d['independent'])}</p><small>{e(d['legalLang'])}</small><div class="footer-languages">{languages}</div></footer>
<dialog id="image-viewer"><button class="close" type="button" aria-label="{e(d['close'])}">×</button><img alt=""></dialog></body></html>'''
def guide_page(lang, key):
 d=DATA[lang]; loc=d['locale']; gd=GUIDES[key][lang]
 url=guide_url(lang,key); prefix='' if lang=='en' else '/'+lang
 home=page(lang)
 header=home[home.index('<header class="header">'):home.index('<main id="main">')]
 header=header[:header.index('<details class="languages">')]
 header=header.replace('href="#',f'href="{prefix}/#')
 guide_languages=''.join(f'<a href="{path_url(l, GUIDES[key][l]["slug"])}" lang="{l}" hreflang="{l}"'+(' aria-current="page"' if l==lang else '')+f'>{v["name"]}</a>' for l,v in DATA.items())
 header+=f'<details class="languages"><summary aria-label="{e(d["language"])}"><span aria-hidden="true">◎</span> {lang.upper()} <span aria-hidden="true">⌄</span></summary><div>{guide_languages}</div></details></header>'
 footer=home[home.index('<footer class="wrap">'):home.index('<dialog')]
 footer_languages=''.join(f'<a href="{path_url(l, GUIDES[key][l]["slug"])}" lang="{l}" hreflang="{l}"'+(' aria-current="page"' if l==lang else '')+f'>{v["name"]}</a>' for l,v in DATA.items())
 footer=footer[:footer.index('<div class="footer-languages">')]+f'<div class="footer-languages">{footer_languages}</div></footer>'
 alternates=''.join(f'<link rel="alternate" hreflang="{l}" href="{guide_url(l,key)}">' for l in DATA)+f'<link rel="alternate" hreflang="x-default" href="{guide_url("en",key)}">'
 og_image=f'{ORIGIN}/assets/og/{loc}.png'
 organization={'@type':'Organization','@id':f'{ORIGIN}/#organization','name':'Tubyo','url':f'{ORIGIN}/','email':'tubyoapp@gmail.com','logo':{'@type':'ImageObject','url':f'{ORIGIN}/assets/brand.png','width':1024,'height':1024}}
 website={'@type':'WebSite','@id':f'{ORIGIN}/#website','name':'Tubyo','alternateName':['Tubyo app','Tubyo video app'],'url':f'{ORIGIN}/','publisher':{'@id':f'{ORIGIN}/#organization'}}
 article={'@type':'WebPage','@id':f'{url}#page','url':url,'name':gd['title'],'description':gd['description'],'inLanguage':loc,'isPartOf':{'@id':f'{ORIGIN}/#website'},'primaryImageOfPage':{'@type':'ImageObject','url':og_image}}
 breadcrumb={'@type':'BreadcrumbList','@id':f'{url}#breadcrumb','itemListElement':[{'@type':'ListItem','position':1,'name':'Tubyo','item':f'{ORIGIN}/'},{'@type':'ListItem','position':2,'name':gd['h1'],'item':url}]}
 faq_page={'@type':'FAQPage','@id':f'{url}#faq','inLanguage':loc,'mainEntity':[{'@type':'Question','name':q,'acceptedAnswer':{'@type':'Answer','text':a}} for q,a in gd['faq']]}
 schema={'@context':'https://schema.org','@graph':[organization,website,article,breadcrumb,faq_page]}
 sections=''.join(f'<section><h2>{e(h)}</h2><p>{e(body)}</p></section>' for h,body in gd['sections'])
 faq=''.join(f'<details><summary>{e(q)}<span aria-hidden="true">+</span></summary><p>{e(a)}</p></details>' for q,a in gd['faq'])
 related=''.join(f'<a href="{path_url(lang, GUIDES[other][lang]["slug"])}">{e(GUIDE_CARD[lang][other])}<span aria-hidden="true">↗</span></a>' for other,_ in gd['related'])
 return f'''<!doctype html>
<html lang="{lang}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="description" content="{e(gd['description'])}">{VERIFICATION_TAGS}<meta name="robots" content="index,follow,max-image-preview:large"><meta name="theme-color" content="#0b1715"><meta name="referrer" content="strict-origin-when-cross-origin"><title>{e(gd['title'])}</title><link rel="icon" href="/assets/brand.png"><link rel="apple-touch-icon" href="/assets/brand.png"><link rel="canonical" href="{url}">{alternates}<meta property="og:type" content="article"><meta property="og:site_name" content="Tubyo"><meta property="og:title" content="{e(gd['title'])}"><meta property="og:description" content="{e(gd['description'])}"><meta property="og:url" content="{url}"><meta property="og:locale" content="{loc.replace('-','_')}"><meta property="og:image" content="{og_image}"><meta property="og:image:width" content="1200"><meta property="og:image:height" content="630"><meta property="og:image:alt" content="{e(gd['title'])}"><meta name="twitter:card" content="summary_large_image"><meta name="twitter:title" content="{e(gd['title'])}"><meta name="twitter:description" content="{e(gd['description'])}"><meta name="twitter:image" content="{og_image}"><link rel="stylesheet" href="/assets/landing.css"><link rel="stylesheet" href="/assets/guide.css"><script type="application/ld+json">{json.dumps(schema,ensure_ascii=False)}</script><script src="/assets/landing.js" defer></script></head>
<body data-locale="{loc}">{header}<main id="main" class="guide wrap"><nav class="crumbs" aria-label="Breadcrumb"><a href="{prefix}/">Tubyo</a><span aria-hidden="true">›</span><span>{e(GUIDE_CARD[lang][key])}</span></nav><h1>{e(gd['h1'])}</h1><p class="lead">{e(gd['lead'])}</p><div class="guide-body">{sections}</div><nav class="related">{related}</nav><section class="guide-faq"><h2>{e(d['faqTitle'])}</h2>{faq}</section><section class="guide-cta"><a class="button" href="{CONTACT}">{e(d['contact'])}<span aria-hidden="true">↗</span></a><p>{e(d['apple'])} · {e(d['android'])}</p></section></main>
{footer}</body></html>'''

for lang in DATA:
 dest=DOC/lang;dest.mkdir(exist_ok=True)
 (dest/'index.html').write_text(page(lang))
 for key in GUIDE_ORDER:
  target=DOC/path_url(lang, GUIDES[key][lang]['slug']).strip('/')
  target.mkdir(parents=True,exist_ok=True)
  (target/'index.html').write_text(guide_page(lang,key))
root=page('en').replace(f'<link rel="canonical" href="{ORIGIN}/en/">',f'<link rel="canonical" href="{ORIGIN}/">').replace('"url": "https://tubyo.github.io/en/"','"url": "https://tubyo.github.io/"')
(DOC/'index.html').write_text(root)
urls=['/']+[f'/{l}/' for l in DATA if l!='en']+[path_url(l, GUIDES[k][l]['slug']) for k in GUIDE_ORDER for l in DATA]+['/support/','/privacy/','/terms/']
from datetime import date
stamp=date.today().isoformat()
(DOC/'sitemap.xml').write_text('<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'+''.join(f'<url><loc>{ORIGIN}{p}</loc><lastmod>{stamp}</lastmod></url>' for p in urls)+'</urlset>')
(DOC/'robots.txt').write_text(f'User-agent: *\nAllow: /\nSitemap: {ORIGIN}/sitemap.xml\n')
print(f'Generated {len(DATA)} localized landings, {len(GUIDE_ORDER)*len(DATA)} guide pages, root, sitemap and robots.txt')

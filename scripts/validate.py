#!/usr/bin/env python3
"""Check generated routes, local assets and localized screenshot coverage."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit,unquote
import json
root=Path(__file__).resolve().parents[1]/'docs'
class Links(HTMLParser):
 def __init__(self):super().__init__();self.refs=[];self.h1=0;self.lang=None;self.titles=0
 def handle_starttag(self,tag,attrs):
  a=dict(attrs)
  if tag=='h1':self.h1+=1
  if tag=='html':self.lang=a.get('lang')
  if tag=='title':self.titles+=1
  for attr in ('src','href'):
   if attr in a:self.refs.append(a[attr])
errors=[]
for p in root.rglob('*.html'):
 if p.name.startswith('google') and p.name.endswith('.html'):continue  # Search Console ownership file
 text=p.read_text();parser=Links();parser.feed(text)
 if parser.h1!=1 or parser.titles!=1:errors.append(f'Invalid heading/title count: {p}')
 if 'elm.dev.code@gmail.com' in text:errors.append(f'Old email: {p}')
 for ref in parser.refs:
  u=urlsplit(ref)
  if u.scheme or u.netloc or not u.path:continue
  target=root/unquote(u.path.lstrip('/')) if u.path.startswith('/') else p.parent/unquote(u.path)
  if target.is_dir():target=target/'index.html'
  if not target.exists():errors.append(f'Missing reference {p}: {ref}')
LANG_LIST=['fr','en','es','de','nl']
pages=json.loads((root.parent/'content'/'guides.json').read_text())
order=['pip','adblock','chromecast','background','fullscreen','live','kids','library','save','shortcuts','sites','private','platforms']
for key in order:
 for lang in LANG_LIST:
  data=pages[key][lang]
  path=root/(data['slug'] if lang=='en' else f'{lang}/{data["slug"]}')/'index.html'
  if not path.exists():errors.append(f'Missing guide page {lang}/{key}');continue
  text=path.read_text()
  if text.count('<h1>')!=1 or text.count('<title>')!=1:errors.append(f'Invalid heading/title count: {path}')
  for signal in ['og:site_name','"FAQPage"','"BreadcrumbList"','rel="canonical"','hreflang="x-default"','class="related"','class="guide-faq"']:
   if signal not in text:errors.append(f'Missing {signal} in {path}')
  if f'<link rel="canonical" href="https://tubyo.github.io{"/" if lang=="en" else "/"+lang+"/"}{data["slug"]}/">' not in text:
   errors.append(f'Wrong canonical: {path}')
 if f'https://tubyo.github.io{"/" if lang=="en" else "/"+lang+"/"}{data["slug"]}/' not in (root/'sitemap.xml').read_text():
   errors.append(f'Guide missing from sitemap: {lang}/{key}')
for lang,locale in [('fr','fr-FR'),('en','en-US'),('es','es-ES'),('de','de-DE'),('nl','nl-NL')]:
 text=(root/lang/'index.html').read_text()
 assert f'<html lang="{lang}">' in text
 assert text.count('class="poster"')==10
 assert text.count('hreflang="')>=5
 assert 'google-site-verification' in text
 expected='https://tubyo.github.io/' if lang=='en' else f'https://tubyo.github.io/{lang}/'
 assert f'<link rel="canonical" href="{expected}">' in text
 assert '<meta property="og:site_name" content="Tubyo">' in text
 assert f'<meta property="og:image" content="https://tubyo.github.io/assets/og/{locale}.png">' in text
 assert '<meta name="twitter:card" content="summary_large_image">' in text
 assert '"MobileApplication"' in text and '"FAQPage"' in text and '"Organization"' in text
 assert text.count('class="intent"')==3
 assert text.count('class="guide-card"')==len(order)
 assert 'class="footer-guides"' in text
 assert text.count('<details>')>=6
 assert '/assets/intents.css' in text
 if not (root/'assets'/'og'/f'{locale}.png').exists():errors.append(f'Missing social card {locale}')
 for device in ['iphone','ipad']:
  if len(list((root/'assets/screens'/locale/device).glob('*.webp')))!=10:errors.append(f'Incomplete gallery {locale}/{device}')
assert (root/'app-ads.txt').exists()
assert (root/'assets'/'intents.css').exists()
sitemap=(root/'sitemap.xml').read_text()
expected_urls=1+(len(LANG_LIST)-1)+len(order)*len(LANG_LIST)+3
assert sitemap.count('<lastmod>')==sitemap.count('<loc>') and sitemap.count('<loc>')==expected_urls, f'{sitemap.count("<loc>")} urls, expected {expected_urls}'
if errors:raise SystemExit('\n'.join(errors))
print('PASS: routes, contact email, headings, language alternates, site name, social cards, structured data, 100 poster assets and app-ads.txt')

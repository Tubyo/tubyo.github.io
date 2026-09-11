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
 text=p.read_text();parser=Links();parser.feed(text)
 if parser.h1!=1 or parser.titles!=1:errors.append(f'Invalid heading/title count: {p}')
 if 'elm.dev.code@gmail.com' in text:errors.append(f'Old email: {p}')
 for ref in parser.refs:
  u=urlsplit(ref)
  if u.scheme or u.netloc or not u.path:continue
  target=root/unquote(u.path.lstrip('/')) if u.path.startswith('/') else p.parent/unquote(u.path)
  if target.is_dir():target=target/'index.html'
  if not target.exists():errors.append(f'Missing reference {p}: {ref}')
for lang,locale in [('fr','fr-FR'),('en','en-US'),('es','es-ES'),('de','de-DE'),('nl','nl-NL')]:
 text=(root/lang/'index.html').read_text()
 assert f'<html lang="{lang}">' in text
 assert text.count('class="poster"')==10
 assert text.count('hreflang="')>=5
 for device in ['iphone','ipad']:
  if len(list((root/'assets/screens'/locale/device).glob('*.webp')))!=10:errors.append(f'Incomplete gallery {locale}/{device}')
assert (root/'app-ads.txt').exists()
if errors:raise SystemExit('\n'.join(errors))
print('PASS: routes, contact email, headings, language alternates, 100 poster assets and app-ads.txt')

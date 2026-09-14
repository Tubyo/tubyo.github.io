#!/usr/bin/env python3
"""Render the social preview card for every locale with headless Chrome.

The card is what search engines and social apps show next to the page, so it is
generated from the same localized copy as the page itself instead of being
hand-edited. Run after build.py; the output lives in docs/assets/og/.
"""
from pathlib import Path
import json, subprocess, tempfile

ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / 'docs'
DATA = json.loads((ROOT / 'content/site.json').read_text())
CHROME = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'


def card(lang, d):
    loc = d['locale']
    prefix = '' if lang == 'en' else lang + '/'
    brand = (DOC / 'assets' / 'brand.png').as_uri()
    phone = (DOC / 'assets' / 'screens' / loc / 'iphone' / 'home.webp').as_uri()
    return f'''<!doctype html><html lang="{lang}"><head><meta charset="utf-8"><style>
      *{{box-sizing:border-box;margin:0}}
      body{{width:1200px;height:630px;background:#0b1715;color:#f4f7ee;
        font:20px/1.5 -apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;overflow:hidden;position:relative}}
      .glow{{position:absolute;inset:-30% -10% auto auto;width:900px;height:900px;border-radius:50%;
        background:radial-gradient(circle,#98ba3633,transparent 65%)}}
      .wrap{{position:relative;padding:64px 70px;height:100%;display:flex;gap:40px;align-items:center}}
      .copy{{flex:1}}
      .brand{{display:flex;align-items:center;gap:10px;font-size:34px;font-weight:750;letter-spacing:-1.5px;margin-bottom:34px}}
      .brand img{{width:44px;height:44px}}
      .eyebrow{{color:#cef25c;font-size:15px;letter-spacing:.16em;font-weight:700;margin-bottom:18px}}
      h1{{font-size:62px;line-height:1.06;letter-spacing:-.045em;font-weight:720;margin-bottom:22px}}
      em{{color:#cef25c;font-style:normal}}
      p{{color:#b8c6be;font-size:21px;max-width:620px}}
      .url{{margin-top:26px;color:#8fa295;font-size:17px;letter-spacing:.04em}}
      .phone{{width:250px;border:7px solid #28362e;border-radius:38px;background:#111c16;
        box-shadow:0 30px 70px #0009;transform:rotate(6deg)}}
    </style></head><body><div class="glow"></div><div class="wrap"><div class="copy">
      <div class="brand">Tuby<img src="{brand}" alt=""></div>
      <div class="eyebrow">{d['eyebrow']}</div>
      <h1>{d['headline']}</h1>
      <p>{d['free']}</p>
      <div class="url">tubyo.github.io/{prefix}</div>
    </div><img class="phone" src="{phone}" alt=""></div></body></html>'''


def main():
    out = DOC / 'assets' / 'og'
    out.mkdir(parents=True, exist_ok=True)
    for lang, d in DATA.items():
        with tempfile.TemporaryDirectory() as tmp:
            page = Path(tmp) / f'og-{lang}.html'
            page.write_text(card(lang, d))
            target = out / (d['locale'] + '.png')
            subprocess.run([CHROME, '--headless=new', '--hide-scrollbars', '--disable-gpu',
                '--force-device-scale-factor=1', '--window-size=1200,630',
                f'--screenshot={target}', page.as_uri()], check=True,
                stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print('rendered', d['locale'])


if __name__ == '__main__':
    main()

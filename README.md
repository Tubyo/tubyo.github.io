# Tubyo website

Official multilingual landing page, support, privacy and subscription information.
Published at https://tubyo.github.io through GitHub Pages (`master:/docs`).

## Content

- English, French, Spanish, German and Dutch landing pages at `/en/`, `/fr/`,
  `/es/`, `/de/` and `/nl/`; `/` is the English default.
- 100 localized iPhone/iPad marketing posters, optimized to WebP; gallery supports
  device selection and full-size viewing. Original capture provenance remains in
  the private application repository.
- All public contact links use `tubyoapp@gmail.com`.
- Existing support, privacy, terms and `app-ads.txt` URLs remain stable.
- Legal documents remain explicitly identified as English.
- No advertising, analytics, third-party fonts or tracking scripts on the site.

## Edit and verify

Edit `content/site.json`, `content/slides.json`, `scripts/build.py` and
`docs/assets/landing.css` / `landing.js`. Run:

```sh
python3 scripts/build.py
python3 scripts/validate.py
node --check docs/assets/landing.js
```

`content/image-manifest.json` maps optimized images to the original marketing
package. Do not put private app code, account details or credentials here.

The website currently announces an upcoming App Store release and a planned
Android release. Only replace availability copy and add a download CTA after
verifying that the app is publicly available. Do not imply that App Review
preparation is a commercial release.

## Search indexing

The URL-prefix property `https://tubyo.github.io/` is verified in Google Search
Console under the Tubyo Google account. Keep the `google-site-verification`
meta tag in the generator: removing it can invalidate ownership.

The root is the canonical English page; `/en/` is a navigable alias. French,
Spanish, German and Dutch pages are self-canonical and connected by reciprocal
hreflang links. The sitemap contains the eight canonical public pages.

Indexing and search positions are controlled by search engines. Verification,
submission and a successful HTTP response do not prove indexing. Check Search
Console's sitemap processing and URL Inspection reports before making such a
claim. Do not add fake reviews, keyword-stuffed pages or invented download counts.

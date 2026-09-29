# relavoi-site

Public marketing site for Relavoi — number-masking infrastructure for the
Nigerian market. Static HTML/CSS/JS, no build step.

Imported from the **NMaaS** Claude Design project
(`019dd2cd-8b92-71af-8c2d-40f0fde06750`), with the copy fact-checked against the
live platform.

## Layout

```
site/
  index.html          home
  products.html       voice, SMS, SDKs, analytics, pricing
  how-it-works.html   five-step walkthrough + session lifecycle
  developers.html     API, SDKs, webhook contract
  about.html          story, principles, where the product actually is
  contact.html        channels + enquiry form
  site.css            design system (colors, type, nav/footer, cards, buttons)
  site.js             injects the shared nav + footer into every page
```

`site.js` renders the nav and footer at runtime, so every page needs
`<body data-page="…">` and `<script src="site.js">` — the `data-page` value
matches the third element of each entry in the `links` array and drives the
active nav state.

## Run it

Any static server; `file://` also works.

```bash
cd site && python3 -m http.server 8000   # → http://localhost:8000
```

## Status

All six pages are ported. Blockers before this can go public are listed under
**Open items** in [`CLAIMS.md`](./CLAIMS.md) — the short version: `relavoi.com`
has no DNS record (so the `@relavoi.com` addresses on the contact page bounce),
the contact form has no backend and falls back to `mailto:`, and the published
pricing needs commercial sign-off.

## Copy rules

Read [`CLAIMS.md`](./CLAIMS.md) before editing any text. It records the source
for every factual claim on the site and lists the ones removed from the original
template as unsupported.

The ones that keep resurfacing:

1. **No customer names** until there is a signed customer who has agreed to be
   named. The original template listed five real Nigerian companies we have no
   relationship with.
2. **Targets are labelled as targets.** `<500ms` is a performance budget, not a
   measured median. Don't quote uptime until it's actually recorded.
3. **Relavoi is not NCC licensed.** Numbers are provisioned through Africa's
   Talking, which holds the approvals. Say it that way.
4. **Prices are a commitment.** The naira rates on `products.html` mirror
   `pricing-seed.ts` in the backend. If one changes, change the other.
5. **Only link docs URLs you've actually loaded.** Several deep links in the
   original template 404 on the deployed docs build.

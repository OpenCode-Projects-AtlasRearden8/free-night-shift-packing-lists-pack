# STATUS.md

## What was built

**Night-Shift Packing Lists Pack** — a free printable pack of tear-out packing
checklists for night-shift nurses and late-shift workers. Print-friendly plain
HTML, US Letter layout, zero backend, no accounts, no tracking. Education only;
every page explicitly states it is not medical advice.

Contents (all pages, plus a hub):

- `index.html` — hub: what's in the pack, how to print, how progress saving works,
  and how this pack differs from the shift-swap pack (coverage trading — a
  different problem) and the night-shift survival guide (a manual — a different
  format). Credits Asdale Dynamics, LLC.
- `checklist-12hr-medsurg.html` — 12-hour med-surg: front-door pocket check,
  full-bag tear-out card (fuel / comfort / job tools / 3 a.m. survival), and a
  go-home recovery kit card.
- `checklist-float-agency.html` — float/agency: full bag, "first 15 minutes on an
  unfamiliar unit" card, and a rent-a-drawer minimum kit.
- `checklist-ed-wipes.html` — ED wet-and-dry wipes edition: a two-bag system
  (dry bag vs grab-and-reset wet bag) plus an 8-minute go-home reset card.
- `weather-addons.html` — three season add-on tear-outs: deep winter/ice,
  summer heat advisories, rain commute/storm season.
- `energy-snacks.html` — coffee-free energy snack ideas sorted by shift window
  (hour 0–3, 3–6, 6–10, 10–12) with packability ratings, four snack archetypes,
  educational caffeine notes, and a shopping-trip tear-out.
- `locker-inventory.html` — fill-in locker-stash inventory table, restock-ritual
  rules card, and a wallet-size pocket copy.
- `fatigue-prep.html` — fatigue-prep one-pager: day-sleep setup, light-as-a-tool
  summary, nap basics, the too-tired-to-drive plan, signposting to clinicians.

Supporting files:

- `assets/style.css` — shared print-friendly styling: tear-out dashed card
  borders with scissors cues, checkbox styling, tables, US Letter `@page`
  0.5in margins, and `@media print` rules that hide UI chrome.
- `assets/app.js` — tiny dependency-free script: checkbox progress saved to
  browser local storage only (`fnspl-v1:*` keys, per-page), Uncheck-all and
  Print buttons. Graceful no-JS fallback: everything still prints and reads fine.
- `scripts/verify.py` — repo verifier (structure, links, assets, required files,
  exact LICENSE copyright line).
- `scripts/print-pdf.sh` — optional local print-to-PDF smoke test with Chrome.
- `README.md` — credit to Asdale Dynamics, LLC; usage; pack positioning.
- `LICENSE` — MIT, copyright line exactly `Copyright (c) 2026 Asdale Dynamics, LLC`.
- `.gitignore` — ignores generated `dist/` PDF output.

## How to run it

No build, no install, no server. Open `index.html` in any browser, or open any
single page directly. To print, use any page's Print button or the browser's
print dialog (paper: US Letter, margins: handled by the CSS).

Optional verification:

```sh
python3 scripts/verify.py          # structure/link/asset checks
bash scripts/print-pdf.sh          # renders PDFs into dist/ (needs Chrome)
node --check assets/app.js         # JS syntax (Node optional)
```

## Verification results (2026-11-07)

- `python3 scripts/verify.py`: **OK** — 8 pages, 153 checkboxes, 31 local
  href/src references all resolve to files that exist; all pages have title,
  charset, viewport, shared stylesheet, shared app.js, clear-all control; every
  content page carries explicit not-medical-advice wording; LICENSE carries the
  exact line `Copyright (c) 2026 Asdale Dynamics, LLC`; README credits
  Asdale Dynamics, LLC. Zero errors at final run.
- Header/nesting audit: found and fixed one stray `</h2>` close tag in
  `checklist-ed-wipes.html`; final pass reports zero unclosed/nested tag errors.
- Headless Chrome print-to-PDF smoke test: all 8 pages rendered to PDF
  successfully (artifacts were generated during testing and then removed;
  `dist/` is gitignored since it's regenerable output).
- Headless Chrome DOM-dump check on all 8 pages: no page-level errors
  (uncaught JS, refused resource loads, or net errors); environment-only
  GPU/xcb messages in a headless container are unrelated to the pages.
- `node --check assets/app.js`: syntax OK.
- Repository: no secrets, API keys, personal data, or network calls; no
  external fonts/CDNs; fully local-first.

## Known gaps / honest limits

- Checkbox persistence is per-browser only (local storage). Print card state is
  obviously ink, and if you clear site data the ticks reset with it.
- US Letter geometry is tuned and tested; A4 prints fine but margins/cut lines
  may sit slightly differently on some printers' borderless settings.
- Content is deliberately generic wellness/hygiene education; it cannot cover
  employer-specific PPE, decon, or break policy — the pages point to facility
  policy and clinicians instead of guessing at clinical specifics.
- No multi-language versions yet; English only.
- No compiled all-in-one "print the entire pack" page yet (each page prints on
  its own; combining pages into one long sheet is a possible future addition).
- Screen-reader semantics are basic (native checkboxes/labels, no ARIA extras);
  a future accessibility pass could add skip links and landmark roles.

# Night-Shift Packing Lists Pack

Free printable tear-out packing checklists for night-shift nurses and late-shift
workers. Plain HTML, zero backend, no accounts, no tracking — open a page, tick
boxes on screen (saved locally in your own browser) or print and cut the cards.

Built for the reality of leaving the house at 6:15 p.m. with 15 minutes to pack:
one-page tear-out cards you can tape inside your bag, locker door, or glovebox.

## What's inside

| Page | What it's for |
| --- | --- |
| `index.html` | Hub: how to use the pack, links to every page |
| `checklist-12hr-medsurg.html` | Tear-out full-bag + pocket check + go-home kit for a 12-hour med-surg night |
| `checklist-float-agency.html` | Float/agency bag, "first 15 minutes on an unfamiliar unit" card, rent-a-drawer minimum kit |
| `checklist-ed-wipes.html` | ED "wet-and-dry wipes" two-bag system for the messiest shifts |
| `weather-addons.html` | Add-on cards: deep winter, summer heat, rain commute |
| `energy-snacks.html` | Coffee-free energy snack ideas sorted by shift timing, with a shopping-trip tear-out |
| `locker-inventory.html` | Fill-in locker-stash inventory card + restock-ritual rules + wallet-size copy |
| `fatigue-prep.html` | One-pager: day-sleep setup, light, naps, and the too-tired-to-drive plan |

## How to run it

Nothing to install. Open `index.html` in any browser, or open an individual
page directly. To print, use your browser's print dialog — the pages are laid
out for US Letter with 0.5-inch margins, and print cleanly in black and white.

Checkbox progress is stored in your browser's local storage only
(`fnspl-v1:*` keys). Clear a page's progress with its **Uncheck all** button.
No data is sent anywhere; there is no server.

To verify everything (HTML well-formedness, internal links, assets, and a
print-to-PDF smoke test with headless Chrome):

```sh
python3 scripts/verify.py
```

To render printable PDFs locally (optional, requires Google Chrome):

```sh
bash scripts/print-pdf.sh
```

## Repository hygiene

- No secrets, API keys, or personal data — nothing collectible is built in.
- No backend, no network calls, no external fonts or CDNs.
- Education only. **Never medical advice.** Every page says so, and anything
  health-shaped points readers to their own clinician.

## How this pack relates to the other packs

- **free-nurse-shift-swap-pack** is about *trading and covering shifts*
  (coverage). This pack is about *packing your bag* — different problem.
- **night-shift-survival-guide** is a longer manual-style resource. These are
  one-page tear-outs designed for a printer and a pair of scissors.

## License

MIT — see [LICENSE](LICENSE). Free to print, copy, adapt, and share.

Copyright (c) 2026 Asdale Dynamics, LLC — Dylan Asdale's plain-English AI
education and practical-tools company ([dylanasdale.github.io](https://dylanasdale.github.io)).

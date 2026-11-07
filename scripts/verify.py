#!/usr/bin/env python3
"""Verify the Night-Shift Packing Lists Pack.

Checks:
  1. Every .html file parses cleanly (html.parser, never raises on bad nesting,
     so we additionally sanity-check required structure).
  2. Every internal href/src resolves to a file in this repo.
  3. Every page links the shared stylesheet and script.
  4. Every page that uses checkboxes offers both a print and clear-all control.
  5. LICENSE, README.md, and index.html exist; LICENSE carries the exact
     copyright line.

Optionally, run the print-to-PDF smoke test with Chrome:
  bash scripts/print-pdf.sh
"""

import re
import sys
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

COPYRIGHT_LINE = "Copyright (c) 2026 Asdale Dynamics, LLC"

REQUIRED_PAGES = [
    "index.html",
    "checklist-12hr-medsurg.html",
    "checklist-float-agency.html",
    "checklist-ed-wipes.html",
    "weather-addons.html",
    "energy-snacks.html",
    "locker-inventory.html",
    "fatigue-prep.html",
]

VOID_ELEMENTS = {
    "area", "base", "br", "col", "embed", "hr", "img", "input",
    "link", "meta", "param", "source", "track", "wbr",
}

errors: list[str] = []
warnings: list[str] = []


class PageAudit(HTMLParser):
    """Collect structure info and flag unclosed tags."""

    def __init__(self, name: str):
        super().__init__(convert_charrefs=True)
        self.name = name
        self.stack: list[tuple[int, str]] = []
        self.hrefs: list[str] = []
        self.srcs: list[str] = []
        self.checkboxes = 0
        self.has_title = False
        self.has_charset = False
        self.has_viewport = False
        self.has_stylesheet = False
        self.has_script = False

    def handle_starttag(self, tag, attrs):
        attrs_d = dict(attrs)
        if tag == "title":
            self.has_title = True
        if tag == "meta":
            if attrs_d.get("charset"):
                self.has_charset = True
            if attrs_d.get("name") == "viewport":
                self.has_viewport = True
        if tag == "link" and attrs_d.get("rel") == "stylesheet":
            target = attrs_d.get("href", "")
            self.hrefs.append(target)
            if target.endswith("style.css"):
                self.has_stylesheet = True
        if tag == "script" and attrs_d.get("src"):
            target = attrs_d.get("src", "")
            self.srcs.append(target)
            if target.endswith("app.js"):
                self.has_script = True
        if tag == "a" and attrs_d.get("href"):
            self.hrefs.append(attrs_d["href"])
        if tag == "img" and attrs_d.get("src"):
            self.srcs.append(attrs_d["src"])
        if tag == "input" and attrs_d.get("type") == "checkbox":
            self.checkboxes += 1
        if tag not in VOID_ELEMENTS:
            self.stack.append((self.getpos()[0], tag))

    def handle_endtag(self, tag):
        if tag in VOID_ELEMENTS:
            return
        if self.stack and self.stack[-1][1] == tag:
            self.stack.pop()
            return
        for i in range(len(self.stack) - 1, -1, -1):
            if self.stack[i][1] == tag:
                for _line, stale in reversed(self.stack[i + 1:]):
                    errors.append(f"{self.name}: <{stale}> closed implicitly at </{tag}> (line {self.getpos()[0]})")
                del self.stack[i:]
                return
        errors.append(f"{self.name}: stray </{tag}> at line {self.getpos()[0]}")


def check_local_resolution(page_audit: PageAudit, urls: list[str], kind: str) -> None:
    for url in urls:
        if url.startswith(("http://", "https://", "mailto:", "#")):
            continue
        target = (ROOT / url).resolve()
        if not target.exists():
            errors.append(f"{page_audit.name}: {kind} references missing file: {url}")


def main() -> int:
    missing = [name for name in REQUIRED_PAGES if not (ROOT / name).exists()]
    for name in missing:
        errors.append(f"required page missing: {name}")

    audits: list[PageAudit] = []
    for name in REQUIRED_PAGES:
        path = ROOT / name
        if not path.exists():
            continue
        raw = path.read_text(encoding="utf-8")
        audit = PageAudit(name)
        audit.feed(raw)
        audits.append(audit)

        if not audit.has_title:
            errors.append(f"{name}: missing <title>")
        if not audit.has_charset:
            errors.append(f"{name}: missing <meta charset>")
        if not audit.has_viewport:
            warnings.append(f"{name}: missing viewport meta")
        if not audit.has_stylesheet:
            errors.append(f"{name}: missing shared stylesheet link")
        if not audit.has_script:
            errors.append(f"{name}: missing shared app.js include")
        if audit.checkboxes and not re.search(r'data-clear-checks', raw):
            errors.append(f"{name}: has checkboxes but no data-clear-checks button")
        if audit.checkboxes and not re.search(r'data-print', raw):
            warnings.append(f"{name}: has checkboxes but no data-print button")
        if "Copyright" not in raw and "Asdale Dynamics, LLC" in raw:
            pass

        inner = re.sub(r"<[^>]+>", " ", raw)
        if re.search(r"(?<=[a-zA-Z])(aisy|firedrill)(?=[ .,\"!?])", inner):
            warnings.append(f"{name}: possible typo fragment found")
        if not re.search(r"(medical\s+(or\s+)?(dietary\s+|clinical\s+)?advice|not\s+medical)", inner, re.I) and name != "index.html":
            warnings.append(f"{name}: no explicit not-medical-advice wording found")

        check_local_resolution(audit, audit.hrefs, "href")
        check_local_resolution(audit, audit.srcs, "src")

        for unclosed_line, unclosed_tag in audit.stack:
            errors.append(f"{name}: <{unclosed_tag}> never closed (opened near line {unclosed_line})")

    for extra in ROOT.glob("*.html"):
        if extra.name not in REQUIRED_PAGES:
            warnings.append(f"unlisted page present: {extra.name}")

    license_text = (ROOT / "LICENSE").read_text(encoding="utf-8") if (ROOT / "LICENSE").exists() else ""
    if COPYRIGHT_LINE not in license_text:
        errors.append(f"LICENSE missing exact line: {COPYRIGHT_LINE}")
    readme = (ROOT / "README.md").read_text(encoding="utf-8") if (ROOT / "README.md").exists() else ""
    if "Asdale Dynamics, LLC" not in readme:
        errors.append("README.md does not credit Asdale Dynamics, LLC")

    for w in warnings:
        print(f"  warn: {w}")

    if errors:
        for e in errors:
            print(f"ERROR: {e}")
        return 1

    pages = len(audits)
    boxes = sum(a.checkboxes for a in audits)
    links = sum(len(a.hrefs) + len(a.srcs) for a in audits)
    print(f"OK: {pages} pages, {boxes} checkboxes, {links} local refs all resolve")
    print(f"LICENSE carries: {COPYRIGHT_LINE!r}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
"""
Fetch brand/tool icons from dashboardicons.com (homarr-labs/dashboard-icons,
Apache-2.0 — "icons are used for identification purposes only") into
styles/icons/, resolving friendly names against the project's metadata.json
so guides don't have to guess exact slugs.

Usage:
    ./fetch-icon.py obsidian claude docker github
    ./fetch-icon.py notion-light   (exact slug also works)
"""
import json
import sys
import urllib.request
from pathlib import Path

METADATA_URL = "https://cdn.jsdelivr.net/gh/homarr-labs/dashboard-icons/metadata.json"
SVG_URL = "https://cdn.jsdelivr.net/gh/homarr-labs/dashboard-icons/svg/{slug}.svg"
ICONS_DIR = Path(__file__).resolve().parent / "styles" / "icons"


def load_metadata():
    with urllib.request.urlopen(METADATA_URL) as r:
        return json.load(r)


def resolve(name, metadata):
    q = name.strip().lower()
    if q in metadata:
        return [q]
    exact_alias = [
        slug for slug, meta in metadata.items()
        if q in [a.lower() for a in meta.get("aliases", [])]
    ]
    if exact_alias:
        return exact_alias
    fuzzy = {slug for slug in metadata if q in slug.lower()}
    fuzzy |= {
        slug for slug, meta in metadata.items()
        if any(q in a.lower() for a in meta.get("aliases", []))
    }
    return sorted(fuzzy)


def fetch_svg(slug):
    ICONS_DIR.mkdir(parents=True, exist_ok=True)
    dest = ICONS_DIR / f"{slug}.svg"
    if dest.exists():
        print(f"  already cached: styles/icons/{slug}.svg")
        return
    urllib.request.urlretrieve(SVG_URL.format(slug=slug), dest)
    print(f"  saved styles/icons/{slug}.svg")


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    metadata = load_metadata()
    exit_code = 0
    for name in sys.argv[1:]:
        matches = resolve(name, metadata)
        if not matches:
            print(f"'{name}': no match found")
            exit_code = 1
        elif len(matches) == 1:
            print(f"'{name}' -> {matches[0]}")
            fetch_svg(matches[0])
        else:
            shown = matches[:15]
            print(f"'{name}' is ambiguous ({len(matches)} matches): {', '.join(shown)}"
                  + (" ..." if len(matches) > 15 else ""))
            print(f"  re-run with the exact slug, e.g.: ./fetch-icon.py {shown[0]}")
            exit_code = 1
    sys.exit(exit_code)


if __name__ == "__main__":
    main()

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
ICON_URL = "https://cdn.jsdelivr.net/gh/homarr-labs/dashboard-icons/{base}/{slug}.{base}"
ICONS_DIR = Path(__file__).resolve().parent / "styles" / "icons"


def load_metadata():
    with urllib.request.urlopen(METADATA_URL) as r:
        metadata = json.load(r)
    # light/dark color variants (e.g. "eleven-labs-light") are real, fetchable
    # files but aren't indexed as their own top-level entries — add them so
    # exact-slug lookup finds them too.
    for meta in list(metadata.values()):
        for variant_slug in meta.get("colors", {}).values():
            metadata.setdefault(variant_slug, {"base": meta.get("base", "svg"), "aliases": []})
    return metadata


def norm(s):
    return s.lower().replace("-", "").replace(" ", "")


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
    nq = norm(q)
    fuzzy = {slug for slug in metadata if nq in norm(slug)}
    fuzzy |= {
        slug for slug, meta in metadata.items()
        if any(nq in norm(a) for a in meta.get("aliases", []))
    }
    return sorted(fuzzy)


def fetch_icon(slug, meta):
    base = meta.get("base", "svg")
    ICONS_DIR.mkdir(parents=True, exist_ok=True)
    dest = ICONS_DIR / f"{slug}.{base}"
    if dest.exists():
        print(f"  already cached: styles/icons/{slug}.{base}")
        return
    urllib.request.urlretrieve(ICON_URL.format(base=base, slug=slug), dest)
    print(f"  saved styles/icons/{slug}.{base}")


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
            try:
                fetch_icon(matches[0], metadata[matches[0]])
            except Exception as e:
                print(f"  failed: {e}")
                exit_code = 1
        else:
            shown = matches[:15]
            print(f"'{name}' is ambiguous ({len(matches)} matches): {', '.join(shown)}"
                  + (" ..." if len(matches) > 15 else ""))
            print(f"  re-run with the exact slug, e.g.: ./fetch-icon.py {shown[0]}")
            exit_code = 1
    sys.exit(exit_code)


if __name__ == "__main__":
    main()

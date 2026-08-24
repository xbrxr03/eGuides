# eGuides

Turns source material into polished, self-contained HTML eGuides for hosting
on the user's website. Sources are one of:

- an existing PDF guide that needs a quality upgrade
- screenshots of a carousel post
- a reel
- a YouTube video link

In every case the job is: extract the underlying material, then produce a
clean HTML eGuide from it.

Guides are reference material, not articles — keep prose minimal. The two
things that matter are copy-pastable code blocks (see `.code-block` below)
and clickable links. Don't pad with paragraphs.

## Structure

Each eGuide gets its own topic folder at the repo root, named as a kebab-case
slug of the topic (e.g. `intermittent-fasting/`):

    <topic-slug>/
        source/       # raw input: PDFs, screenshots, transcripts, video links — NOT tracked
        index.html    # the finished eGuide — tracked
        assets/       # images/css/js the eGuide itself uses — tracked

`source/` is gitignored repo-wide (see `.gitignore`), so `git add .` never
picks up raw material — only the finished guide and the assets it actually
uses get committed. This is also why the eGuide's own images/css must live
in `assets/`, not loose in `source/`.

## Adding a new eGuide

1. `./new-guide.sh <topic name>` — scaffolds `<topic-slug>/{source,assets}` and an empty `index.html`.
2. Drop the raw material into `<topic-slug>/source/`.
3. Build `<topic-slug>/index.html` (and `assets/`) from that material, using one of the design systems below.
4. Commit as usual — `source/` is excluded automatically.

## Design systems ("packs")

Shared visual styles live in `styles/<pack-name>/`, at the repo root — not
inside any one topic folder, since a pack is reused across many guides.
Unlike `source/`, everything under `styles/` IS tracked in git (it's shipped
output, not raw material). An eguide links to its pack with a relative
stylesheet path, e.g. from `<topic-slug>/index.html`:

    <link rel="stylesheet" href="../styles/grove/grove.css">
    <script src="../styles/grove/grove.js" defer></script>

Both tags are required if the guide uses code blocks — the CSS alone renders
`.code-block` but the copy button does nothing without `grove.js`.

### grove (default, current only pack)

Warm editorial look — graph-paper cream background, forest green as the
structural dark, one rationed coral accent, Fraunces serif for
headlines/body copy, JetBrains Mono for kickers/labels/code, Lobster script
for rare decorative accents. Originally built as the MotionAgent "Grove
Editorial" video pack; repurposed here for eGuides so reels and guides share
a look.

- `styles/grove/grove.css` — the actual stylesheet to `<link>`. Self-hosts
  its three fonts via `@font-face` (relative `fonts/*.woff2` paths), defines
  the full color/type token set as CSS custom properties, and ships utility
  classes for the pack's signature patterns: `.kicker` (numbered pill badge),
  `.card`, `.stat` (big numbers), `.lead`, `.mono`, `.script`, `.graph-paper`
  (grid background), `.icon-tile` (glossy beveled icon square), `.terminal`
  (dark floating card), `.code-block` + `.copy-btn` (copy-pastable code, see
  below). Add `class="grove"` on `<body>` and on any container that needs
  the type rules.
- `styles/grove/grove.js` — vanilla JS, no dependencies. Delegated click
  handler that wires up every `.copy-btn` on the page: copies its
  `.code-block`'s `<pre>` text via `navigator.clipboard`, falls back to a
  hidden-textarea + `execCommand('copy')` if Clipboard API is missing OR
  rejects (e.g. permission denied — confirmed this actually happens, not
  just a theoretical case), and flips the button to "Copied!" for 1.5s
  either way. Markup pattern:

      <div class="code-block">
        <button class="copy-btn" type="button">Copy</button>
        <pre>npm install -g some-cli-tool</pre>
      </div>

- `grove-editorial-design-system.html`, `Grove-Palette.svg`,
  `Grove-Typography.svg`, `Grove-Patterns.svg`, `Grove-ThumbnailExample.svg`
  — the original reference/mockup files the pack was exported from. Open
  these to see the intended look; `grove.css` is my distillation of them
  into real, linkable CSS.
- `grove.css`'s body-copy size (18px) and lead size (22px) are my own call —
  the source system was built for punchy short video slides, not long-form
  reading. Since guides run code-blocks/links first and prose is minimal
  anyway (see top of file), this mostly matters for the occasional one-line
  blurb — adjust if it reads too big/small once a real guide is built.

## Icons

Real brand/tool icons come from [dashboardicons.com](https://dashboardicons.com)
(GitHub: `homarr-labs/dashboard-icons`, Apache-2.0 — "icons are used for
identification purposes only and do not imply endorsement"). Never hand-draw
or invent a brand mark; either pull the real one or leave it out.

- `./fetch-icon.py <name> [<name>...]` — resolves friendly names against the
  project's live `metadata.json` (matches on slug, then exact alias, then
  fuzzy substring) and downloads the matched SVG into `styles/icons/<slug>.svg`.
  Exact slugs work too. An ambiguous name (e.g. `claude` matches both
  `anthropic`, the official logo, and `clawd`, a community mascot icon)
  prints all candidates instead of guessing — check what each one actually
  is (metadata.json has `aliases`/`categories`) before re-running with the
  exact slug. A name with no match prints "no match found"; don't substitute
  a lookalike. Some icons are PNG-only (metadata's `base` field) — the
  script saves those as `<slug>.png` instead of `.svg`, check the actual
  saved filename. Fuzzy matching can also resolve to an unrelated icon that
  merely shares the search word (e.g. `whisper` matched a generic
  speech-bubble icon for an unrelated "web-whisper" app, not OpenAI
  Whisper's branding) — glance at the downloaded file before using it, not
  just the slug name.
- Many icons have light/dark color variants (e.g. `eleven-labs-light` for
  use on a light background, vs. the base slug which is often white-on-
  transparent and invisible on `.tag`/paper backgrounds) — `fetch-icon.py`
  resolves these variant slugs directly even though they aren't top-level
  metadata entries. Watch for the reverse problem too: at least one variant
  file (`eleven-labs-light`) is actually a PNG despite living at a `.svg`-
  suffixed URL upstream — if a "downloaded successfully" file won't render,
  check its real magic bytes before assuming the script is wrong.
- `styles/icons/` is a shared cache like the rest of `styles/` — tracked in
  git, so guides that reference the same tool don't redownload it. Only
  icons an actual guide uses should live here; don't pre-fetch speculatively.
- Reference from a guide: `<img src="../styles/icons/<slug>.svg" alt="...">`
  — works well dropped into `.icon-tile` from the grove pack.

## Previewing locally

`.claude/launch.json` has a `static-preview` config (`python3 -m http.server
8934`) for the Claude Code browser preview tool — needed because relative
asset paths (fonts, `styles/...`) and `navigator.clipboard` don't behave the
same under a bare `file://` URL. Opening an eguide's `index.html` straight
from disk will look unstyled; serve the repo root and navigate to
`http://localhost:8934/<topic-slug>/` instead.

## Conventions log

- 2026-08-23 — design packs added: `styles/<pack-name>/`, tracked in git,
  referenced by relative path from each eguide.
- 2026-08-23 — guides are code-blocks + links first, prose is minimal;
  grove pack got `.code-block`/`.copy-btn`/`grove.js` and real link styling
  to match.
- 2026-08-23 — icons come from dashboardicons.com via `./fetch-icon.py`,
  cached in `styles/icons/`. Never fabricate a brand icon.

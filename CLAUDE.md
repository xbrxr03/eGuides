# eGuides

Turns source material into polished, self-contained HTML eGuides for hosting
on the user's website. Sources are one of:

- an existing PDF guide that needs a quality upgrade
- screenshots of a carousel post
- a reel
- a YouTube video link

In every case the job is: extract the underlying material, then produce a
clean HTML eGuide from it.

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
  (dark floating card). Add `class="grove"` on `<body>` and on any container
  that needs the type rules.
- `grove-editorial-design-system.html`, `Grove-Palette.svg`,
  `Grove-Typography.svg`, `Grove-Patterns.svg`, `Grove-ThumbnailExample.svg`
  — the original reference/mockup files the pack was exported from. Open
  these to see the intended look; `grove.css` is my distillation of them
  into real, linkable CSS.
- `grove.css`'s body-copy size (18px) and lead size (22px) are my own call —
  the source system was built for punchy short video slides, not long-form
  reading, so paragraph sizing for actual guide prose isn't specified
  upstream. Adjust if it reads too big/small once a real guide is built.

## Conventions log

- 2026-08-23 — design packs added (see above): `styles/<pack-name>/`,
  tracked in git, referenced by relative path from each eguide.

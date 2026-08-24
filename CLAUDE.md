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
3. Build `<topic-slug>/index.html` (and `assets/`) from that material.
4. Commit as usual — `source/` is excluded automatically.

## Conventions log

Nothing beyond the above yet — add rules here as they're decided.

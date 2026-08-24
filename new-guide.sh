#!/usr/bin/env bash
# Scaffold a new eGuide topic folder: <slug>/{source,assets} + empty index.html
set -euo pipefail

if [ $# -eq 0 ]; then
  echo "Usage: ./new-guide.sh <topic name>" >&2
  exit 1
fi

slug=$(echo "$*" | tr '[:upper:]' '[:lower:]' | tr -cs 'a-z0-9' '-' | sed 's/^-*//; s/-*$//')

if [ -e "$slug" ]; then
  echo "Folder '$slug' already exists." >&2
  exit 1
fi

mkdir -p "$slug/source" "$slug/assets"
touch "$slug/index.html"

echo "Created $slug/"

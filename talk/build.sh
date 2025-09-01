#!/bin/bash

set -e

build() {
  pandoc --lua-filter columns.lua \
    -t revealjs \
    --highlight-style zenburn \
    --css=slides.css \
    --syntax-definition emfatic.xml \
    -o index.html \
    -s "$1"
  echo Slides built
}

wait_for_change() {
  echo Waiting for change...
  if which inotifywait &>/dev/null; then
    # For Linux
    inotifywait -e modify *.md *.css *.xml
  else
    # For MacOS
    fswatch -1 --event=Updated *.md *.css *.xml
  fi
}

build slides.md
while :; do
  wait_for_change
  build slides.md
done

#!/bin/bash

set -e

build() {
  pandoc --lua-filter columns.lua -t revealjs -s "$1" --css=slides.css -o index.html
  echo Slides built
}

wait_for_change() {
  echo Waiting for change...
  if which inotifywait &>/dev/null; then
    # For Linux
    inotifywait -e modify *.md *.css
  else
    # For MacOS
    fswatch -1 --event=Updated *.md *.css
  fi
}

build *.md
while :; do
  wait_for_change
  build *.md
done

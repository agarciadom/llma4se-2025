#!/bin/bash

set -e

build() {
  pandoc -t revealjs -s "$1" -o index.html
  echo Slides built
}

wait_for_change() {
  echo Waiting for change...
  if which inotifywait &>/dev/null; then
    # For Linux
    inotifywait -e modify *.md
  else
    # For MacOS
    fswatch -1 --event=Updated *.md
  fi
}

build *.md
while :; do
  wait_for_change
  build *.md
done

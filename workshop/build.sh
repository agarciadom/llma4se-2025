#!/bin/bash

build() {
  pandoc -t revealjs -s mde-ci-slides.md -o index.html
}

build
while true; do
  inotifywait -e modify *.md
  build
done

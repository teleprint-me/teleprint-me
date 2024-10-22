#!/usr/bin/env bash

# Copyright (C) 2020 Austin Berrio

# Configuration variables
config=".prettierrc"
template="template.html"
filename="Teach-Yourself-Programming-in-Ten-Years"
markdown="${filename}.md"
html="${filename}.html"

# Remove old HTML file, if it exists
rm -f "$html"

# Convert Markdown to HTML with Pandoc, disabling smart quotes
pandoc -f markdown-smart -t html "$markdown" -o "$html" \
    --template="$template" \
    --css=style.css \
    --metadata pagetitle="Teach Yourself Programming in Ten Years"

# Format HTML using Prettier with specified config
prettier --ignore-path --config "$config" --write "$html"

#!/usr/bin/env bash

# Copyright (C) 2020 Austin Berrio

echo "generating static content..."

# Paths
config=".prettierrc"
template_main="static/templates/main.html"
template_mathjax="static/templates/mathjax.html"
css="static/styles/style.css"

# Generate blog articles
mkdir -p static/views/blog
for file in docs/blog/*.md; do
    filename=$(basename "$file" .md)
    echo "generating ${filename}"
    pandoc -f markdown-smart -t html "$file" \
        --template="$template_main" --css="$css" \
        -o "static/views/blog/$filename.html"
    prettier --ignore-path --config "$config" \
        --write "static/views/blog/$filename.html"
done

# Generate technical articles
mkdir -p static/views/technical
for file in docs/technical/*.md; do
    filename=$(basename "$file" .md)
    echo "generating ${filename}"
    pandoc -f markdown+tex_math_dollars -t html "$file" \
        --template="$template_mathjax" --css="$css" \
        -o "static/views/technical/$filename.html"
    prettier --ignore-path --config "$config" \
        --write "static/views/technical/$filename.html"
done

# Generate core views (like index.md)
for file in docs/views/*.md; do
    filename=$(basename "$file" .md)
    echo "generating ${filename}"
    pandoc -f markdown-smart -t html "$file" \
        --template="$template_main" --css="$css" \
        -o "static/views/$filename.html"
    prettier --ignore-path --config "$config" \
        --write "static/views/$filename.html"
done

# Copy index.html to the root if needed
cp static/views/index.html ./index.html

echo "done!"

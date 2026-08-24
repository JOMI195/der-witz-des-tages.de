#!/bin/sh
set -e

HTML_DIR=/usr/share/nginx/html
SEO_DIR="$HTML_DIR/seo"

mkdir -p "$SEO_DIR"

# The volume is created from the backend image, so it belongs to the backend's
# app user. Anything created here as root has to keep that owner, otherwise the
# backend cannot write its renders.
OWNER=$(stat -c '%u:%g' "$SEO_DIR")
mkdir -p "$SEO_DIR/galerie"

# Renders from the previous deployment reference the old hashed assets, so they
# are dropped: nginx falls back to the build output until the backend re-renders.
rm -f "$SEO_DIR/index.html" "$SEO_DIR/galerie/index.html" "$SEO_DIR"/galerie/page-*.html

# The analytics tracker is injected into the served files at runtime
# (scripts/inject-umami-tracker.sh), so a fresh template would drop it and every
# scheduled render after a restart would come out untracked. Carry it over.
TRACKER=/tmp/umami-block.html
rm -f "$TRACKER"
if [ -f "$SEO_DIR/template.html" ] && grep -q "umami:start" "$SEO_DIR/template.html"; then
  sed -n '/<!-- umami:start -->/,/<!-- umami:end -->/p' "$SEO_DIR/template.html" > "$TRACKER"
fi

# The backend renders on top of the deployed build (matching asset hashes).
# seo-template.html is the pristine copy with an empty #root; index.html is
# already prerendered and only serves as a fallback.
if [ -f "$HTML_DIR/seo-template.html" ]; then
  cp "$HTML_DIR/seo-template.html" "$SEO_DIR/template.html"
else
  cp "$HTML_DIR/index.html" "$SEO_DIR/template.html"
fi

if [ -s "$TRACKER" ] && ! grep -q "data-website-id" "$SEO_DIR/template.html"; then
  echo "restoring the umami tracker in seo/template.html"
  awk "/<\/head>/ { while ((getline l < \"$TRACKER\") > 0) print l } { print }" \
      "$SEO_DIR/template.html" > "$SEO_DIR/template.html.new"
  mv "$SEO_DIR/template.html.new" "$SEO_DIR/template.html"
fi
rm -f "$TRACKER"

chown -R "$OWNER" "$SEO_DIR"

exec nginx -g 'daemon off;'

#!/usr/bin/env bash
#
# download-ghl-assets.sh -- pull the Identity 2.0 images off GoHighLevel
# before that account is touched.
#
#     bash migration/download-ghl-assets.sh
#
# WHY THIS IS URGENT
# ------------------
# The Identity 2.0 Challenge lived ONLY in the GoHighLevel page builder, at
# start.parallaxxtransformations.com. Its DNS record is already deleted, so
# the page is gone; the copy survives solely because it was harvested into
# migration/harvested/harvested-identity-2-0-challenge.html before that
# happened.
#
# THE IMAGES WERE NOT HARVESTED. All seven still sit on GoHighLevel's CDN,
# and they are the same one-copy-left situation the words were in a fortnight
# ago. The moment that subscription lapses they are unrecoverable, and unlike
# the copy there is nothing to retype them from.
#
# Run this before cancelling anything at GHL.
#
# It skips what it already has, so re-running after a failure is safe, and it
# reports a non-zero exit if any file failed.

set -u
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
OUT="$HERE/ghl-assets"
mkdir -p "$OUT"

BASE="https://images.leadconnectorhq.com/image/f_webp/q_80/r_1200/u_https://assets.cdn.filesafe.space/Nja8qXnwLqNjaNTJVf5T/media"

# media id -> the name it gets locally. Renamed on the way in: an id like
# 6546895d92b8578f008de2eb tells nobody anything a year from now, and these
# are the last copies.
FILES="
65485084cc187bbcafcd4228.png:identity-hero.png
6546807b92b8573d358dd1df.png:identity-02.png
6546895d92b8578f008de2eb.png:identity-03.png
6546895da075686010da00f2.png:identity-04.png
6546864592b857ab448de117.png:identity-05.png
654a8aae24fa462a22afe733.png:identity-06.png
654a93617b3caa4ddf894f0b.png:identity-07.png
"

ok=0; skip=0; fail=0
for pair in $FILES; do
  id="${pair%%:*}"; name="${pair##*:}"
  dest="$OUT/$name"
  if [ -s "$dest" ]; then
    echo "  skip    $name"
    skip=$((skip+1))
    continue
  fi
  # The CDN serves webp regardless of the .png in the id, so ask for the
  # original bytes and let file(1) tell us what actually arrived.
  if curl -fsSL --max-time 60 "$BASE/$id" -o "$dest" 2>/dev/null; then
    echo "  got     $name  ($(wc -c < "$dest" | tr -d ' ') bytes, $(file -b --mime-type "$dest"))"
    ok=$((ok+1))
  else
    echo "  FAILED  $name"
    rm -f "$dest"
    fail=$((fail+1))
  fi
done

echo
echo "got: $ok   skipped: $skip   failed: $fail"
echo "into: $OUT"

if [ "$fail" -ne 0 ]; then
  echo
  echo "Some files failed. If they 404, the GHL account may already be gone and"
  echo "those images are unrecoverable -- say so rather than rebuilding around"
  echo "a gap nobody knows about."
  exit 1
fi

echo
echo "Next: tell Claude they are down, and they get renamed, mapped and"
echo "localised the same way the Wix assets were."

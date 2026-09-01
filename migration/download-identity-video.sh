#!/usr/bin/env bash
#
# download-identity-video.sh -- pull the Identity 2.0 video and its poster off
# Wix, so the page survives the subscription ending.
#
#     bash migration/download-identity-video.sh
#
# WHY THIS IS SEPARATE FROM download-wix-assets.sh
# ------------------------------------------------
# That script works from asset-map.json, which was generated from the ten
# bundles that existed when the migration was planned. The Identity 2.0 page
# was never in the build, so its two Wix assets were never in the map and have
# never been downloaded by anything.
#
# They are the last two Wix dependencies on the site. A 1080p VSL is not
# something that can be reconstructed from a harvest the way copy can, so this
# is the one asset on the site whose loss would be permanent.
#
# After this runs:
#     python3 migration/map-new-assets.py "../Parallaxx Identity 2.0.dc.html" --apply
# and build-site.py will localise both to /assets/ like everything else.

set -u
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VID="$HERE/wix-assets/video"
IMG="$HERE/wix-assets/img"
mkdir -p "$VID" "$IMG"

VIDEO_URL="https://video.wixstatic.com/video/111174_fe0f4187e6ec49828451a3e21ca58f1d/1080p/mp4/file.mp4"
POSTER_URL="https://static.wixstatic.com/media/111174_74b26341d59e409799eed10e853ae4e7~mv2.png"

VIDEO_OUT="$VID/identity-2-0-vsl.mp4"
POSTER_OUT="$IMG/identity-2-0-poster.png"

fail=0

if [ -s "$VIDEO_OUT" ]; then
  echo "  skip    identity-2-0-vsl.mp4 ($(wc -c < "$VIDEO_OUT" | tr -d ' ') bytes)"
else
  echo "  getting identity-2-0-vsl.mp4 ... (1080p, this is the big one)"
  if curl -fsSL --max-time 900 "$VIDEO_URL" -o "$VIDEO_OUT"; then
    echo "  got     identity-2-0-vsl.mp4  $(wc -c < "$VIDEO_OUT" | tr -d ' ') bytes"
  else
    echo "  FAILED  identity-2-0-vsl.mp4"; rm -f "$VIDEO_OUT"; fail=1
  fi
fi

if [ -s "$POSTER_OUT" ]; then
  echo "  skip    identity-2-0-poster.png"
else
  if curl -fsSL --max-time 120 "$POSTER_URL" -o "$POSTER_OUT"; then
    echo "  got     identity-2-0-poster.png  $(wc -c < "$POSTER_OUT" | tr -d ' ') bytes"
  else
    echo "  FAILED  identity-2-0-poster.png"; rm -f "$POSTER_OUT"; fail=1
  fi
fi

echo
if [ "$fail" -ne 0 ]; then
  echo "Something failed. If Wix is already cancelled, the video may be gone --"
  echo "say so rather than shipping a VSL page with a dead player."
  exit 1
fi

echo "Both down. Next:"
echo "  python3 migration/map-new-assets.py \"../Parallaxx Identity 2.0.dc.html\" --apply"
echo "  python3 migration/build-site.py --local"

#!/usr/bin/env bash
# Re-fetches every video at the resolution we chose, and PARKS the 1080p
# originals rather than deleting them.
#
# WHY PARK RATHER THAN DELETE
# ---------------------------
# Wix is being cancelled in a few weeks. After that video.wixstatic.com stops
# answering, and any resolution not already on disk is gone for good. The 1080p
# files are the best copies that exist outside your original footage, so they
# move to _originals/ (gitignored, never pushed) instead of being removed. Costs
# nothing but disk, and keeps the upgrade path open after Wix is gone.
#
# THE CHOICE
# ----------
# Cloudflare Pages caps a single file at 25 MiB. From the probe:
#   4e1bcc7d4c  720p   9MB      59a18a858d  720p  13MB
#   7af3a35d66  480p  18MB      c76bb418f8  480p  17MB   (35MB / 32MB at 720p)
#
# To upgrade a clip later: change its resolution in the src field of
# asset-map.json and re-run. If the file lands over 25 MiB this script says OVER
# — it cannot live on Pages, and the options are R2, or an ffmpeg re-encode of
# the parked 1080p original, which usually beats Wix's encoder at the same size.
#
# Note the page bundles are untouched. They still reference the 1080p Wix URL;
# the build maps that reference to whichever local file we put here.
set -u
cd "$(dirname "$0")"

CAP=26214400   # 25 MiB
ok=0; over=0; fail=0
mkdir -p wix-assets/video _originals

get(){
  local url="$1" out="wix-assets/$2"
  if curl -fsSL --retry 3 --retry-delay 2 -A "Mozilla/5.0" "$url" -o "$out"; then
    local b; b=$(wc -c < "$out" | tr -d " ")
    if [ "$b" -gt "$CAP" ]; then
      printf "OVER  %-32s %5sMB  over the 25MB cap\n" "$2" "$(( b / 1048576 ))"; over=$((over+1))
    else
      printf "ok    %-32s %5sMB\n" "$2" "$(( b / 1048576 ))"; ok=$((ok+1))
    fi
  else
    printf "FAIL  %-32s\n" "$2"; rm -f "$out"; fail=$((fail+1))
  fi
}

get "https://video.wixstatic.com/video/111174_0c316e5ec9a44931a1f94fe8f9bac6a6/480p/mp4/file.mp4" "video/video-0c316e5ec9-480p.mp4"
get "https://video.wixstatic.com/video/111174_2dd20e0c35d3467e8957b2e57cd6d9d9/480p/mp4/file.mp4" "video/video-2dd20e0c35-480p.mp4"
get "https://video.wixstatic.com/video/111174_469a5c83d5ae49ddb30780eb2ca3a85d/480p/mp4/file.mp4" "video/video-469a5c83d5-480p.mp4"
get "https://video.wixstatic.com/video/111174_495d92c709a74ae199756df31216a61e/480p/mp4/file.mp4" "video/video-495d92c709-480p.mp4"
get "https://video.wixstatic.com/video/111174_4e1bcc7d4c634401adae988048a9cb1b/720p/mp4/file.mp4" "video/video-4e1bcc7d4c-720p.mp4"
get "https://video.wixstatic.com/video/111174_59a18a858df34f798fbeb5ae8d5b19b8/720p/mp4/file.mp4" "video/video-59a18a858d-720p.mp4"
get "https://video.wixstatic.com/video/111174_7af3a35d66374744965fbdaa2f9a3a9b/480p/mp4/file.mp4" "video/video-7af3a35d66-480p.mp4"
get "https://video.wixstatic.com/video/111174_863af1d4805a4c24ad33cb35ff088881/480p/mp4/file.mp4" "video/video-863af1d480-480p.mp4"
get "https://video.wixstatic.com/video/111174_96f86443b9e244999b01cd1e8172bd81/720p/mp4/file.mp4" "video/video-96f86443b9-720p.mp4"
get "https://video.wixstatic.com/video/111174_a6961c80d0464fbe8437a38fa69071da/720p/mp4/file.mp4" "video/video-a6961c80d0-720p.mp4"
get "https://video.wixstatic.com/video/111174_c76bb418f85d49579bd90c14e6addf79/480p/mp4/file.mp4" "video/video-c76bb418f8-480p.mp4"

# Park the superseded 1080p files. Kept, not deleted — see the note above.
echo
for f in wix-assets/video/*-1080p.mp4; do
  [ -e "$f" ] || continue
  echo "parking $(basename "$f") ($(du -h "$f" | cut -f1))"
  mv -f "$f" _originals/
done

echo
echo "=============================="
echo "under cap: $ok"
echo "over cap:  $over"
echo "failed:    $fail"
echo "shipping:  $(du -sh wix-assets/video 2>/dev/null | cut -f1) of video"
echo "parked:    $(du -sh _originals 2>/dev/null | cut -f1) of 1080p masters (never pushed)"
echo "assets:    $(find wix-assets -type f | wc -l | tr -d " ") files (expect 68)"
echo "=============================="

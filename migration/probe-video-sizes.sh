#!/usr/bin/env bash
# Probes every video at each resolution Wix offers and prints the sizes.
# HEAD requests only — downloads nothing. Runs in a few seconds.
#
# Why this matters: Cloudflare Pages caps a single file at 25 MiB. If 720p fits
# under that cap, the whole site lives on Pages alone and R2 is unnecessary —
# one product instead of three, no media subdomain, no payment card.
set -u
cd "$(dirname "$0")"

size_of() {
  curl -sIL -A "Mozilla/5.0" --max-time 20 \
       "https://video.wixstatic.com/video/$1/$2/mp4/file.mp4" \
    | tr -d '\r' \
    | grep -i '^content-length:' \
    | tail -1 \
    | awk '{print $2}'
}

printf "%-12s %-20s %9s %9s %9s %9s\n" ID PAGE 1080p 720p 480p 360p
printf '%.0s-' {1..74}; echo

t1080=0; t720=0; t480=0
while IFS=$'\t' read -r id page; do
  [ -z "$id" ] && continue
  printf "%-12s %-20s" "${id:7:10}" "$page"
  for res in 1080p 720p 480p 360p; do
    b=$(size_of "$id" "$res")
    if [ -z "$b" ]; then
      printf "%9s" "-"
    else
      mb=$(( b / 1048576 ))
      case $res in
        1080p) t1080=$((t1080+b));;
        720p)  t720=$((t720+b));;
        480p)  t480=$((t480+b));;
      esac
      if [ "$b" -gt 26214400 ]; then printf "%8sMB!" "$mb"; else printf "%8sMB " "$mb"; fi
    fi
  done
  echo
done < vids.tsv

echo
echo "TOTALS   1080p: $((t1080/1048576))MB   720p: $((t720/1048576))MB   480p: $((t480/1048576))MB"
echo
echo "! = over the 25 MiB Cloudflare Pages per-file cap (would need R2)"

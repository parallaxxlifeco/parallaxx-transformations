#!/usr/bin/env bash
# Fetches the 4 assets the first run missed.
#
# Not your fault and not Wix rate-limiting: the URL extractor stopped at the
# first "(", because a closing paren normally ends a CSS url(...) wrapper.
# Four Wix filenames genuinely contain parentheses — "Parallaxx Transformation
# Logo Design White (1).png" and friends — so those four requests went out
# truncated and Wix answered 403. The extractor now counts the parens and only
# strips one that is unbalanced.
#
# The other 64 files are unaffected and keep their names. This script only adds.
set -u
cd "$(dirname "$0")"
mkdir -p wix-assets/img
ok=0; fail=0
dl(){
  local url="$1" out="wix-assets/$2"
  if [ -s "$out" ]; then echo "skip  $2"; ok=$((ok+1)); return; fi
  if curl -fsSL --retry 3 --retry-delay 2 -A "Mozilla/5.0" "$url" -o "$out"; then
    echo "ok    $2  ($(du -h "$out" | cut -f1))"; ok=$((ok+1))
  else
    echo "FAIL  $2"; rm -f "$out"; fail=$((fail+1))
  fi
}

dl "https://static.wixstatic.com/media/e1784d_8540d4c3c9b94831a4e2a8533ed1d15b~mv2.png/v1/crop/x_0,y_463,w_1080,h_166/fill/w_300,h_46,al_c,q_85,enc_avif,quality_auto/contier%20(1).png" "img/contier-20-1-crop1080x166-0-463.png"
dl "https://static.wixstatic.com/media/e1784d_b79c8e912d16444584b8a4726542b886~mv2.png/v1/crop/x_828,y_138,w_1046,h_1225/fill/w_900,h_1400,al_c,q_90,enc_avif,quality_auto/What%20you%20resist%20persists_%20(3).png" "img/what-20you-20resist-20persists-20-3-crop1046x1225-828-138.png"
dl "https://static.wixstatic.com/media/e1784d_fe3c841c471f47d088f0cd631a89d883~mv2.png/v1/fill/w_260,h_57,al_c,q_90,enc_auto/Parallaxx%20Transformation%20Logo%20Design%20White%20(1).png" "img/parallaxx-20transformation-20logo-20design-20white-20-1.png"
dl "https://static.wixstatic.com/media/e1784d_fe3c841c471f47d088f0cd631a89d883~mv2.png/v1/fill/w_260,h_57,al_c,q_90,enc_avif,quality_auto/Parallaxx%20Transformation%20Logo%20Design%20White%20(1).png" "img/parallaxx-20transformation-20logo-20design-20white-20-1-2.png"

# Remove the empty placeholders the first run left behind, if any.
rm -f wix-assets/img/*.jpg.part 2>/dev/null

echo
echo "=============================="
echo "added:  $ok"
echo "failed: $fail"
echo "=============================="
echo "Total in wix-assets: $(find wix-assets -type f | wc -l | tr -d " ") of 68"

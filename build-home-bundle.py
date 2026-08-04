#!/usr/bin/env python3
"""
Build parallaxx-home.js from "Parallaxx Home.dc.html".

This is the FRONT DOOR: the routing page at /, which supersedes
"Parallaxx Home Sort.dc.html". It sends the right person to /men or /women
and gives them a reason to trust Daniel on the way past.
  Bundle : parallaxx-home.js
  Tag    : parallaxx-home
  Preview: home.html
Its two destinations are avatar pages with builds of their own:
"Parallaxx Home Men.dc.html" and "Parallaxx Home Women.dc.html".

The .dc.html is the SOURCE OF RECORD. This script converts it into the
self-contained shadow-DOM custom element that Wix loads. Never hand-edit
parallaxx-home.js -- it is overwritten every run.

    python3 build-home-bundle.py

HOW THIS BUILD DIFFERS FROM THE OTHER TWO, AND WHY
No GSAP and no Lenis. The avatar pages animate on scroll and need both; this
page has one CSS entrance and nothing else, on purpose. A routing page cannot
have content that depends on an animation completing, and the men's page lost
its headline twice to tweens stranded by a ScrollTrigger refresh. So there is
no loadLibs step and boot() runs immediately rather than waiting on a CDN.
That is worth real milliseconds on the highest-traffic URL on the site.

WHAT STILL HAS TO BE HANDLED, same as the others
  1. document.getElementById() returns null inside a shadow root.
  2. @font-face declared inside a shadow tree is ignored by Chrome, so fonts
     are injected into document.head separately.
  3. Wix wraps the element in ancestors that keep their own height, so they
     get collapsed after mount.

The guards below fail the build rather than shipping any of those, and rather
than shipping a page whose two images are still placeholders.
"""
import re, sys, pathlib

HERE = pathlib.Path(__file__).parent
SRC  = HERE / "Parallaxx Home.dc.html"
OUT  = HERE / "parallaxx-home.js"

src = SRC.read_text(encoding="utf-8")
lines = src.split("\n")

# ---- guards on the SOURCE -------------------------------------------------

# THE IMAGE GUARD, and it is specific to this page. The hero portrait and the
# full-bleed plate behind the record are both Wix Media URLs that have to be
# pasted in after upload. A bundle shipped with the placeholders still in it
# renders a page with a broken portrait as the first thing a cold visitor
# sees, which is the exact opposite of what this page is for.
# LUMIOS_MARKER_WOFF2_URL is exempt and always has been: the stack falls
# through to Permanent Marker on purpose, so the page is correct without it.
# Every other placeholder is a hard stop.
SOFT = {"LUMIOS_MARKER_WOFF2_URL"}
found = set(re.findall(r"[A-Z][A-Z0-9_]*_URL", src))
hard = sorted(found - SOFT)
if hard:
    sys.exit("FAIL: image placeholder(s) still in the source: " + ", ".join(hard)
             + ".\n      Upload to Wix Media and paste the URLs in before building."
               "\n        DANIEL_CLEAR_JPG_URL  -> daniel-clear.jpg, the hero portrait"
               "\n        STAGE_ROOM_JPG_URL    -> home-plate-room.jpg, the plate "
               "behind the record")
if found & SOFT:
    print("note: Lumios Marker not uploaded; the hand lines fall back to "
          "Permanent Marker. Intentional, not a failure.")

def style_block(open_line_idx):
    close = next(k for k in range(open_line_idx + 1, len(lines))
                 if lines[k].strip() == "</style>")
    return "\n".join(lines[open_line_idx + 1:close])

opens = [i for i, l in enumerate(lines) if l.strip() == "<style>"]
if len(opens) < 2:
    sys.exit("FAIL: expected a @font-face <style> and at least one page <style>.")
# Block 0 is the @font-face, which has to go into document.head separately.
# EVERY other block is page CSS and gets concatenated: the page sheet, then
# the baked-in footer.
FONTFACE = style_block(opens[0])
CSS = "\n\n".join(style_block(i) for i in opens[1:])

h0 = next(i for i, l in enumerate(lines) if l.startswith('<div id="px-root">'))
h1 = next(i for i, l in enumerate(lines) if l.rstrip() == "</x-dc>")
HTML = "\n".join(lines[h0:h1]).rstrip()

# Only CSS and HTML are embedded in template literals, so only they can be
# broken by a backtick. The JS body is emitted as raw source, where a backtick
# inside a comment is harmless.
for _label, _chunk in (("CSS", CSS), ("HTML", HTML)):
    if "`" in _chunk:
        sys.exit(f"FAIL: backtick inside the {_label}. It would terminate the "
                 f"template literal and destroy the block.")
    if "${" in _chunk:
        sys.exit(f"FAIL: '${{' inside the {_label} would interpolate.")

# This page ships no GSAP. If a ScrollTrigger ever appears here, something has
# been pasted in from an avatar page and the no-JS-required rule is broken.
if "ScrollTrigger" in src or "gsap" in src:
    sys.exit("FAIL: GSAP on the routing page. Nothing on this page may depend "
             "on an animation completing. See the header comment.")

js = src[src.index('<script type="text/x-dc"'):]
js = js[js.index(">") + 1:js.index("</script>")]
body = js[js.index("componentDidMount(){") + len("componentDidMount(){"):]
body = body[:body.rindex("renderVals()")].rstrip()
body = body[:body.rindex("}")].rstrip()          # drop componentDidMount's closer

body = body.replace(
    "    const root = document.getElementById('px-root');\n    if(!root) return;\n", "")
body = body.replace("document.getElementById(", "root.getElementById(")

# ---- guards on the OUTPUT -------------------------------------------------
if "const root =" in body:
    sys.exit("FAIL: local root binding survived; it would shadow boot()'s parameter.")
if "document.getElementById" in body:
    sys.exit("FAIL: a document.getElementById survived the rewrite.")

font_links = re.findall(r'<link href="([^"]+)" rel="stylesheet">',
                        "\n".join(lines[:opens[0] + 30]))
fonts = "\n".join(
    "    var f%d=document.createElement('link'); f%d.rel='stylesheet'; f%d.href=%r; "
    "document.head.appendChild(f%d);" % (i, i, i, u, i)
    for i, u in enumerate(font_links))

OUT.write_text("""/* PARALLAXX TRANSFORMATIONS - Home, the front door. Wix Custom Element. Tag: parallaxx-home.
   GENERATED by build-home-bundle.py from "Parallaxx Home.dc.html".
   DO NOT EDIT THIS FILE - edit the .dc.html and rerun the build.
   In the Wix editor: turn the site Header + Footer OFF for this page. */
(function(){
  if (customElements.get('parallaxx-home')) return;

  var CSS = `%s`;

  var HTML = `%s`;

  function addFonts(){
    if (document.getElementById('px-fonts-home')) return;
    var p1=document.createElement('link'); p1.rel='preconnect'; p1.href='https://fonts.googleapis.com'; document.head.appendChild(p1);
    var p2=document.createElement('link'); p2.rel='preconnect'; p2.href='https://fonts.gstatic.com'; p2.crossOrigin=''; document.head.appendChild(p2);
%s
    /* @font-face has to live in the DOCUMENT, not the shadow root. Chrome
       ignores font-face rules declared inside a shadow tree. */
    var ff=document.createElement('style'); ff.id='px-fonts-home'; ff.textContent=`%s`; document.head.appendChild(ff);
  }

  /* NO loadLibs(). This page ships no GSAP and no Lenis, so boot() runs
     immediately instead of waiting on two CDN round trips. Every word is
     already visible before any script runs. */

  /* This rewrites ancestor heights, which moves every scroll position on the
     page. Returns whether it actually changed anything so the caller can
     avoid doing it for nothing. */
  function collapseAncestors(host){
    var changed = false;
    try{ var h=host.getBoundingClientRect().height; if(h<50) return false;
      var n=host.parentElement,guard=0;
      while(n && n!==document.body && guard++<14){ if(n.getBoundingClientRect().height>h+600){ n.style.height='auto'; n.style.minHeight='0px'; changed = true; } n=n.parentElement; }
    }catch(e){}
    return changed;
  }

  function boot(root){
    if(!root || !root.getElementById('px-root')) return;
%s
  }

  class ParallaxxHome extends HTMLElement {
    connectedCallback(){
      if (this._mounted) return; this._mounted = true;
      addFonts();
      var shadow = this.attachShadow({mode:'open'});
      shadow.innerHTML = '<style>'+CSS+'</style>'+HTML;
      var host = this;
      try{ boot(shadow); }catch(e){ console.error('[px] boot failed:', e); }
      requestAnimationFrame(function(){ collapseAncestors(host); });
      [400,1200,2500].forEach(function(t){ setTimeout(function(){ collapseAncestors(host); }, t); });
      window.addEventListener('resize', function(){ collapseAncestors(host); }, {passive:true});
    }
  }
  customElements.define('parallaxx-home', ParallaxxHome);
})();
""" % (CSS, HTML, fonts, FONTFACE, body), encoding="utf-8")

print(f"built {OUT.name}  css={len(CSS)}  html={len(HTML)}  boot={len(body)}  fonts={len(font_links)}")

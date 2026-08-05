#!/usr/bin/env python3
"""
Build parallaxx-testimonials.js from "Parallaxx Testimonials v4.dc.html".

  Bundle : parallaxx-testimonials.js
  Tag    : parallaxx-testimonials
  Page   : /testimonials-daniel-lawson

The .dc.html is the SOURCE OF RECORD. This script converts it into the
self-contained shadow-DOM custom element that Wix loads. Never hand-edit
parallaxx-testimonials.js -- it is overwritten every run.

    python3 build-testimonials-bundle.py

WHY A BUILD STEP AT ALL
The .dc.html runs inside Wix's Design Code runtime, where the component is
in the light DOM. The deployed bundle runs inside a shadow root, and the
differences fail SILENTLY rather than throwing:

  1. document.getElementById() returns null inside a shadow root, so every
     element lookup has to go through the root instead.
  2. @font-face declared inside a shadow tree is ignored by Chrome, so the
     fonts have to be injected into document.head separately.
  3. A backtick or a "${" anywhere in the CSS or HTML terminates the
     template literal the bundle embeds them in, and destroys the block.

The guards below fail the build rather than shipping any of those.

WHAT THIS PAGE DOES NOT NEED
No GSAP, no ScrollTrigger, no Lenis. The reveal is an IntersectionObserver
and the filter is plain DOM, so there is nothing to load from a CDN and no
string-selector trigger to resolve against the wrong document. That is
deliberate: this is a PROOF page, and no part of it may depend on a library
arriving. See the note at the head of the .dc.html.
"""
import re, sys, pathlib

HERE = pathlib.Path(__file__).parent
SRC  = HERE / "Parallaxx Testimonials v4.dc.html"
OUT  = HERE / "parallaxx-testimonials.js"

src = SRC.read_text(encoding="utf-8")
lines = src.split("\n")

# ---- extract ---------------------------------------------------------------
def style_block(open_idx):
    close = next(k for k in range(open_idx + 1, len(lines))
                 if lines[k].strip() == "</style>")
    return "\n".join(lines[open_idx + 1:close])

opens = [i for i, l in enumerate(lines) if l.strip() == "<style>"]
if len(opens) < 2:
    sys.exit("FAIL: expected a @font-face <style> and at least one page <style>.")
# Block 0 is @font-face and has to reach document.head on its own. Every
# other block is page or chrome CSS and gets concatenated in source order:
# the page sheet, then PtNav v3, then PtFooter v3.
FONTFACE = style_block(opens[0])
CSS = "\n\n".join(style_block(i) for i in opens[1:])

h0 = next(i for i, l in enumerate(lines) if l.startswith('<div id="px-root">'))
h1 = next(i for i, l in enumerate(lines) if l.rstrip() == "</x-dc>")
HTML = "\n".join(lines[h0:h1]).rstrip()
# The JSON-LD block sits between the markup and </x-dc>. It must NOT ride
# into the shadow root: structured data is only read from the document, and
# a <script type="application/ld+json"> inside a shadow tree is invisible to
# every crawler. It is emitted into document.head instead, below.
LD = ""
m = re.search(r'<script type="application/ld\+json">(.*?)</script>', HTML, re.S)
if m:
    LD = m.group(1).strip()
    HTML = HTML[:m.start()] + HTML[m.end():]
HTML = HTML.rstrip()

# The page's behaviour lives in a plain <script>, not in componentDidMount:
# three named initialisers plus a bootstrap that binds them to `document`.
# The functions come across as-is; the bootstrap is dropped, because in the
# bundle the element decides when to boot and against which root.
plain = re.findall(r"<script>(.*?)</script>", src, re.S)
if not plain:
    sys.exit("FAIL: no plain <script> block found.")
BODY = plain[0]
cut = BODY.find("/* Plain-page bootstrap.")
if cut < 0:
    sys.exit("FAIL: could not find the plain-page bootstrap marker to cut at. "
             "If that comment was reworded, update this build.")
BODY = BODY[:cut].rstrip()

# ---- guards ----------------------------------------------------------------
for label, chunk in (("CSS", CSS), ("HTML", HTML), ("JSON-LD", LD)):
    if "`" in chunk:
        sys.exit(f"FAIL: backtick inside the {label}. It would terminate the "
                 f"template literal and destroy the block.")
    if "${" in chunk:
        sys.exit(f"FAIL: '${{' inside the {label} would interpolate.")

# Every element lookup has to be scoped. document.addEventListener is fine and
# expected -- the nav's outside-click and Escape handlers listen on the whole
# document on purpose -- so only getElementById/querySelector are checked.
leaks = re.findall(r"document\.(?:getElementById|querySelector(?:All)?)\([^)]*\)", BODY)
if leaks:
    sys.exit("FAIL: unscoped document lookup(s) survived into the bundle body. "
             "Inside a shadow root these return null and fail silently:\n  "
             + "\n  ".join(sorted(set(leaks))))
for fn in ("function initTestimonials(", "function initPtNav(", "function initPtFooter("):
    if fn not in BODY:
        sys.exit(f"FAIL: {fn}...) missing from the bundle body.")

if "WIX_COVER_URL" in HTML:
    n = HTML.count("WIX_COVER_URL")
    print(f"  !! WARNING: {n} cover image(s) still point at the WIX_COVER_URL "
          f"placeholder.\n     Upload covers/*.jpg to Wix Media and replace each "
          f"src before deploying.\n     Building anyway: a missing image is a "
          f"VISIBLE fault, not a silent one.")

font_links = re.findall(r'<link href="([^"]+)" rel="stylesheet">',
                        "\n".join(lines[:opens[0] + 30]))
fonts = "\n".join(
    "    var f%d=document.createElement('link'); f%d.rel='stylesheet'; f%d.href=%r; "
    "document.head.appendChild(f%d);" % (i, i, i, u, i)
    for i, u in enumerate(font_links))

ld_block = ""
if LD:
    ld_block = """
  /* STRUCTURED DATA GOES IN THE DOCUMENT, NOT THE SHADOW ROOT.
     Nine Review objects. A crawler reads ld+json from the document only; the
     same script inside a shadow tree is invisible, which would have quietly
     undone the main point of rebuilding this page as text. */
  function addSchema(){
    if (document.getElementById('px-ld')) return;
    var s=document.createElement('script'); s.type='application/ld+json';
    s.id='px-ld'; s.textContent=`%s`; document.head.appendChild(s);
  }
""" % LD

OUT.write_text("""/* PARALLAXX TRANSFORMATIONS - Testimonials Wix Custom Element. Tag: parallaxx-testimonials.
   GENERATED by build-testimonials-bundle.py from "Parallaxx Testimonials v4.dc.html".
   DO NOT EDIT THIS FILE - edit the .dc.html and rerun the build.
   In the Wix editor: turn the site Header + Footer OFF for this page. It
   carries PtNav v3 and PtFooter v3 baked in. */
(function(){
  if (customElements.get('parallaxx-testimonials')) return;

  var CSS = `%s`;

  var HTML = `%s`;

  function addFonts(){
    if (document.getElementById('px-fonts-testimonials')) return;
    var p1=document.createElement('link'); p1.rel='preconnect'; p1.href='https://fonts.googleapis.com'; document.head.appendChild(p1);
    var p2=document.createElement('link'); p2.rel='preconnect'; p2.href='https://fonts.gstatic.com'; p2.crossOrigin=''; document.head.appendChild(p2);
%s
    /* @font-face has to live in the DOCUMENT, not the shadow root. Chrome
       ignores font-face rules declared inside a shadow tree. */
    var ff=document.createElement('style'); ff.id='px-fonts-testimonials'; ff.textContent=`%s`; document.head.appendChild(ff);
  }
%s
%s

  /* ══════════════ ANCESTOR COLLAPSE ══════════════
     Wix wraps a custom element in containers with fixed heights, so the page
     renders inside a short box with its own scrollbar. This walks up and
     releases them. One shot per element via a WeakSet, because re-running it
     on every resize is what once grew a document to Chrome's 2^24 clamp. */
  var PX_SANE_MAX = 200000;
  var pxCollapsed = new WeakSet();

  function collapseAncestors(host){
    try{
      if (document.documentElement.scrollHeight > PX_SANE_MAX) return;
      var h = host.getBoundingClientRect().height;
      if (h < 50) return;
      var n = host.parentElement, guard = 0;
      while(n && n !== document.body && guard++ < 14){
        if(!pxCollapsed.has(n) && n.getBoundingClientRect().height > h + 600){
          pxCollapsed.add(n);
          n.style.height = 'auto';
          n.style.minHeight = '0px';
        }
        n = n.parentElement;
      }
    }catch(e){}
  }

  function boot(root){
    var pxRoot = root.getElementById('px-root');
    if(!pxRoot) return;
    initTestimonials(pxRoot);
    try{ initPtNav(root); }catch(e){ if(window.console) console.warn('[px] ptnav', e); }
    try{ initPtFooter(root); }catch(e){ if(window.console) console.warn('[px] ptfooter', e); }
  }

  class ParallaxxTestimonials extends HTMLElement {
    connectedCallback(){
      if (this._mounted) return; this._mounted = true;
      addFonts();%s
      var shadow = this.attachShadow({mode:'open'});
      shadow.innerHTML = '<style>'+CSS+'</style>'+HTML;
      var host = this;
      /* The host's own fixed height, not just its ancestors'. Left set, the
         surplus renders as empty page background under the content. */
      try{ host.style.height='auto'; host.style.minHeight='0px'; }catch(e){}
      try{ boot(shadow); }catch(e){ console.error('[px] boot failed:', e); }
      requestAnimationFrame(function(){ collapseAncestors(host); });
      [400,1200,2500].forEach(function(t){ setTimeout(function(){ collapseAncestors(host); }, t); });
      var pxRT;
      window.addEventListener('resize', function(){
        clearTimeout(pxRT);
        pxRT = setTimeout(function(){ collapseAncestors(host); }, 250);
      }, {passive:true});
    }
  }
  customElements.define('parallaxx-testimonials', ParallaxxTestimonials);
})();
""" % (CSS, HTML, fonts, FONTFACE, ld_block, BODY,
       "\n      addSchema();" if LD else ""), encoding="utf-8")

print(f"built {OUT.name}  css={len(CSS)}  html={len(HTML)}  body={len(BODY)}  "
      f"schema={len(LD)}  fonts={len(font_links)}")

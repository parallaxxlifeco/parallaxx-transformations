#!/usr/bin/env python3
"""
Build parallaxx-contact.js AND contact-preview.html from
"Parallaxx Contact v4.dc.html".

    python3 build-contact-bundle.py

THE .dc.html IS THE SOURCE OF RECORD. Both outputs are generated and are
overwritten on every run. Never hand-edit either of them.

  Source  : Parallaxx Contact v4.dc.html
  Bundle  : parallaxx-contact.js          (custom element)
  Preview : contact-preview.html          (open it in a browser)
  Tag     : parallaxx-contact
  Root    : pc-root

WHY A BUILD STEP AT ALL
Same reason as every other page here. The .dc.html runs in the Design Code
runtime, where the component sits in the light DOM. The deployed bundle runs
inside a shadow root, and two things differ, both of which fail SILENTLY
rather than throwing:

  1. document.getElementById() returns null inside a shadow root, so the nav
     would render perfectly and do nothing at all.
  2. @font-face declared inside a shadow tree is ignored by Chrome, so the
     font rules have to be injected into document.head separately.

WHY THIS ONE LOADS NO LIBRARIES
The other pages pull GSAP, ScrollTrigger and Lenis off two CDNs before they
animate. This page exists to hand over an email address, and an address that
is waiting on a CDN round trip is an address that can fail to arrive. Every
reveal here is a CSS keyframe on a delay, so boot() runs immediately and
nothing on the page depends on a library that may never land. The guard
below refuses to build if GSAP ever appears in the source, the same way
build-home-bundle.py does for the front door.

There is also no form, and that is not an omission. The page this replaces
carried one that called preventDefault(), discarded all four fields and
redirected to a booking page. It never sent anything. The guard below fails
the build on a <form> element, so a form cannot come back without somebody
deciding, out loud, where the submissions go.
"""
import re, sys, pathlib

HERE = pathlib.Path(__file__).parent
SRC  = HERE / "Parallaxx Contact v4.dc.html"
JS   = HERE / "parallaxx-contact.js"
PREV = HERE / "contact-preview.html"
TAG  = "parallaxx-contact"
ROOT = "pc-root"
MAIL = "daniel@parallaxxtransformations.com"

src = SRC.read_text(encoding="utf-8")

# ---- guards on the SOURCE -------------------------------------------------
if "`" in src:
    bad = [i + 1 for i, l in enumerate(src.split("\n")) if "`" in l]
    sys.exit(f"FAIL: backtick in source (lines {bad}). CSS and HTML are embedded "
             f"in template literals; a backtick terminates them and silently "
             f"destroys the stylesheet. Use single quotes.")
if "${" in src:
    sys.exit("FAIL: '${' in source would interpolate inside the template literal.")
# Usage, not mentions. The comment at the top of the stylesheet says the
# words on purpose, so the guard looks for a script tag or a real API call
# rather than the bare noun -- the same distinction the localStorage guard in
# build-priority-audit-bundle.py had to make.
if re.search(r"<script[^>]+src=[^>]*(gsap|lenis)", src, re.I) or \
   re.search(r"\b(gsap|Lenis|ScrollTrigger)\s*[.(]", src):
    sys.exit("FAIL: an animation library is loaded or called in the source. This "
             "page hands over an email address and must not wait on a CDN to do "
             "it. Use a CSS keyframe.")
if re.search(r"<form\b", src, re.I):
    sys.exit("FAIL: a <form> is back in the source. The page this replaced had "
             "one that threw every field away. If a real form is wanted, decide "
             "where the submissions land first, then delete this guard on "
             "purpose rather than by accident.")
if MAIL not in src:
    sys.exit(f"FAIL: {MAIL} is not in the source. The address IS the page; "
             f"shipping it without one is shipping nothing.")
if 'href="mailto:%s"' % MAIL not in src:
    sys.exit("FAIL: the address appears as text but not as a mailto link. On a "
             "phone that is an address nobody can tap.")
for api in ("localStorage", "sessionStorage"):
    if re.search(r"\b%s\s*[.\[]" % api, src):
        sys.exit(f"FAIL: {api} used in source. Browser storage is unavailable in "
                 f"the target environments.")

lines = src.split("\n")

def style_block(open_line_idx):
    close = next(k for k in range(open_line_idx + 1, len(lines))
                 if lines[k].strip() == "</style>")
    return "\n".join(lines[open_line_idx + 1:close])

opens = [i for i, l in enumerate(lines) if l.strip() == "<style>"]
if len(opens) != 2:
    sys.exit("FAIL: expected exactly two <style> blocks in the helmet, a "
             "@font-face one and the main sheet. Found %d. A third block "
             "outside the helmet is dropped by this converter and would ship "
             "unstyled." % len(opens))
FONTFACE, CSS = style_block(opens[0]), style_block(opens[1])

h0 = next(i for i, l in enumerate(lines) if l.startswith('<div id="%s"' % ROOT))
h1 = next(i for i, l in enumerate(lines) if l.rstrip() == "</x-dc>")
HTML = "\n".join(lines[h0:h1]).rstrip()
HTML = HTML[:HTML.index('<script type="text/x-dc"')].rstrip()

js = src[src.index('<script type="text/x-dc"'):]
js = js[js.index(">") + 1:js.index("</script>")]
body = js[js.index("componentDidMount(){") + len("componentDidMount(){"):]
body = body[:body.rindex("renderVals()")].rstrip()
body = body[:body.rindex("}")].rstrip()          # drop componentDidMount's closer

BOOTBODY = body.replace(
    "    const root = document.getElementById('%s');\n    if(!root) return;\n" % ROOT, "")
BOOTBODY = BOOTBODY.replace("document.getElementById(", "root.getElementById(")

# ---- guards on the OUTPUT -------------------------------------------------
if "const root =" in BOOTBODY:
    sys.exit("FAIL: local root binding survived; it would shadow boot()'s parameter.")
if "document.getElementById" in BOOTBODY:
    sys.exit("FAIL: a document.getElementById survived the rewrite.")
if "document.querySelector" in BOOTBODY:
    sys.exit("FAIL: document.querySelector in the boot body. Inside a shadow "
             "root that searches the wrong tree. Use root.querySelector.")
if "root.classList" in BOOTBODY:
    sys.exit("FAIL: classList called on root. In the bundle that is a shadow "
             "root, which has no classList.")
if "pt-nav" not in HTML or "pt-foot" not in HTML:
    sys.exit("FAIL: the nav or the footer is missing from the markup. Site "
             "Header and Footer are OFF for this page, so the page would ship "
             "with no way out of itself.")

font_links = re.findall(r'<link href="([^"]+)" rel="stylesheet">',
                        "\n".join(lines[:opens[0] + 30]))
fonts = "\n".join(
    "    var f%d=document.createElement('link'); f%d.rel='stylesheet'; f%d.href=%r; "
    "document.head.appendChild(f%d);" % (i, i, i, u, i)
    for i, u in enumerate(font_links))

# ═══════════════════════════════════════════════════════════════════════════
# 1 · THE CUSTOM ELEMENT
# ═══════════════════════════════════════════════════════════════════════════
JS.write_text("""/* PARALLAXX TRANSFORMATIONS - Contact. Custom Element. Tag: %s.
   GENERATED by build-contact-bundle.py from "Parallaxx Contact v4.dc.html".
   DO NOT EDIT THIS FILE - edit the .dc.html and rerun the build.

   PtNav v3 and PtFooter v3 are baked in, same as every other page in the
   README table, so the site Header and Footer must be OFF for this page or
   it renders two navs and two footers.

   The nav works out where it is from the URL. Its table already maps
   /contact-daniel-lawson to 'contact', so the coral pill in the top right
   lights up here with nothing to configure. */
(function(){
  if (customElements.get('%s')) return;

  var CSS = `%s`;

  var HTML = `%s`;

  function addFonts(){
    if (document.getElementById('pc-fonts')) return;
    var p1=document.createElement('link'); p1.rel='preconnect'; p1.href='https://fonts.googleapis.com'; document.head.appendChild(p1);
    var p2=document.createElement('link'); p2.rel='preconnect'; p2.href='https://fonts.gstatic.com'; p2.crossOrigin=''; document.head.appendChild(p2);
%s
    /* @font-face has to live in the DOCUMENT, not the shadow root. Chrome
       ignores font-face rules declared inside a shadow tree. */
    var ff=document.createElement('style'); ff.id='pc-fonts'; ff.textContent=`%s`; document.head.appendChild(ff);
  }

  function boot(root){
    if(!root || !root.getElementById('%s')) return;
%s
  }

  /* Wix wraps a custom element in a fixed-height container sized from the
     editor. This page is shorter than most and the wrapper is usually told
     to be taller, which leaves a navy gap under the footer. */
  function collapseAncestors(host){
    try{ var h=host.getBoundingClientRect().height; if(h<50) return;
      var n=host.parentElement,guard=0;
      while(n && n!==document.body && guard++<14){ if(n.getBoundingClientRect().height>h+600){ n.style.height='auto'; n.style.minHeight='0px'; } n=n.parentElement; }
    }catch(e){}
  }

  class ParallaxxContact extends HTMLElement {
    connectedCallback(){
      if (this._mounted) return; this._mounted = true;
      addFonts();
      var shadow = this.attachShadow({mode:'open'});
      shadow.innerHTML = '<style>'+CSS+'</style>'+HTML;
      var host = this;
      /* No library to wait for. boot() runs on this tick, which is the
         whole reason this page has no GSAP. */
      try{ boot(shadow); }catch(e){ console.error('[pc] boot failed:', e); }
      requestAnimationFrame(function(){ collapseAncestors(host); });
      [400,1200,2500].forEach(function(t){ setTimeout(function(){ collapseAncestors(host); }, t); });
      window.addEventListener('resize', function(){ collapseAncestors(host); }, {passive:true});
    }
  }
  customElements.define('%s', ParallaxxContact);
})();
""" % (TAG, TAG, CSS, HTML, fonts, FONTFACE, ROOT, BOOTBODY, TAG), encoding="utf-8")

# ═══════════════════════════════════════════════════════════════════════════
# 2 · THE STANDALONE PREVIEW
# Same CSS, same markup, same script. The page carries its own nav and
# footer, so unlike the Priority Audit's preview there is no shell to add.
# ═══════════════════════════════════════════════════════════════════════════
PREV.write_text("""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>Contact &mdash; Parallaxx Transformations</title>
<meta name="description" content="Write to Daniel Lawson. It comes to his own inbox.">
<meta name="robots" content="noindex">
<!-- GENERATED by build-contact-bundle.py from "Parallaxx Contact v4.dc.html".
     DO NOT EDIT - edit the .dc.html and rerun the build. -->
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
%s
<style>%s</style>
<style>html,body{margin:0;padding:0;background:#04122A}</style>
<style>%s</style>
</head>
<body>

%s

<script>
(function(){
%s
})();
</script>
</body>
</html>
""" % ("\n".join('<link href="%s" rel="stylesheet">' % u for u in font_links),
       FONTFACE, CSS, HTML, body), encoding="utf-8")

print("built %s  css=%d  html=%d  boot=%d  fonts=%d" % (JS.name, len(CSS), len(HTML), len(BOOTBODY), len(font_links)))
print("built %s" % PREV.name)

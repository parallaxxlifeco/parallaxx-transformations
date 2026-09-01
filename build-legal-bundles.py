#!/usr/bin/env python3
"""
Build parallaxx-privacy.js and parallaxx-terms.js, plus a preview for each,
from ONE source: "Parallaxx Legal.dc.html".

    python3 build-legal-bundles.py

THE .dc.html IS THE SOURCE OF RECORD. All four outputs are generated and are
overwritten on every run. Never hand-edit any of them.

  Source   : Parallaxx Legal.dc.html
  Bundles  : parallaxx-privacy.js       tag parallaxx-privacy
             parallaxx-terms.js         tag parallaxx-terms
  Previews : privacy-preview.html
             terms-preview.html
  Root     : lg-root  (both -- each bundle gets its own shadow root, so the
             id cannot collide even if the two pages ever shared a document)

WHY ONE SOURCE FOR TWO PAGES
Everything about these two documents is identical except their words: same
chrome, same header block, same 68ch measure, same closing block. Authored as
two .dc.html files they would share a stylesheet by copy, and the first fix to
one would silently stop applying to the other. That is not hypothetical -- it
is exactly what happened to parallaxx-footer.js, whose committed bundle is
still ahead of PtFooter v3.dc.html and gets reverted by its own build. So the
stylesheet and the chrome live once, and this script slices the file on the
two <section> ids.

Each bundle therefore ships the FULL stylesheet, including the rules only the
other document uses. That is a few hundred wasted bytes per page and it buys
the guarantee that the two pages cannot drift. Take the trade.

WHY A BUILD STEP AT ALL
The .dc.html runs in the Design Code runtime, in the light DOM. The deployed
bundle runs inside a shadow root, where document.getElementById() returns null
and @font-face is ignored -- both silently. Same as every other page here.

THE WORDS ARE NOT OURS TO EDIT. Both documents are the copy harvested off the
live Wix pages, verbatim. The guard below fails the build if either document
loses its "Last updated" line or its governing-entity line, because a legal
page that has quietly lost its date is worse than one that is out of date.
"""
import re, sys, pathlib

HERE = pathlib.Path(__file__).parent
SRC  = HERE / "Parallaxx Legal.dc.html"
ROOT = "lg-root"

PAGES = [
    dict(key="privacy", section="lg-privacy", tag="parallaxx-privacy",
         js="parallaxx-privacy.js", prev="privacy-preview.html",
         title="Privacy Policy",
         desc="How Parallaxx Transformations collects, uses and safeguards your "
              "information. Australian Privacy Principles and GDPR."),
    dict(key="terms", section="lg-terms", tag="parallaxx-terms",
         js="parallaxx-terms.js", prev="terms-preview.html",
         title="Terms of Use",
         desc="The terms that govern use of the Parallaxx Transformations website "
              "and services."),
]

src = SRC.read_text(encoding="utf-8")

# ---- guards on the SOURCE -------------------------------------------------
if "`" in src:
    bad = [i + 1 for i, l in enumerate(src.split("\n")) if "`" in l]
    sys.exit(f"FAIL: backtick in source (lines {bad}). CSS and HTML are embedded "
             f"in template literals; a backtick terminates them and silently "
             f"destroys the stylesheet. Use single quotes.")
if "${" in src:
    sys.exit("FAIL: '${' in source would interpolate inside the template literal.")
if src.count("Last updated 1 September 2026") != 2:
    sys.exit("FAIL: expected a 'Last updated 1 September 2026' line on both\n"
             "documents. A legal page that has quietly lost its date is worse than\n"
             "one that is out of date. If the date genuinely changed, change it in\n"
             "the source AND in this guard -- they are pinned together on purpose,\n"
             "so a date can never drift without somebody deciding it should.")
if src.count("Parallax Life Co Pty LTD") < 3:
    sys.exit("FAIL: the governing entity is missing from one of the documents. "
             "Both have to name who the terms are with.")
for api in ("localStorage", "sessionStorage"):
    if re.search(r"\b%s\s*[.\[]" % api, src):
        sys.exit(f"FAIL: {api} used in source.")

lines = src.split("\n")

def style_block(open_line_idx):
    close = next(k for k in range(open_line_idx + 1, len(lines))
                 if lines[k].strip() == "</style>")
    return "\n".join(lines[open_line_idx + 1:close])

opens = [i for i, l in enumerate(lines) if l.strip() == "<style>"]
if len(opens) != 2:
    sys.exit("FAIL: expected exactly two <style> blocks in the helmet. Found %d. "
             "A third block outside the helmet is dropped by this converter and "
             "would ship unstyled." % len(opens))
FONTFACE, CSS = style_block(opens[0]), style_block(opens[1])

# ---- the pieces of markup -------------------------------------------------
def between(open_tag_start, close_tag):
    a = src.index(open_tag_start)
    b = src.index(close_tag, a) + len(close_tag)
    return src[a:b]

NAV  = between('<header id="pt-nav">', "</header>")
FOOT = between('<footer id="pt-foot">', "</footer>")

def section(sid):
    a = src.index('<section id="%s">' % sid)
    b = src.index("</section>", a) + len("</section>")
    return src[a:b]

# ---- the boot body --------------------------------------------------------
js = src[src.index('<script type="text/x-dc"'):]
js = js[js.index(">") + 1:js.index("</script>")]
body = js[js.index("componentDidMount(){") + len("componentDidMount(){"):]
body = body[:body.rindex("renderVals()")].rstrip()
body = body[:body.rindex("}")].rstrip()

BOOTBODY = body.replace(
    "    const root = document.getElementById('%s');\n    if(!root) return;\n" % ROOT, "")
BOOTBODY = BOOTBODY.replace("document.getElementById(", "root.getElementById(")

if "const root =" in BOOTBODY:
    sys.exit("FAIL: local root binding survived; it would shadow boot()'s parameter.")
if "document.getElementById" in BOOTBODY:
    sys.exit("FAIL: a document.getElementById survived the rewrite.")
if "document.querySelector" in BOOTBODY:
    sys.exit("FAIL: document.querySelector in the boot body. Inside a shadow root "
             "that searches the wrong tree. Use root.querySelector.")
if "root.classList" in BOOTBODY:
    sys.exit("FAIL: classList called on root. In the bundle that is a shadow root, "
             "which has no classList.")

font_links = re.findall(r'<link href="([^"]+)" rel="stylesheet">',
                        "\n".join(lines[:opens[0] + 30]))
fonts = "\n".join(
    "    var f%d=document.createElement('link'); f%d.rel='stylesheet'; f%d.href=%r; "
    "document.head.appendChild(f%d);" % (i, i, i, u, i)
    for i, u in enumerate(font_links))

BUNDLE = """/* PARALLAXX TRANSFORMATIONS - %(title)s. Custom Element. Tag: %(tag)s.
   GENERATED by build-legal-bundles.py from "Parallaxx Legal.dc.html".
   DO NOT EDIT THIS FILE - edit the .dc.html and rerun the build, which
   rebuilds BOTH legal pages. They share one source on purpose.

   PtNav v3 and PtFooter v3 are baked in, so site Header and Footer must be
   OFF, same as every other page in the README table.

   No libraries. These are documents; nothing on them animates beyond a CSS
   keyframe, and a legal page that is waiting on a CDN is a legal page that
   can fail to render at the moment somebody is auditing the site. */
(function(){
  if (customElements.get('%(tag)s')) return;

  var CSS = `%(css)s`;

  var HTML = `%(html)s`;

  function addFonts(){
    if (document.getElementById('lg-fonts')) return;
    var p1=document.createElement('link'); p1.rel='preconnect'; p1.href='https://fonts.googleapis.com'; document.head.appendChild(p1);
    var p2=document.createElement('link'); p2.rel='preconnect'; p2.href='https://fonts.gstatic.com'; p2.crossOrigin=''; document.head.appendChild(p2);
%(fonts)s
    /* @font-face has to live in the DOCUMENT, not the shadow root. Chrome
       ignores font-face rules declared inside a shadow tree. */
    var ff=document.createElement('style'); ff.id='lg-fonts'; ff.textContent=`%(fontface)s`; document.head.appendChild(ff);
  }

  function boot(root){
    if(!root || !root.getElementById('%(root)s')) return;
%(boot)s
  }

  function collapseAncestors(host){
    try{ var h=host.getBoundingClientRect().height; if(h<50) return;
      var n=host.parentElement,guard=0;
      while(n && n!==document.body && guard++<14){ if(n.getBoundingClientRect().height>h+600){ n.style.height='auto'; n.style.minHeight='0px'; } n=n.parentElement; }
    }catch(e){}
  }

  class %(cls)s extends HTMLElement {
    connectedCallback(){
      if (this._mounted) return; this._mounted = true;
      addFonts();
      var shadow = this.attachShadow({mode:'open'});
      shadow.innerHTML = '<style>'+CSS+'</style>'+HTML;
      var host = this;
      try{ boot(shadow); }catch(e){ console.error('[lg] boot failed:', e); }
      requestAnimationFrame(function(){ collapseAncestors(host); });
      [400,1200,2500].forEach(function(t){ setTimeout(function(){ collapseAncestors(host); }, t); });
      window.addEventListener('resize', function(){ collapseAncestors(host); }, {passive:true});
    }
  }
  customElements.define('%(tag)s', %(cls)s);
})();
"""

PREVIEW = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>%(title)s &mdash; Parallaxx Transformations</title>
<meta name="description" content="%(desc)s">
<meta name="robots" content="noindex">
<!-- GENERATED by build-legal-bundles.py from "Parallaxx Legal.dc.html".
     DO NOT EDIT - edit the .dc.html and rerun the build. -->
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
%(links)s
<style>%(fontface)s</style>
<style>html,body{margin:0;padding:0;background:#04122A}</style>
<style>%(css)s</style>
</head>
<body>

%(html)s

<script>
(function(){
%(body)s
})();
</script>
</body>
</html>
"""

for pg in PAGES:
    sec = section(pg["section"])
    html = '<div id="%s">\n\n%s\n\n%s\n\n%s\n\n</div>' % (ROOT, NAV, sec, FOOT)
    if "pt-nav" not in html or "pt-foot" not in html:
        sys.exit("FAIL: %s lost its chrome." % pg["key"])
    if "Last updated" not in html:
        sys.exit("FAIL: %s lost its date." % pg["key"])
    cls = "Parallaxx" + pg["key"].capitalize()
    (HERE / pg["js"]).write_text(BUNDLE % dict(
        title=pg["title"], tag=pg["tag"], css=CSS, html=html, fonts=fonts,
        fontface=FONTFACE, root=ROOT, boot=BOOTBODY, cls=cls), encoding="utf-8")
    (HERE / pg["prev"]).write_text(PREVIEW % dict(
        title=pg["title"], desc=pg["desc"], fontface=FONTFACE, css=CSS, html=html,
        body=body, links="\n".join('<link href="%s" rel="stylesheet">' % u for u in font_links)
    ), encoding="utf-8")
    print("built %-24s tag=%-20s html=%d" % (pg["js"], pg["tag"], len(html)))
    print("built %s" % pg["prev"])

print("css=%d boot=%d fonts=%d (one stylesheet, both pages)" % (len(CSS), len(BOOTBODY), len(font_links)))

#!/usr/bin/env python3
"""
Build parallaxx-identity.js and identity-preview.html from
"Parallaxx Identity 2.0.dc.html".

    python3 build-identity-bundle.py

THE .dc.html IS THE SOURCE OF RECORD. Both outputs are generated and are
overwritten on every run. Never hand-edit either of them.

  Source  : Parallaxx Identity 2.0.dc.html
  Bundle  : parallaxx-identity.js       (custom element)
  Preview : identity-preview.html
  Tag     : parallaxx-identity
  Root    : id2-root

WHY THIS PAGE HAS NO NAV OR FOOTER
Every other route in this repo bakes PtNav v3 and PtFooter v3 in. This one
does not, and that is a decision rather than an oversight: it is a VSL funnel
page whose only job is to get somebody to press play and then enrol, and a
full site nav on a page like that is ten ways to leave before the video
starts. It carries a slim header and a one-line footer instead.

Because of that, the usual "the nav and footer must be present" guard would be
wrong here. What replaces it is the pair of guards below on the two things
this page cannot ship without: the video and the enrol link.

WHY A BUILD STEP AT ALL
Same as every other page. The .dc.html runs in the Design Code runtime in the
light DOM; the deployed bundle runs inside a shadow root, where
document.getElementById() returns null and @font-face is ignored, both
silently. The overlay that starts the video is the entire interaction on this
page, so a silent failure here is the whole page failing.
"""
import re, sys, pathlib

HERE = pathlib.Path(__file__).parent
SRC  = HERE / "Parallaxx Identity 2.0.dc.html"
JS   = HERE / "parallaxx-identity.js"
PREV = HERE / "identity-preview.html"
TAG  = "parallaxx-identity"
ROOT = "id2-root"

src = SRC.read_text(encoding="utf-8")

# ---- guards on the SOURCE -------------------------------------------------
if "`" in src:
    bad = [i + 1 for i, l in enumerate(src.split("\n")) if "`" in l]
    sys.exit(f"FAIL: backtick in source (lines {bad}). CSS and HTML are embedded "
             f"in template literals; a backtick terminates them and silently "
             f"destroys the stylesheet. Use single quotes.")
if "${" in src:
    sys.exit("FAIL: '${' in source would interpolate inside the template literal.")

# The page arrived carrying UTF-8 read as Latin-1 in three places -- the title,
# the bonus heading and the footer copyright. Each rendered as literal garbage.
# Cheap to catch, invisible in a diff, embarrassing in production.
MOJIBAKE = ("‘Äî", "‚Äî", "Â©", "â€”")
for m in MOJIBAKE:
    if m in src:
        sys.exit("FAIL: mojibake in source (%r). Something was saved as UTF-8 and "
                 "re-read as Latin-1. Fix the character, do not ship it." % m)

if "id2-video" not in src or "<source" not in src:
    sys.exit("FAIL: the video is gone. This is a VSL page -- without the video "
             "it is a headline and a button.")
if "members.parallaxxtransformations.com" in src and "UNCONFIRMED" not in src:
    sys.exit("FAIL: the enrol link still points at members.parallaxxtransformations.com "
             "and the comment explaining that it is unconfirmed has been removed. "
             "Either the URL is fixed, or the warning stays. That CNAME was dropped "
             "in the migration and no browser will connect to it.")
if not re.search(r'<a class="id2-btn" href="https?://', src):
    sys.exit("FAIL: no enrol link. The page has one job.")
for api in ("localStorage", "sessionStorage"):
    if re.search(r"\b%s\s*[.\[]" % api, src):
        sys.exit(f"FAIL: {api} used in source.")

lines = src.split("\n")

def style_block(i):
    close = next(k for k in range(i + 1, len(lines)) if lines[k].strip() == "</style>")
    return "\n".join(lines[i + 1:close])

opens = [i for i, l in enumerate(lines) if l.strip() == "<style>"]
if len(opens) != 2:
    sys.exit("FAIL: expected exactly two <style> blocks in the helmet. Found %d."
             % len(opens))
FONTFACE, CSS = style_block(opens[0]), style_block(opens[1])

h0 = next(i for i, l in enumerate(lines) if l.startswith('<div id="%s"' % ROOT))
h1 = next(i for i, l in enumerate(lines) if l.rstrip() == "</x-dc>")
HTML = "\n".join(lines[h0:h1]).rstrip()
HTML = HTML[:HTML.index('<script type="text/x-dc"')].rstrip()

js = src[src.index('<script type="text/x-dc"'):]
js = js[js.index(">") + 1:js.index("</script>")]
body = js[js.index("componentDidMount(){") + len("componentDidMount(){"):]
body = body[:body.rindex("renderVals()")].rstrip()
body = body[:body.rindex("}")].rstrip()

BOOTBODY = body.replace(
    "    const root = document.getElementById('%s');\n    if(!root) return;\n" % ROOT, "")
BOOTBODY = BOOTBODY.replace("document.getElementById('id2-overlay')", "root.getElementById('id2-overlay')")
BOOTBODY = BOOTBODY.replace("document.getElementById('id2-video')", "root.getElementById('id2-video')")

# ---- guards on the OUTPUT -------------------------------------------------
if "const root =" in BOOTBODY:
    sys.exit("FAIL: local root binding survived; it would shadow boot()'s parameter.")
if "document.getElementById" in BOOTBODY:
    sys.exit("FAIL: a document.getElementById survived the rewrite.")
if "document.querySelector" in BOOTBODY:
    sys.exit("FAIL: document.querySelector in the boot body. Inside a shadow root "
             "that searches the wrong tree. Use root.querySelector.")
if "root.classList" in BOOTBODY:
    sys.exit("FAIL: classList called on root. In the bundle that is a shadow root.")

font_links = re.findall(r'<link href="([^"]+)" rel="stylesheet">',
                        "\n".join(lines[:opens[0] + 30]))
fonts = "\n".join(
    "    var f%d=document.createElement('link'); f%d.rel='stylesheet'; f%d.href=%r; "
    "document.head.appendChild(f%d);" % (i, i, i, u, i)
    for i, u in enumerate(font_links))

JS.write_text("""/* PARALLAXX TRANSFORMATIONS - Identity 2.0 Challenge. Custom Element.
   Tag: %s.
   GENERATED by build-identity-bundle.py from "Parallaxx Identity 2.0.dc.html".
   DO NOT EDIT THIS FILE - edit the .dc.html and rerun the build.

   NO PtNav AND NO PtFooter ON PURPOSE. This is a funnel page; a full site nav
   on a VSL is ten ways to leave before the video starts. It carries its own
   slim header and a one-line footer, so unlike every other row in the README
   table there is no Wix chrome to switch off -- there is no Wix.

   TWO THINGS ARE STILL OUTSTANDING AND BOTH ARE IN THE SOURCE COMMENTS:
   the enrol URL points at a subdomain the migration dropped, and the video
   and poster are still served from Wix rather than /assets/. */
(function(){
  if (customElements.get('%s')) return;

  var CSS = `%s`;

  var HTML = `%s`;

  function addFonts(){
    if (document.getElementById('id2-fonts')) return;
    var p1=document.createElement('link'); p1.rel='preconnect'; p1.href='https://fonts.googleapis.com'; document.head.appendChild(p1);
    var p2=document.createElement('link'); p2.rel='preconnect'; p2.href='https://fonts.gstatic.com'; p2.crossOrigin=''; document.head.appendChild(p2);
%s
    var ff=document.createElement('style'); ff.id='id2-fonts'; ff.textContent=`%s`; document.head.appendChild(ff);
  }

  function boot(root){
    if(!root || !root.getElementById('%s')) return;
%s
  }

  function collapseAncestors(host){
    try{ var h=host.getBoundingClientRect().height; if(h<50) return;
      var n=host.parentElement,guard=0;
      while(n && n!==document.body && guard++<14){ if(n.getBoundingClientRect().height>h+600){ n.style.height='auto'; n.style.minHeight='0px'; } n=n.parentElement; }
    }catch(e){}
  }

  class ParallaxxIdentity extends HTMLElement {
    connectedCallback(){
      if (this._mounted) return; this._mounted = true;
      addFonts();
      var shadow = this.attachShadow({mode:'open'});
      shadow.innerHTML = '<style>'+CSS+'</style>'+HTML;
      var host = this;
      try{ boot(shadow); }catch(e){ console.error('[id2] boot failed:', e); }
      requestAnimationFrame(function(){ collapseAncestors(host); });
      [400,1200,2500].forEach(function(t){ setTimeout(function(){ collapseAncestors(host); }, t); });
      window.addEventListener('resize', function(){ collapseAncestors(host); }, {passive:true});
    }
  }
  customElements.define('%s', ParallaxxIdentity);
})();
""" % (TAG, TAG, CSS, HTML, fonts, FONTFACE, ROOT, BOOTBODY, TAG), encoding="utf-8")

PREV.write_text("""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>Identity 2.0 Challenge &mdash; Parallaxx Transformations</title>
<meta name="robots" content="noindex">
<!-- GENERATED by build-identity-bundle.py. DO NOT EDIT. -->
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

print("built %s  css=%d  html=%d  boot=%d" % (JS.name, len(CSS), len(HTML), len(BOOTBODY)))
print("built %s" % PREV.name)
print("NOTE: the enrol URL and the Wix-hosted video are both still unresolved.")

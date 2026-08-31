#!/usr/bin/env python3
"""
Build parallaxx-as-seen-in.js and as-seen-in-preview.html from
"Parallaxx As Seen In.dc.html".

    python3 build-as-seen-in-bundle.py

THE .dc.html IS THE SOURCE OF RECORD. Both outputs are generated and are
overwritten on every run. Never hand-edit either of them.

  Source  : Parallaxx As Seen In.dc.html
  Bundle  : parallaxx-as-seen-in.js      (custom element)
  Preview : as-seen-in-preview.html
  Tag     : parallaxx-as-seen-in
  Root    : sn-root

WHAT THIS PAGE IS
Eight podcast appearances, each one a link on somebody else's platform. That
is the entire value of it: everything else on this site is Daniel describing
Daniel, and this is eight other people putting him in front of their audience
with a URL the reader can go and open.

WHICH IS WHY THE GUARDS BELOW ARE ABOUT LINKS.
The page's promise is "go and check", so a dead link costs more here than
anywhere else on the site. Every URL was opened and verified on 24 Aug 2026
and the result is recorded in a comment beside each row. The guards enforce
the shape of that arrangement rather than the checking itself, which a build
script cannot do:

  - every row has to be an external link that opens in a new tab, with
    rel="noopener" -- an internal or same-tab link in this list is a mistake
  - the count in the headline has to match the number of rows, because
    "Eight of them" above seven rows is the kind of thing nobody notices
    until a visitor counts
  - the verification date in the body has to appear, so the claim on the page
    stays attached to a date somebody can judge

RE-VERIFY BEFORE ANY DEPLOY THAT IS MONTHS LATER THAN THE LAST ONE. Podcast
hosts move, buzzsprout re-orders feeds, and one of these nine was already a
404 by the time this page was built.

WHY A BUILD STEP AT ALL
The .dc.html runs in the Design Code runtime, in the light DOM. The deployed
bundle runs inside a shadow root, where document.getElementById() returns null
and @font-face is ignored -- both silently. Same as every other page here.

No libraries. Nothing on this page animates beyond a CSS keyframe.
"""
import re, sys, pathlib

HERE = pathlib.Path(__file__).parent
SRC  = HERE / "Parallaxx As Seen In.dc.html"
JS   = HERE / "parallaxx-as-seen-in.js"
PREV = HERE / "as-seen-in-preview.html"
TAG  = "parallaxx-as-seen-in"
ROOT = "sn-root"
VERIFIED = "24 August 2026"

NUMBERS = {1:"One",2:"Two",3:"Three",4:"Four",5:"Five",6:"Six",7:"Seven",
           8:"Eight",9:"Nine",10:"Ten",11:"Eleven",12:"Twelve"}

src = SRC.read_text(encoding="utf-8")

# ---- guards on the SOURCE -------------------------------------------------
if "`" in src:
    bad = [i + 1 for i, l in enumerate(src.split("\n")) if "`" in l]
    sys.exit(f"FAIL: backtick in source (lines {bad}). CSS and HTML are embedded "
             f"in template literals; a backtick terminates them and silently "
             f"destroys the stylesheet. Use single quotes.")
if "${" in src:
    sys.exit("FAIL: '${' in source would interpolate inside the template literal.")
if re.search(r"<script[^>]+src=[^>]*(gsap|lenis)", src, re.I) or \
   re.search(r"\b(gsap|Lenis|ScrollTrigger)\s*[.(]", src):
    sys.exit("FAIL: an animation library is loaded or called in the source.")
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
    sys.exit("FAIL: expected exactly two <style> blocks in the helmet. Found %d."
             % len(opens))
FONTFACE, CSS = style_block(opens[0]), style_block(opens[1])

h0 = next(i for i, l in enumerate(lines) if l.startswith('<div id="%s"' % ROOT))
h1 = next(i for i, l in enumerate(lines) if l.rstrip() == "</x-dc>")
HTML = "\n".join(lines[h0:h1]).rstrip()
HTML = HTML[:HTML.index('<script type="text/x-dc"')].rstrip()

# ---- guards on the LIST --------------------------------------------------
rows = re.findall(r'<a class="sn-row"[^>]*>', HTML)
if not rows:
    sys.exit("FAIL: no .sn-row links found. The list IS the page.")

bad_target = [r for r in rows if 'target="_blank"' not in r]
if bad_target:
    sys.exit("FAIL: %d row(s) do not open in a new tab. Every row on this page "
             "leaves the site for somebody else's platform, and sending the "
             "reader away from the page that was proving something is the one "
             "navigation mistake this page cannot afford:\n  %s"
             % (len(bad_target), "\n  ".join(r[:110] for r in bad_target)))

bad_rel = [r for r in rows if "noopener" not in r]
if bad_rel:
    sys.exit("FAIL: %d row(s) missing rel=\"noopener\" on a target=\"_blank\" "
             "link." % len(bad_rel))

internal = [r for r in rows if "parallaxxtransformations.com" in r]
if internal:
    sys.exit("FAIL: %d row(s) point back at this site. Every row here has to be "
             "somebody else's URL -- that is the whole proof." % len(internal))

# The headline counts the rows out loud, so it has to agree with them.
n = len(rows)
word = NUMBERS.get(n, str(n))
m = re.search(r'<h2>([A-Za-z]+) of them', HTML)
if not m:
    sys.exit("FAIL: could not find the '<N> of them' headline in the list "
             "section. It is the one place the row count is written down in "
             "words, and it has to stay checkable.")
if m.group(1) != word:
    sys.exit("FAIL: the headline says '%s of them' and there are %d rows. "
             "Change the headline to '%s of them', or the page miscounts itself "
             "in its own largest type." % (m.group(1), n, word))

lede = re.search(r'([A-Za-z]+) conversations I have been a guest on', HTML)
if lede and lede.group(1) != word:
    sys.exit("FAIL: the lede says '%s conversations' and there are %d rows."
             % (lede.group(1), n))

if VERIFIED not in HTML:
    sys.exit("FAIL: the verification date '%s' is not on the page. The page "
             "invites the reader to check the links, so the date they were last "
             "checked has to be visible and has to be updated when they are "
             "re-checked." % VERIFIED)

# ---- the boot body --------------------------------------------------------
js = src[src.index('<script type="text/x-dc"'):]
js = js[js.index(">") + 1:js.index("</script>")]
body = js[js.index("componentDidMount(){") + len("componentDidMount(){"):]
body = body[:body.rindex("renderVals()")].rstrip()
body = body[:body.rindex("}")].rstrip()

BOOTBODY = body.replace(
    "    const root = document.getElementById('%s');\n    if(!root) return;\n" % ROOT, "")
BOOTBODY = BOOTBODY.replace("document.getElementById(", "root.getElementById(")

for bad, why in [("const root =", "local root binding survived; it would shadow boot()'s parameter"),
                 ("document.getElementById", "a document.getElementById survived the rewrite"),
                 ("document.querySelector", "document.querySelector searches the wrong tree in a shadow root"),
                 ("root.classList", "classList called on root, which is a shadow root in the bundle")]:
    if bad in BOOTBODY:
        sys.exit("FAIL: " + why + ".")
if "pt-nav" not in HTML or "pt-foot" not in HTML:
    sys.exit("FAIL: the nav or the footer is missing. Site Header and Footer are "
             "OFF for this page, so it would ship with no way out of itself.")

font_links = re.findall(r'<link href="([^"]+)" rel="stylesheet">',
                        "\n".join(lines[:opens[0] + 30]))
fonts = "\n".join(
    "    var f%d=document.createElement('link'); f%d.rel='stylesheet'; f%d.href=%r; "
    "document.head.appendChild(f%d);" % (i, i, i, u, i)
    for i, u in enumerate(font_links))

JS.write_text("""/* PARALLAXX TRANSFORMATIONS - As Seen In. Custom Element. Tag: %s.
   GENERATED by build-as-seen-in-bundle.py from "Parallaxx As Seen In.dc.html".
   DO NOT EDIT THIS FILE - edit the .dc.html and rerun the build.

   %d podcast appearances, every link on somebody else's platform, all of them
   opened and verified on %s. Re-verify before any deploy that is
   months later than that: one of the nine on the old Wix page was already a
   404 by the time this was built.

   PtNav v3 and PtFooter v3 are baked in, so site Header and Footer must be
   OFF, same as every other page in the README table. */
(function(){
  if (customElements.get('%s')) return;

  var CSS = `%s`;

  var HTML = `%s`;

  function addFonts(){
    if (document.getElementById('sn-fonts')) return;
    var p1=document.createElement('link'); p1.rel='preconnect'; p1.href='https://fonts.googleapis.com'; document.head.appendChild(p1);
    var p2=document.createElement('link'); p2.rel='preconnect'; p2.href='https://fonts.gstatic.com'; p2.crossOrigin=''; document.head.appendChild(p2);
%s
    /* @font-face has to live in the DOCUMENT, not the shadow root. Chrome
       ignores font-face rules declared inside a shadow tree. */
    var ff=document.createElement('style'); ff.id='sn-fonts'; ff.textContent=`%s`; document.head.appendChild(ff);
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

  class ParallaxxAsSeenIn extends HTMLElement {
    connectedCallback(){
      if (this._mounted) return; this._mounted = true;
      addFonts();
      var shadow = this.attachShadow({mode:'open'});
      shadow.innerHTML = '<style>'+CSS+'</style>'+HTML;
      var host = this;
      try{ boot(shadow); }catch(e){ console.error('[sn] boot failed:', e); }
      requestAnimationFrame(function(){ collapseAncestors(host); });
      [400,1200,2500].forEach(function(t){ setTimeout(function(){ collapseAncestors(host); }, t); });
      window.addEventListener('resize', function(){ collapseAncestors(host); }, {passive:true});
      /* Eight lazy thumbnails arriving change the height as they land. */
      if (window.ResizeObserver){
        try{ new ResizeObserver(function(){ collapseAncestors(host); }).observe(host); }catch(e){}
      }
    }
  }
  customElements.define('%s', ParallaxxAsSeenIn);
})();
""" % (TAG, n, VERIFIED, TAG, CSS, HTML, fonts, FONTFACE, ROOT, BOOTBODY, TAG),
   encoding="utf-8")

PREV.write_text("""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>As Seen In &mdash; Parallaxx Transformations</title>
<meta name="description" content="Podcast appearances by Daniel Lawson, all linked.">
<meta name="robots" content="noindex">
<!-- GENERATED by build-as-seen-in-bundle.py from "Parallaxx As Seen In.dc.html".
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

print("built %s  rows=%d  css=%d  html=%d  boot=%d" % (JS.name, n, len(CSS), len(HTML), len(BOOTBODY)))
print("built %s" % PREV.name)
print("links last verified %s -- re-check before a late deploy" % VERIFIED)

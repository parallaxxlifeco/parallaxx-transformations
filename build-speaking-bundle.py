#!/usr/bin/env python3
"""
Build parallaxx-speaking.js and speaking-preview.html from
"Parallaxx Speaking.dc.html".

    python3 build-speaking-bundle.py           draft: slots render as slots
    python3 build-speaking-bundle.py --ship    refuses while any slot is empty

THE .dc.html IS THE SOURCE OF RECORD. Both outputs are generated and are
overwritten on every run. Never hand-edit either of them.

  Source  : Parallaxx Speaking.dc.html
  Bundle  : parallaxx-speaking.js        (custom element)
  Preview : speaking-preview.html
  Tag     : parallaxx-speaking
  Root    : sp-root

ONE PAGE, TWO FOOTER LINKS. /facilitating redirects here rather than getting
a page of its own. It is the same offer described a second way, and splitting
thin material across two URLs makes both of them worse.

═══════════════════════════════════════════════════════════════════════════
THE IMAGE SLOTS, AND WHY THIS SCRIPT HAS A --ship MODE
───────────────────────────────────────────────────────────────────────────
The page this replaces pointed its hero at 'assets/stage-3.jpg' and a second
section at 'assets/connecting.jpg'. NEITHER FILE HAS EVER EXISTED IN THIS
REPO. The page shipped a broken image above the fold and stayed that way,
because nothing anywhere ever failed loudly about it -- a missing <img> is
the quietest possible defect. It renders as a gap, and a gap looks like
design.

So photographs are declared rather than assumed. Every one is an
IMAGE_SLOT_<NAME> token in the source, with its brief in SLOTS below.

  Draft build   each slot renders as a dashed box carrying its own brief and
                pixel size, at the true aspect ratio of the final photograph.
                The page lays out at full height with no photographs at all,
                so nothing shifts when they arrive.

  --ship build  FAILS if any slot is still a slot, and names the ones that
                are. Run it before a deploy.

TO FILL A SLOT
  1. Put the file in migration/wix-assets/img/ .
  2. In the .dc.html, replace IMAGE_SLOT_HERO with /assets/img/<filename>.
     Root-relative, because migration/build-site.py copies wix-assets/ to
     dist/assets/ and leaves already-relative paths alone.
  3. Rerun this build. Run it with --ship to confirm nothing is left.

There is usable material already in the archive if a slot needs a stand-in:
  HERO / ROOM   migration/wix-assets/img/img-107f479d04.jpg  (mid-talk, room
                in frame) and migration/wix-archive/c305d407e8e046b6b9f20129
                ebf7ee40.jpg (the audience, absorbed).
Everything else on the old page was old-brand programme covers, a stock
microphone or a trade-show booth, and none of it belongs here.
═══════════════════════════════════════════════════════════════════════════

WHY A BUILD STEP AT ALL
The .dc.html runs in the Design Code runtime, in the light DOM. The deployed
bundle runs inside a shadow root, where document.getElementById() returns
null and @font-face is ignored -- both silently. Same as every other page.

No libraries. Nothing on this page animates beyond a CSS keyframe.
"""
import html as _html
import re, sys, pathlib

HERE = pathlib.Path(__file__).parent
SRC  = HERE / "Parallaxx Speaking.dc.html"
JS   = HERE / "parallaxx-speaking.js"
PREV = HERE / "speaking-preview.html"
TAG  = "parallaxx-speaking"
ROOT = "sp-root"

# name -> (pixel size, the brief). The brief is the whole point: a slot that
# says "image here" gets filled with whatever is nearest, which is how a page
# ends up with a stock microphone on it.
SLOTS = {
    "HERO": ("2400 x 1350", "You mid-session with the audience in the frame. "
                            "Wide, taken from the side or the back, and you "
                            "off-centre -- the headline sits over the left "
                            "third and the bottom third goes dark under the "
                            "gradient."),
    "WORK": ("1200 x 1500", "Closer, and portrait. You working with a handful "
                            "of people rather than presenting to a full "
                            "audience. Faces, hands, somebody mid-sentence."),
    "ROOM": ("2400 x 1050", "The audience, not you. Faces absorbed, phones "
                            "down. Wide enough to read as a real event. This "
                            "one carries a caption naming the event and the "
                            "year, so pick a photograph you can name."),
    "AFTER": ("1600 x 1200", "The end of it. People talking to each other "
                             "rather than to you -- this is the photograph "
                             "that proves the headline, so it matters more "
                             "than it looks like it does."),
}

SHIP = "--ship" in sys.argv
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
    sys.exit("FAIL: an animation library is loaded or called in the source. "
             "Nothing on this page needs one.")
for api in ("localStorage", "sessionStorage"):
    if re.search(r"\b%s\s*[.\[]" % api, src):
        sys.exit(f"FAIL: {api} used in source.")

# Every declared slot has to still be referenced somewhere, or the table and
# the page have drifted and the briefs are describing photographs nobody is
# going to be asked for.
declared = set(SLOTS)
referenced = set(re.findall(r"IMAGE_SLOT_([A-Z0-9_]+)", src))
orphan_tokens = referenced - declared
if orphan_tokens:
    sys.exit("FAIL: the source references slots with no brief in SLOTS: %s. "
             "Add the brief, or the photograph gets guessed."
             % ", ".join(sorted(orphan_tokens)))

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

# ---- slots ----------------------------------------------------------------
SLOT_IMG = re.compile(r'<img\s+src="IMAGE_SLOT_([A-Z0-9_]+)"[^>]*>')

def render_slot(m):
    name = m.group(1)
    size, brief = SLOTS[name]
    return ('<div class="sp-slot" role="img" aria-label="Photograph still to come: %s">'
            '<p class="tag">Image slot &middot; %s</p>'
            '<p class="brief">%s</p>'
            '<p class="dim">%s &middot; replace IMAGE_SLOT_%s in the source</p>'
            '</div>') % (_html.escape(brief), name, _html.escape(brief), size, name)

empty = sorted(set(SLOT_IMG.findall(HTML)))
if SHIP and empty:
    print("FAIL: %d image slot(s) still empty, so this cannot ship:\n" % len(empty))
    for n in empty:
        size, brief = SLOTS[n]
        print("  IMAGE_SLOT_%-6s  %-12s  %s" % (n, size, brief))
    print("\nPut the file in migration/wix-assets/img/ and replace the token")
    print("with /assets/img/<filename> in Parallaxx Speaking.dc.html.")
    sys.exit(1)
# Check for stray tokens BEFORE substituting, not after: the rendered slot
# prints the token name on purpose so whoever is filling it knows what to
# search for, and a naive after-check flags that as the bug.
if "IMAGE_SLOT_" in SLOT_IMG.sub("", HTML):
    sys.exit("FAIL: an IMAGE_SLOT_ token appears outside an <img src=\"...\">. "
             "It would ship as literal text on the page.")
HTML = SLOT_IMG.sub(render_slot, HTML)

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
    sys.exit("FAIL: classList called on root. In the bundle that is a shadow root.")
if "pt-nav" not in HTML or "pt-foot" not in HTML:
    sys.exit("FAIL: the nav or the footer is missing. Site Header and Footer are "
             "OFF for this page, so it would ship with no way out of itself.")

font_links = re.findall(r'<link href="([^"]+)" rel="stylesheet">',
                        "\n".join(lines[:opens[0] + 30]))
fonts = "\n".join(
    "    var f%d=document.createElement('link'); f%d.rel='stylesheet'; f%d.href=%r; "
    "document.head.appendChild(f%d);" % (i, i, i, u, i)
    for i, u in enumerate(font_links))

JS.write_text("""/* PARALLAXX TRANSFORMATIONS - Speaking & Facilitating. Custom Element.
   Tag: %s.
   GENERATED by build-speaking-bundle.py from "Parallaxx Speaking.dc.html".
   DO NOT EDIT THIS FILE - edit the .dc.html and rerun the build.

   PtNav v3 and PtFooter v3 are baked in, so site Header and Footer must be
   OFF, same as every other page in the README table.

   %s */
(function(){
  if (customElements.get('%s')) return;

  var CSS = `%s`;

  var HTML = `%s`;

  function addFonts(){
    if (document.getElementById('sp-fonts')) return;
    var p1=document.createElement('link'); p1.rel='preconnect'; p1.href='https://fonts.googleapis.com'; document.head.appendChild(p1);
    var p2=document.createElement('link'); p2.rel='preconnect'; p2.href='https://fonts.gstatic.com'; p2.crossOrigin=''; document.head.appendChild(p2);
%s
    /* @font-face has to live in the DOCUMENT, not the shadow root. Chrome
       ignores font-face rules declared inside a shadow tree. */
    var ff=document.createElement('style'); ff.id='sp-fonts'; ff.textContent=`%s`; document.head.appendChild(ff);
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

  class ParallaxxSpeaking extends HTMLElement {
    connectedCallback(){
      if (this._mounted) return; this._mounted = true;
      addFonts();
      var shadow = this.attachShadow({mode:'open'});
      shadow.innerHTML = '<style>'+CSS+'</style>'+HTML;
      var host = this;
      try{ boot(shadow); }catch(e){ console.error('[sp] boot failed:', e); }
      requestAnimationFrame(function(){ collapseAncestors(host); });
      [400,1200,2500].forEach(function(t){ setTimeout(function(){ collapseAncestors(host); }, t); });
      window.addEventListener('resize', function(){ collapseAncestors(host); }, {passive:true});
      /* Photographs arriving late change the height by hundreds of pixels. */
      if (window.ResizeObserver){
        try{ new ResizeObserver(function(){ collapseAncestors(host); }).observe(host); }catch(e){}
      }
    }
  }
  customElements.define('%s', ParallaxxSpeaking);
})();
""" % (TAG,
       ("THIS BUILD STILL CARRIES %d EMPTY IMAGE SLOT(S): %s. Run\n   build-speaking-bundle.py --ship before deploying."
        % (len(empty), ", ".join(empty))) if empty else "All image slots are filled.",
       TAG, CSS, HTML, fonts, FONTFACE, ROOT, BOOTBODY, TAG), encoding="utf-8")

PREV.write_text("""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>Speaking &amp; Facilitating &mdash; Parallaxx Transformations</title>
<meta name="description" content="Daniel Lawson facilitates other people's retreats, offsites and stages.">
<meta name="robots" content="noindex">
<!-- GENERATED by build-speaking-bundle.py from "Parallaxx Speaking.dc.html".
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

print("built %s  css=%d  html=%d  boot=%d" % (JS.name, len(CSS), len(HTML), len(BOOTBODY)))
print("built %s" % PREV.name)
if empty:
    print("\n%d image slot(s) still empty -- the page renders them as briefs:" % len(empty))
    for n in empty:
        print("  IMAGE_SLOT_%-6s %s" % (n, SLOTS[n][0]))
    print("Run with --ship to block a deploy while any remain.")
else:
    print("all image slots filled")

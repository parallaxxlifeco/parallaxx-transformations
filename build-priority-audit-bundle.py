#!/usr/bin/env python3
"""
Build parallaxx-priority-audit.js AND priority-audit-preview.html
from "Priority Audit.dc.html".

    python3 build-priority-audit-bundle.py

THE .dc.html IS THE SOURCE OF RECORD. Both outputs are generated and are
overwritten on every run. Never hand-edit either of them.

  Source  : Priority Audit.dc.html
  Bundle  : parallaxx-priority-audit.js      (Wix custom element)
  Preview : priority-audit-preview.html      (open it in a browser)
  Tag     : parallaxx-priority-audit
  Root    : pa-root

WHY A BUILD STEP AT ALL
Same three reasons as build-home-men-bundle.py. The .dc.html runs inside
Wix's Design Code runtime, where the component sits in the light DOM. The
deployed bundle runs inside a shadow root, and three things differ, all of
which fail SILENTLY rather than throwing:

  1. document.getElementById() returns null inside a shadow root.
  2. GSAP resolves STRING selectors against document, so any ScrollTrigger
     keyed to a string gets a null trigger and never runs.
  3. @font-face declared inside a shadow tree is ignored by Chrome, so the
     font rules have to be injected into document.head separately.

And one more that is specific to this component, because it is the only
one on the site that is keyboard driven end to end:

  4. document.activeElement returns the shadow HOST, not the focused node
     inside it. The source therefore routes every focus read through the
     focused() helper, and the guard below refuses to ship without it.

WHY THE PREVIEW IS GENERATED TOO
The men's quiz and its previews drifted from their sources because both
were maintained by hand. There is one set of words in this instrument and
it lives in the .dc.html. The preview is the same CSS, the same markup and
the same script, wrapped in a page shell with a header and a footer that
Wix supplies in production.
"""
import re, sys, pathlib

HERE = pathlib.Path(__file__).parent
SRC  = HERE / "Priority Audit.dc.html"
JS   = HERE / "parallaxx-priority-audit.js"
PREV = HERE / "priority-audit-preview.html"
TAG  = "parallaxx-priority-audit"
ROOT = "pa-root"

src = SRC.read_text(encoding="utf-8")

# ---- guards on the SOURCE -------------------------------------------------
if "`" in src:
    bad = [i + 1 for i, l in enumerate(src.split("\n")) if "`" in l]
    sys.exit(f"FAIL: backtick in source (lines {bad}). CSS and HTML are embedded "
             f"in template literals; a backtick terminates them and silently "
             f"destroys the stylesheet. Use single quotes.")
if "${" in src:
    sys.exit("FAIL: '${' in source would interpolate inside the template literal.")
if re.search(r"trigger:\s*'#", src):
    sys.exit("FAIL: GSAP ScrollTrigger keyed to a string selector. Inside a "
             "shadow root that resolves to null and the tween never runs. "
             "Use document.getElementById('...') so the converter rewrites it.")
if "const focused =" not in src:
    sys.exit("FAIL: no focused() helper. document.activeElement returns the "
             "shadow HOST inside a shadow root, so arrow-key movement on the "
             "scale would silently stop working in the deployed bundle.")
# Usage, not mentions. The source comments say the words on purpose, so the
# guard looks for a property read or a subscript rather than the bare noun.
for api in ("localStorage", "sessionStorage"):
    if re.search(r"\b%s\s*[.\[]" % api, src):
        sys.exit(f"FAIL: {api} used in source. Browser storage is unavailable "
                 f"in the target environments and a failed write takes the "
                 f"result screen with it. Answers live in memory only.")

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
# The x-dc script sits inside the markup range; the bundle supplies it as
# boot() instead, so it must not be copied into the HTML template.
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

font_links = re.findall(r'<link href="([^"]+)" rel="stylesheet">',
                        "\n".join(lines[:opens[0] + 30]))
fonts = "\n".join(
    "    var f%d=document.createElement('link'); f%d.rel='stylesheet'; f%d.href=%r; "
    "document.head.appendChild(f%d);" % (i, i, i, u, i)
    for i, u in enumerate(font_links))

# ═══════════════════════════════════════════════════════════════════════════
# 1 · THE WIX CUSTOM ELEMENT
# ═══════════════════════════════════════════════════════════════════════════
JS.write_text("""/* PARALLAXX TRANSFORMATIONS - The Priority Audit. Wix Custom Element. Tag: %s.
   GENERATED by build-priority-audit-bundle.py from "Priority Audit.dc.html".
   DO NOT EDIT THIS FILE - edit the .dc.html and rerun the build.

   DEPLOY AS A CUSTOM ELEMENT, NOT AN HTML EMBED. An embed renders inside a
   fixed-height iframe, hides the site header and footer, and puts every word
   on a filesusr.com origin Google will not attribute to the site. Bump the
   ?v= on the source URL on every deploy so the CDN does not serve the old
   bundle. Page SEO lives in Wix page settings, not in here.

   In the Wix editor: Add -> Embed Code -> Custom Element.
     Source    the hosted URL of this file, with ?v= bumped
     Tag name  %s
   Leave the site Header and Footer ON. This is an instrument on a page,
   not a full-bleed page of its own. */
(function(){
  if (customElements.get('%s')) return;

  var CSS = `%s`;

  var HTML = `%s`;

  function addFonts(){
    if (document.getElementById('pa-fonts')) return;
    var p1=document.createElement('link'); p1.rel='preconnect'; p1.href='https://fonts.googleapis.com'; document.head.appendChild(p1);
    var p2=document.createElement('link'); p2.rel='preconnect'; p2.href='https://fonts.gstatic.com'; p2.crossOrigin=''; document.head.appendChild(p2);
%s
    /* @font-face has to live in the DOCUMENT, not the shadow root. Chrome
       ignores font-face rules declared inside a shadow tree. */
    var ff=document.createElement('style'); ff.id='pa-fonts'; ff.textContent=`%s`; document.head.appendChild(ff);
  }

  function loadScript(src){
    return new Promise(function(res,rej){
      var ex=document.querySelector('script[data-px="'+src+'"]');
      if(ex){ if(ex.getAttribute('data-loaded')){res();} else { ex.addEventListener('load',function(){res();}); ex.addEventListener('error',rej);} return; }
      var s=document.createElement('script'); s.src=src; s.async=false; s.setAttribute('data-px',src);
      s.addEventListener('load',function(){ s.setAttribute('data-loaded','1'); res(); });
      s.addEventListener('error',rej);
      document.head.appendChild(s);
    });
  }

  /* Every animation in here has a no-GSAP path and a reduced-motion path
     that simply shows the content, so a library that never arrives costs
     the visitor nothing but the easing. */
  function loadLibs(){
    var g=loadScript('https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.5/gsap.min.js')
      .then(function(){ return loadScript('https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.5/ScrollTrigger.min.js'); });
    var l=loadScript('https://unpkg.com/lenis@1.1.13/dist/lenis.min.js');
    return Promise.all([ g.catch(function(){}), l.catch(function(){}) ]);
  }

  /* Wix wraps a custom element in a fixed-height container sized from the
     editor. This component changes height four times (intro, items, turn,
     result), so the wrapper has to be told to follow it. */
  function collapseAncestors(host){
    var changed = false;
    try{ var h=host.getBoundingClientRect().height; if(h<50) return false;
      var n=host.parentElement,guard=0;
      while(n && n!==document.body && guard++<14){ if(n.getBoundingClientRect().height>h+600){ n.style.height='auto'; n.style.minHeight='0px'; changed = true; } n=n.parentElement; }
    }catch(e){}
    return changed;
  }

  function collapseAndRefresh(host){
    var changed = collapseAncestors(host);
    if (changed && window.ScrollTrigger) { try{ window.ScrollTrigger.refresh(); }catch(e){} }
  }

  function boot(root){
    if(!root || !root.getElementById('%s')) return;
%s
  }

  class ParallaxxPriorityAudit extends HTMLElement {
    connectedCallback(){
      if (this._mounted) return; this._mounted = true;
      addFonts();
      var shadow = this.attachShadow({mode:'open'});
      shadow.innerHTML = '<style>'+CSS+'</style>'+HTML;
      var host = this;
      loadLibs().then(function(){ try{ boot(shadow); }catch(e){ console.error('[pa] boot failed:', e); } })
        .catch(function(){ try{ boot(shadow); }catch(e){} });
      requestAnimationFrame(function(){ collapseAndRefresh(host); });
      [400,1200,2500].forEach(function(t){ setTimeout(function(){ collapseAndRefresh(host); }, t); });
      window.addEventListener('resize', function(){ collapseAndRefresh(host); }, {passive:true});
      /* The screen swaps change the element's height by thousands of pixels
         and Wix has already cached the old one. */
      new MutationObserver(function(){ collapseAndRefresh(host); })
        .observe(shadow, {subtree:true, attributes:true, attributeFilter:['class']});
    }
  }
  customElements.define('%s', ParallaxxPriorityAudit);
})();
""" % (TAG, TAG, TAG, CSS, HTML, fonts, FONTFACE, ROOT, BOOTBODY, TAG), encoding="utf-8")

# ═══════════════════════════════════════════════════════════════════════════
# 2 · THE STANDALONE PREVIEW
# Same CSS, same markup, same script. A page shell around it, because in
# production Wix supplies the header and footer and here nothing does.
# ═══════════════════════════════════════════════════════════════════════════
SHELL_CSS = """
  html{-webkit-text-size-adjust:100%;scroll-behavior:smooth}
  body{margin:0;background:#04122A}
  .pv-head{position:sticky;top:0;z-index:60;background:rgba(4,18,42,.86);
    backdrop-filter:blur(14px);border-bottom:1px solid rgba(232,198,95,.14)}
  .pv-in{max-width:1240px;margin:0 auto;padding:14px clamp(20px,4vw,52px);
    display:flex;align-items:center;justify-content:space-between;gap:20px}
  .pv-head img{height:32px;width:auto;display:block}
  .pv-foot{border-top:1px solid #12233F;background:#030C1C;padding:30px 0}
  .pv-foot-in{max-width:1240px;margin:0 auto;padding:0 clamp(20px,4vw,52px);
    display:flex;flex-wrap:wrap;align-items:center;justify-content:space-between;gap:16px;
    font-family:'Montserrat',system-ui,sans-serif}
  .pv-foot a{color:#7C89A3;text-decoration:none;font-size:.8rem}
  .pv-foot a:hover{color:#F1ECE1}
  .pv-foot nav{display:flex;flex-wrap:wrap;gap:20px}
  .pv-foot small{color:#5E6B85;font-size:.74rem}
  @media print{.pv-head,.pv-foot{display:none!important}body{background:#fff}}
"""

PREV.write_text("""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>The Priority Audit &mdash; Parallaxx Transformations</title>
<meta name="description" content="Fifteen statements about your working week, and the three things they were measuring. About ninety seconds.">
<meta name="robots" content="noindex">
<!-- GENERATED by build-priority-audit-bundle.py from "Priority Audit.dc.html".
     DO NOT EDIT - edit the .dc.html and rerun the build.
     This is the local review harness. In production the component ships as
     parallaxx-priority-audit.js and Wix supplies the header and footer.
     Review deep links:  ?state=needs  ?state=boundaries  ?state=emotions  ?state=flat -->
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
%s
<style>%s</style>
<style>%s</style>
<style>%s</style>
</head>
<body>

<header class="pv-head">
  <div class="pv-in">
    <a href="https://www.parallaxxtransformations.com" aria-label="Parallaxx Transformations">
      <img src="https://static.wixstatic.com/media/e1784d_fe3c841c471f47d088f0cd631a89d883~mv2.png/v1/fill/w_260,h_57,al_c,q_90,enc_avif,quality_auto/Parallaxx%%20Transformation%%20Logo%%20Design%%20White%%20(1).png" alt="Parallaxx Transformations" width="260" height="57">
    </a>
  </div>
</header>

%s

<footer class="pv-foot">
  <div class="pv-foot-in">
    <small>&copy; <span id="pv-yr"></span> Parallaxx Transformations</small>
    <nav>
      <a href="https://www.parallaxxtransformations.com/about-daniel-lawson">About</a>
      <a href="https://www.parallaxxtransformations.com/the-reconnected-woman">The Reconnected Woman</a>
      <a href="https://www.parallaxxtransformations.com/contact-daniel-lawson">Contact</a>
      <a href="https://www.parallaxxtransformations.com/privacy-policy">Privacy</a>
    </nav>
  </div>
</footer>

<script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.5/gsap.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.5/ScrollTrigger.min.js"></script>
<script src="https://unpkg.com/lenis@1.1.13/dist/lenis.min.js"></script>
<script>
(function(){
  var y = document.getElementById('pv-yr');
  if (y) y.textContent = String(new Date().getFullYear());
%s
})();
</script>
</body>
</html>
""" % ("\n".join('<link href="%s" rel="stylesheet">' % u for u in font_links),
       FONTFACE, CSS, SHELL_CSS, HTML, body), encoding="utf-8")

print("built %s  css=%d  html=%d  boot=%d  fonts=%d" % (JS.name, len(CSS), len(HTML), len(BOOTBODY), len(font_links)))
print("built %s" % PREV.name)

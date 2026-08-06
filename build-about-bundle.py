#!/usr/bin/env python3
"""
Build parallaxx-about-page.js from "Parallaxx About v4.dc.html".

Same contract as build-home-men-bundle.py: the .dc.html is the SOURCE OF RECORD,
this script converts it into the self-contained shadow-DOM custom element
that Wix loads, and parallaxx-about-page.js is overwritten every run.

    python3 build-about-bundle.py

WHY A BUILD STEP AT ALL
The .dc.html runs inside Wix's Design Code runtime, where the component is
in the light DOM. The deployed bundle runs inside a shadow root. Three
things differ, and all three fail SILENTLY rather than throwing:

  1. document.getElementById() returns null inside a shadow root.
  2. GSAP resolves STRING selectors ('#pxa-hero') against document, so any
     ScrollTrigger keyed to a string gets a null trigger and never scrubs.
  3. @font-face declared inside a shadow tree is ignored by Chrome, so
     fonts have to be injected into document.head separately.

The guards below fail the build rather than shipping any of those.
"""
import re, sys, pathlib

HERE = pathlib.Path(__file__).parent
SRC  = HERE / "Parallaxx About v4.dc.html"
OUT  = HERE / "parallaxx-about-page.js"
TAG  = "parallaxx-about-page"
ROOT = "pxa-root"

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
if "style-hover" in src:
    sys.exit("FAIL: style-hover attribute in source. That is a DC-runtime "
             "feature and it does not exist in the deployed bundle, so the "
             "hover state would silently never fire. Use a CSS class.")

lines = src.split("\n")

def style_block(open_line_idx):
    close = next(k for k in range(open_line_idx + 1, len(lines))
                 if lines[k].strip() == "</style>")
    return "\n".join(lines[open_line_idx + 1:close])

opens = [i for i, l in enumerate(lines) if l.strip() == "<style>"]
if len(opens) < 2:
    sys.exit("FAIL: expected a @font-face <style> and a main <style> in the helmet.")
FONTFACE = style_block(opens[0])
# Block 0 is @font-face and has to reach document.head on its own. Every other
# block is page or chrome CSS, concatenated in source order: the page sheet
# (which carries PtNav v3), then PtFooter v3.
CSS = "\n\n".join(style_block(i) for i in opens[1:])

# Everything between </helmet> and </x-dc>, which is the same contract
# build-chrome-bundles.py uses. It used to start at the page root instead,
# and that silently dropped the site nav when the nav was baked in above it:
# the bundle built clean and shipped with no header.
h0 = next(i for i, l in enumerate(lines) if l.strip() == "</helmet>") + 1
h1 = next(i for i, l in enumerate(lines) if l.rstrip() == "</x-dc>")
HTML = "\n".join(lines[h0:h1]).rstrip()

js = src[src.index('<script type="text/x-dc"'):]
js = js[js.index(">") + 1:js.index("</script>")]
body = js[js.index("componentDidMount(){") + len("componentDidMount(){"):]
body = body[:body.rindex("renderVals()")].rstrip()
body = body[:body.rindex("}")].rstrip()          # drop componentDidMount's closer

body = body.replace(
    "    const root = document.getElementById('%s');\n    if(!root) return;\n" % ROOT, "")
body = body.replace("document.getElementById(", "root.getElementById(")

# ---- guards on the OUTPUT -------------------------------------------------
if "const root =" in body:
    sys.exit("FAIL: local root binding survived; it would shadow boot()'s parameter.")
if "document.getElementById" in body:
    sys.exit("FAIL: a document.getElementById survived the rewrite.")


if '<header id="pt-nav">' not in HTML:
    sys.exit("FAIL: the nav markup is not in the extracted HTML.")
if '<footer id="pt-foot">' not in HTML:
    sys.exit("FAIL: the footer markup is not in the extracted HTML. This page "
             "shipped with nothing at the bottom once; the guard is here so it "
             "cannot happen quietly again.")
if "#pt-foot{" not in CSS:
    sys.exit("FAIL: the footer stylesheet did not make it into CSS.")
if "pt-year" not in body:
    sys.exit("FAIL: the copyright-year logic is missing from the bundle body.")
font_links = re.findall(r'<link href="([^"]+)" rel="stylesheet">',
                        "\n".join(lines[:opens[0] + 30]))
fonts = "\n".join(
    "    var f%d=document.createElement('link'); f%d.rel='stylesheet'; f%d.href=%r; "
    "document.head.appendChild(f%d);" % (i, i, i, u, i)
    for i, u in enumerate(font_links))

OUT.write_text("""/* PARALLAXX TRANSFORMATIONS - About page Wix Custom Element. Tag: %s.
   GENERATED by build-about-bundle.py from "Parallaxx About v4.dc.html".
   DO NOT EDIT THIS FILE - edit the .dc.html and rerun the build.
   In the Wix editor: turn the site Header + Footer OFF for this page, and
   place PtNav (active="about") and PtFooter as their own custom elements. */
(function(){
  if (customElements.get('%s')) return;

  var CSS = `%s`;

  var HTML = `%s`;

  function addFonts(){
    if (document.getElementById('px-fonts')) return;
    var p1=document.createElement('link'); p1.rel='preconnect'; p1.href='https://fonts.googleapis.com'; document.head.appendChild(p1);
    var p2=document.createElement('link'); p2.rel='preconnect'; p2.href='https://fonts.gstatic.com'; p2.crossOrigin=''; document.head.appendChild(p2);
%s
    /* @font-face has to live in the DOCUMENT, not the shadow root. Chrome
       ignores font-face rules declared inside a shadow tree. */
    var ff=document.createElement('style'); ff.id='px-fonts'; ff.textContent=`%s`; document.head.appendChild(ff);
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

  function loadLibs(){
    var g=loadScript('https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.5/gsap.min.js')
      .then(function(){ return loadScript('https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.5/ScrollTrigger.min.js'); });
    var l=loadScript('https://unpkg.com/lenis@1.1.13/dist/lenis.min.js');
    return Promise.all([ g.catch(function(){}), l.catch(function(){}) ]);
  }

  /* This rewrites ancestor heights, which moves every scroll position on the
     page. ScrollTrigger has already cached those positions, so without a
     refresh afterwards its triggers fire at the wrong offsets. Returns
     whether it actually changed anything so the caller can avoid refreshing
     for nothing. */
  /* Measures the real content inside the shadow root. A fixed-position child
     (the site nav) takes no space in flow, so summing children and skipping
     fixed ones is the only honest number: scrollHeight would miss it too and
     offsetHeight of the host is the very thing we are trying to check. */
  /* Runaway guards. This loop once grew a document to Chrome's 2^24 clamp,
     so every element is one-shot and the whole thing bails if the page is
     already absurd. */
  var PX_SANE_MAX = 200000;              // taller than any real page here
  var pxCollapsed = new WeakSet();

  /* Sums the real content inside the shadow root. A fixed-position child (a
     baked-in site nav) takes no space in flow, so summing children and
     skipping fixed ones is the only honest number. */
  function contentHeight(host){
    var total = 0;
    try{
      var kids = host.shadowRoot ? host.shadowRoot.children : [];
      for (var i=0;i<kids.length;i++){
        var c = kids[i];
        if (c.tagName === 'STYLE') continue;
        var cs = window.getComputedStyle(c);
        if (cs.position === 'fixed' || cs.display === 'none') continue;
        total += c.getBoundingClientRect().height;
      }
    }catch(e){}
    return total;
  }

  /* WHAT THIS IS ACTUALLY FIXING, measured on the live About page 5 Aug.
     59851px of page with 5790px of content in it: fifty thousand pixels of
     empty section under the footer. Wix writes the widget height the editor
     last recorded into an INLINE STYLESHEET RULE, not an inline style:

         #comp-msfv7drl { height: 59851px }
         #comp-msfv7drl { --custom-element-height: 59851px }

     Two consequences, and the previous version of this function missed both.

     1. A plain host.style.height = 'auto' LOSES to that rule. Every write
        here has to be setProperty with 'important' or nothing moves.
     2. The rule sits on the PARENT and the host stretches to match, so host
        and parent measure identically. Comparing each ancestor against the
        HOST and asking for a 600px difference therefore compares a number
        with itself. It never fired, on any page, for the exact case it was
        written for. Everything is measured against the CONTENT now.

     Verified in the browser before shipping: 59851 -> 5790, and it held.

     THE RUNAWAY GUARDS STAY. They are not paranoia: this loop once grew a
     document to Chrome's 2^24 clamp. Every element is one-shot via the
     WeakSet, and the whole thing bails if the page is already absurd. */
  function collapseAncestors(host){
    var changed = false;
    try{
      if (document.documentElement.scrollHeight > PX_SANE_MAX) return false;
      var content = contentHeight(host);
      if (content < 50) return false;

      if (!pxCollapsed.has(host) && host.getBoundingClientRect().height > content + 24){
        pxCollapsed.add(host);
        if (window.getComputedStyle(host).display === 'inline') host.style.setProperty('display','block','important');
        host.style.setProperty('height','auto','important');
        host.style.setProperty('min-height','0px','important');
        host.style.setProperty('max-height','none','important');
        changed = true;
      }

      var n = host.parentElement, guard = 0;
      while(n && n !== document.body && guard++ < 14){
        if(!pxCollapsed.has(n) && n.getBoundingClientRect().height > content + 240){
          pxCollapsed.add(n);
          n.style.setProperty('height','auto','important');
          n.style.setProperty('min-height','0px','important');
          n.style.setProperty('max-height','none','important');
          n.style.setProperty('--custom-element-height','auto','important');
          changed = true;
        }
        n = n.parentElement;
      }
    }catch(e){}
    return changed;
  }

  function collapseAndRefresh(host){
    var changed = collapseAncestors(host);
    if (changed && window.ScrollTrigger) {
      try{ window.ScrollTrigger.refresh(); }catch(e){}
    }
  }

  function boot(root){
    if(!root || !root.getElementById('%s')) return;
%s
  }

  class ParallaxxAboutPage extends HTMLElement {
    connectedCallback(){
      if (this._mounted) return; this._mounted = true;
      addFonts();
      var shadow = this.attachShadow({mode:'open'});
      shadow.innerHTML = '<style>'+CSS+'</style>'+HTML;
      var host = this;
      loadLibs().then(function(){ try{ boot(shadow); }catch(e){ console.error('[pxa] boot failed:', e); } })
        .catch(function(){ try{ boot(shadow); }catch(e){} });
      requestAnimationFrame(function(){ collapseAndRefresh(host); });
      [400,1200,2500,4000,6000].forEach(function(t){ setTimeout(function(){ collapseAndRefresh(host); }, t); });
      /* Images arriving late change the content height, and Wix can
         re-apply its stored height after its own layout settles. Watching
         the host is cheaper and more reliable than guessing more timeouts. */
      if (window.ResizeObserver){
        try{ new ResizeObserver(function(){ collapseAndRefresh(host); }).observe(host); }catch(e){}
      }
      window.addEventListener('resize', function(){ collapseAndRefresh(host); }, {passive:true});
    }
  }
  customElements.define('%s', ParallaxxAboutPage);
})();
""" % (TAG, TAG, CSS, HTML, fonts, FONTFACE, ROOT, body, TAG), encoding="utf-8")

print(f"built {OUT.name}  css={len(CSS)}  html={len(HTML)}  boot={len(body)}  fonts={len(font_links)}")

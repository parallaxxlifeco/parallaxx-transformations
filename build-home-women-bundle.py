#!/usr/bin/env python3
"""
Build parallaxx-home-women.js from "Parallaxx Home Women.dc.html".

This is the WOMEN'S avatar page, sister to "Parallaxx Home Men.dc.html".
  Bundle : parallaxx-home-women.js
  Tag    : parallaxx-home-women
  Preview: home-women.html

The .dc.html is the SOURCE OF RECORD. Never hand-edit the generated .js.

    python3 build-home-women-bundle.py

HOW THIS DIFFERS FROM THE MEN'S BUILD, AND WHY IT NEEDED ITS OWN SCRIPT

The men's page is authored as a Design Code component: one
<script type="text/x-dc"> holding a class with componentDidMount, and two
<style> blocks. This page is not. It is assembled from parts by build.py and
ships as plain markup with two ordinary <script> blocks and three <style>
blocks. Pointing the men's build at it fails on all three counts.

  1. THREE STYLESHEETS, not two. The font-face block, the inherited v4
     sheet, and this page's own sheet. Two and three concatenate; only the
     first goes to document.head.

  2. TWO SCRIPTS, not one. The page module and the Priority Audit, which was
     ported wholesale from the standalone rather than rewritten. They run in
     order and share nothing but the DOM.

  3. EACH SCRIPT BINDS ITS OWN ROOT. The page module opens with
     `const root = document`, the audit with
     `const root = document.getElementById('pa-root')`. Inside a shadow root
     both resolve to the wrong thing, silently: document.getElementById
     returns null from inside a shadow tree, so the audit would simply never
     start and the page would look fine while its only instrument was dead.
     The rewrites below are checked by guards rather than trusted.

The audit's $ helper is `id => document.getElementById(id)` and is rewritten
the same way. document.createElement, document.head and document.body are
left alone on purpose: those genuinely belong to the document.
"""
import re, sys, pathlib

HERE = pathlib.Path(__file__).parent
SRC  = HERE / "Parallaxx Home Women.dc.html"
OUT  = HERE / "parallaxx-home-women.js"
TAG  = "parallaxx-home-women"

src = SRC.read_text(encoding="utf-8")

# ---- guards on the SOURCE -------------------------------------------------
if "`" in src:
    bad = [i + 1 for i, l in enumerate(src.split("\n")) if "`" in l]
    sys.exit(f"FAIL: backtick in source (lines {bad}). CSS, HTML and the two "
             f"scripts are embedded in template literals; a backtick "
             f"terminates them and silently destroys the bundle.")
if "${" in src:
    sys.exit("FAIL: '${' in source would interpolate inside the template literal.")
if re.search(r"trigger:\s*'#", src):
    sys.exit("FAIL: GSAP ScrollTrigger keyed to a string selector. Inside a "
             "shadow root that resolves to null and the tween never runs.")
# Usage, not mentions: the audit carries a comment saying it uses neither,
# and that comment should not fail its own build.
if re.search(r"(?<![\w.])(local|session)Storage\s*[.\[]", src):
    sys.exit("FAIL: storage API in use. Unavailable in the target runtime, "
             "and a failed write takes the result screen with it.")

lines = src.split("\n")

def block(open_idx, closer):
    close = next(k for k in range(open_idx + 1, len(lines))
                 if lines[k].strip() == closer)
    return "\n".join(lines[open_idx + 1:close]), close

# ---- stylesheets ----------------------------------------------------------
opens = [i for i, l in enumerate(lines) if l.strip() == "<style>"]
if len(opens) != 3:
    sys.exit(f"FAIL: expected 3 <style> blocks (font-face, v4 sheet, page "
             f"sheet); found {len(opens)}.")
FONTFACE, _ = block(opens[0], "</style>")
BASE, _     = block(opens[1], "</style>")
PAGE, _     = block(opens[2], "</style>")
CSS = BASE + "\n\n" + PAGE

# ---- markup ---------------------------------------------------------------
h0 = next(i for i, l in enumerate(lines) if l.startswith('<div id="px-root">'))
h1 = next(i for i, l in enumerate(lines) if l.strip() == "<script>"
          and i > h0)
HTML = "\n".join(lines[h0:h1]).rstrip()
if "</div>" not in HTML:
    sys.exit("FAIL: markup slice looks wrong.")

# ---- the two scripts ------------------------------------------------------
starts = [i for i, l in enumerate(lines) if l.strip() == "<script>" and i > h0]
if len(starts) != 2:
    sys.exit(f"FAIL: expected 2 page <script> blocks; found {len(starts)}.")
bodies = []
for i in starts:
    b, _ = block(i, "</script>")
    bodies.append(b)
PAGE_JS, AUDIT_JS = bodies

# ---- rebind both roots to the shadow --------------------------------------
if "const root = document;" not in PAGE_JS:
    sys.exit("FAIL: page module no longer opens with 'const root = document;'.")
PAGE_JS = PAGE_JS.replace("const root = document;", "const root = SHADOW;", 1)

for a, b in [("const root = document.getElementById('pa-root');",
              "const root = SHADOW.getElementById('pa-root');"),
             ("const $ = id => document.getElementById(id);",
              "const $ = id => SHADOW.getElementById(id);")]:
    if a not in AUDIT_JS:
        sys.exit(f"FAIL: audit no longer contains {a!r}; the rewrite would "
                 f"leave it bound to the document and it would never start.")
    AUDIT_JS = AUDIT_JS.replace(a, b, 1)

BODY = PAGE_JS + "\n\n" + AUDIT_JS

# ---- guards on the OUTPUT -------------------------------------------------
leftover = [l for l in BODY.split("\n")
            if "document.getElementById" in l or "document.querySelector" in l]
if leftover:
    sys.exit("FAIL: a document lookup survived the rewrite:\n  " +
             "\n  ".join(l.strip()[:90] for l in leftover[:5]))
if "SHADOW" not in BODY:
    sys.exit("FAIL: no shadow binding in the output.")

# ---- template-literal safety ----------------------------------------------
# CSS, HTML and the font-face block are embedded inside backticks. A backslash
# survives Python's %-format untouched and is then read by JS as an escape, so
# a CSS codepoint escape like content:'\201C' becomes an octal escape and the
# whole bundle fails to parse. Backticks and ${ are already refused above; the
# backslash is the one that cannot be, because CSS legitimately needs it.
def lit(t):
    return t.replace("\\", "\\\\")

CSS, HTML, FONTFACE = lit(CSS), lit(HTML), lit(FONTFACE)
# BODY is NOT escaped: it is emitted as raw JS inside boot(), not inside a
# template literal, so its own escapes have to reach the engine intact.

font_links = re.findall(r'<link href="([^"]+)" rel="stylesheet">',
                        "\n".join(lines[:opens[0] + 30]))
fonts = "\n".join(
    "    var f%d=document.createElement('link'); f%d.rel='stylesheet'; f%d.href=%r; "
    "document.head.appendChild(f%d);" % (i, i, i, u, i)
    for i, u in enumerate(font_links))

OUT.write_text("""/* PARALLAXX TRANSFORMATIONS - Home, women's avatar. Wix Custom Element.
   Tag: %s
   GENERATED by build-home-women-bundle.py from "Parallaxx Home Women.dc.html".
   DO NOT EDIT THIS FILE - edit the .dc.html and rerun the build.
   In the Wix editor: place PtNav in the site header strip and PtFooter in the
   footer strip, and leave both ON for this page. This element is the page
   content between them, not the whole page. */
(function(){
  if (customElements.get('%s')) return;

  var CSS = `%s`;

  var HTML = `%s`;

  function addFonts(){
    if (document.getElementById('px-fonts-w')) return;
    var p1=document.createElement('link'); p1.rel='preconnect'; p1.href='https://fonts.googleapis.com'; document.head.appendChild(p1);
    var p2=document.createElement('link'); p2.rel='preconnect'; p2.href='https://fonts.gstatic.com'; p2.crossOrigin=''; document.head.appendChild(p2);
%s
    /* @font-face has to live in the DOCUMENT, not the shadow root. Chrome
       ignores font-face rules declared inside a shadow tree. */
    var ff=document.createElement('style'); ff.id='px-fonts-w'; ff.textContent=`%s`; document.head.appendChild(ff);
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

  /* Rewrites ancestor heights, which moves every scroll position on the page.
     ScrollTrigger has already cached those, so a refresh has to follow.
     Returns whether anything actually changed so we do not refresh for
     nothing. */
  function collapseAncestors(host){
    var changed = false;
    try{ var h=host.getBoundingClientRect().height; if(h<50) return false;
      var n=host.parentElement,guard=0;
      while(n && n!==document.body && guard++<14){ if(n.getBoundingClientRect().height>h+600){ n.style.height='auto'; n.style.minHeight='0px'; changed = true; } n=n.parentElement; }
    }catch(e){}
    return changed;
  }

  function collapseAndRefresh(host){
    if (collapseAncestors(host) && window.ScrollTrigger) {
      try{ window.ScrollTrigger.refresh(); }catch(e){}
    }
  }

  /* The audit runs its own reveal machinery and the page module runs
     another. Both are handed the shadow root as SHADOW; neither one
     touches the document for lookups. */
  function boot(SHADOW){
    if(!SHADOW || !SHADOW.getElementById('px-root')) return;
%s
  }

  class ParallaxxHomeWomen extends HTMLElement {
    connectedCallback(){
      if (this._mounted) return; this._mounted = true;
      addFonts();
      var shadow = this.attachShadow({mode:'open'});
      shadow.innerHTML = '<style>'+CSS+'</style>'+HTML;
      var host = this;
      loadLibs().then(function(){ try{ boot(shadow); }catch(e){ console.error('[px] boot failed:', e); } })
        .catch(function(){ try{ boot(shadow); }catch(e){} });
      requestAnimationFrame(function(){ collapseAndRefresh(host); });
      [400,1200,2500].forEach(function(t){ setTimeout(function(){ collapseAndRefresh(host); }, t); });
      window.addEventListener('resize', function(){ collapseAndRefresh(host); }, {passive:true});
    }
  }
  customElements.define('%s', ParallaxxHomeWomen);
})();
""" % (TAG, TAG, CSS, HTML, fonts, FONTFACE, BODY, TAG), encoding="utf-8")

print(f"built {OUT.name}  css={len(CSS)}  html={len(HTML)}  boot={len(BODY)}  fonts={len(font_links)}")

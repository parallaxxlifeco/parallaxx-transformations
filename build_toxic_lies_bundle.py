#!/usr/bin/env python3
"""Wrap the Three Toxic Lies preview as the custom element the site loads.

    Source URL  /parallaxx-toxic-lies.js
    Tag         parallaxx-toxic-lies
    Route       /three-toxic-lies

Same pattern as build_bundle_v10.py, and deliberately not the pattern the
older build-*-bundle.py scripts use. Those bake a copy of PtNav and PtFooter
into every bundle -- roughly 700 lines each -- which is how the nav drifted
between pages before. This one loads /parallaxx-nav.js and
/parallaxx-footer.js as shared bundles, so the chrome on this page is the
same object as the chrome on the other twelve, and there is nothing here to
keep in sync.

LIGHT DOM, on purpose. The stylesheet is scoped to #ttl-page and the page
script uses document.querySelector, so the reveals work with no rewriting.
Nav and footer attach their own shadow roots, so this page's styles cannot
reach into them.

The cover render is a Wix URL in the source. migration/build-site.py
--local rewrites them to /assets/img/... from migration/asset-map.json,
which is where the cropped cover now lives. Do not hand-edit them to local paths
here -- the map is the one place that mapping is recorded.
"""
import re, pathlib

HERE = pathlib.Path(__file__).parent
SRC = HERE / "toxic-lies-preview.html"
OUT = HERE / "parallaxx-toxic-lies.js"
TAG = "parallaxx-toxic-lies"

s = SRC.read_text(encoding="utf-8")

font_links = re.findall(
    r'<link[^>]*href="(https://fonts\.googleapis\.com[^"]+)"[^>]*>', s)

CSS = "\n".join(re.findall(r"<style>([\s\S]*?)</style>", s))

# The scroll rail sits outside #ttl-page so it can be fixed to the viewport,
# so the body slice starts there, not at the page root.
body_start = s.index('<div id="ttl-rail"')
body_end = s.index('<script src="/parallaxx-nav.js">')
HTML = s[body_start:body_end].strip()

PAGE_JS = "\n;\n".join(re.findall(r"<script>([\s\S]*?)</script>", s))

# A lone backslash inside a template literal starts an escape sequence, and
# CSS content values like \2014 read as octal, which is a hard syntax error.
CSS = CSS.replace("\\", "\\\\")
HTML = HTML.replace("\\", "\\\\")

for name, blob in (("CSS", CSS), ("HTML", HTML), ("PAGE_JS", PAGE_JS)):
    if "`" in blob or "${" in blob:
        raise SystemExit(
            "FAIL: backtick or dollar-brace in %s would break the template literal" % name)

assert 'id="ttl-page"' in HTML, "page root missing"
assert "parallaxx-nav" in HTML and "parallaxx-footer" in HTML, "chrome missing from the body"

# THE CHECKOUT. This page has one job and it is this link. A build that
# ships it with a dead or missing Stripe link ships a shop with no till.
STRIPE = "https://buy.stripe.com/5kA01L10meewbni008"
n_buy = HTML.count(STRIPE)
if n_buy != 3:
    raise SystemExit(
        "FAIL: the Stripe checkout link appears %d times, expected 3 "
        "(hero, what-you-get, close)." % n_buy)

# THE PRICE. It is printed in three places and they have to agree. Two of
# them are fine print, which is exactly the kind of line that gets left
# behind when a price changes.
prices = set(re.findall(r"&euro;([\d.,]+)", HTML))
if len(prices) != 1:
    raise SystemExit(
        "FAIL: more than one price on the page: %s" % sorted(prices))
print("price      EUR %s  (%d buy links)" % (prices.pop(), n_buy))

# THE COVER. The one asset this product has. A cover render that 404s leaves
# a page selling an object nobody can see.
_cover = "img/toxic-lies-cover.png"
if not (HERE / "migration" / "wix-assets" / _cover).exists():
    raise SystemExit("FAIL: %s is missing from migration/wix-assets/" % _cover)

# THE THREE LIES. The whole reason this page exists rather than the Wix one,
# which sold three outcomes and never named a lie. All three are verbatim from
# the book and the page is not worth shipping without them.
for _n, _frag in ((1, "not busy"), (2, "more money"), (3, "one more outcome")):
    if _frag not in HTML.lower():
        raise SystemExit(
            "FAIL: toxic lie %d is not on the page. The old Wix page sold the "
            "outcomes and never named the lies -- that is the thing this "
            "rebuild fixes." % _n)
if HTML.count('class="t">Truth<') != 3:
    raise SystemExit("FAIL: every lie needs the truth the book sets against it")

# The value stack was removed on purpose. If one comes back it should come
# back as a decision, not as a paste.
for banned in ("Total Value", "Valued over", "&euro;300", "RRP", "was &euro;"):
    if banned in HTML:
        raise SystemExit(
            "FAIL: %r is back on the page. The struck value stack was removed "
            "deliberately -- see the note at the top of the preview." % banned)

# Typos that were on the Wix page for years. Cheap to check forever.
for typo in ("PARRALLAXX", "Parrallaxx", "Keep you Busy", "worlds most"):
    if typo in HTML:
        raise SystemExit("FAIL: %r is back in the markup" % typo)

# The annotation layer is a build-time thing and must never reach a browser.
for marker in ('class="note"', "noteBtn", 'class="ph"', "IMAGE_SLOT_", "[CLIENT]"):
    if marker in HTML:
        raise SystemExit("FAIL: %s is still in the markup" % marker)

bundle = """/* PARALLAXX TRANSFORMATIONS - Three Toxic Lies. Tag: %(tag)s.
   GENERATED by build_toxic_lies_bundle.py from toxic-lies-preview.html,
   which is the approved design. DO NOT EDIT THIS FILE, edit that one and rerun.

   Renders into the LIGHT DOM on purpose. The stylesheet is scoped to #ttl-page
   and the page script uses document.querySelector, so light DOM keeps the
   reveals working as approved. */
(function () {
  if (customElements.get('%(tag)s')) return;

  var CSS = `%(css)s`;
  var HTML = `%(html)s`;

  function once(id, make) {
    if (document.getElementById(id)) return;
    var el = make(); el.id = id; document.head.appendChild(el);
  }

  function addHead() {
    once('ttl-pre1', function () { var l = document.createElement('link'); l.rel = 'preconnect'; l.href = 'https://fonts.googleapis.com'; return l; });
    once('ttl-pre2', function () { var l = document.createElement('link'); l.rel = 'preconnect'; l.href = 'https://fonts.gstatic.com'; l.crossOrigin = ''; return l; });
%(fonts)s
    once('ttl-css', function () { var st = document.createElement('style'); st.textContent = CSS; return st; });
    if (!document.querySelector('meta[name="viewport"]')) {
      var mv = document.createElement('meta'); mv.name = 'viewport';
      mv.content = 'width=device-width, initial-scale=1'; document.head.appendChild(mv);
    }
  }

  function script(src, id) {
    return new Promise(function (res) {
      if (document.getElementById(id)) return res();
      var sc = document.createElement('script'); sc.id = id; sc.src = src; sc.async = false;
      sc.onload = res; sc.onerror = res; document.head.appendChild(sc);
    });
  }

  function boot() {
%(pagejs)s
  }

  var El = function () { return Reflect.construct(HTMLElement, [], El); };
  El.prototype = Object.create(HTMLElement.prototype);
  El.prototype.constructor = El;
  Object.setPrototypeOf(El, HTMLElement);

  El.prototype.connectedCallback = function () {
    if (this._ttlUp) return;
    this._ttlUp = true;
    addHead();
    this.innerHTML = HTML;
    script('/parallaxx-nav.js', 'ttl-nav-js');
    script('/parallaxx-footer.js', 'ttl-foot-js');
    try { boot(); } catch (e) { /* the page renders fully visible without it */ }
  };

  customElements.define('%(tag)s', El);
})();
""" % dict(
    tag=TAG,
    css=CSS,
    html=HTML,
    pagejs=PAGE_JS,
    fonts="\n".join(
        "    once('ttl-font%d', function () { var l = document.createElement('link'); l.rel = 'stylesheet'; l.href = '%s'; return l; });"
        % (i, u) for i, u in enumerate(font_links)),
)

OUT.write_text(bundle, encoding="utf-8")
print("wrote %s  %d bytes  css=%d html=%d js=%d fonts=%d"
      % (OUT.name, len(bundle), len(CSS), len(HTML), len(PAGE_JS), len(font_links)))

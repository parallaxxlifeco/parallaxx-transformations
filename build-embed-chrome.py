#!/usr/bin/env python3
"""
Put the current Parallaxx nav and footer on the two LIVE Wix HTML embeds.

    python3 build-embed-chrome.py

INPUT   src/reconnected-man-wix-inject.html      the page serving now
        src/reconnected-woman-wix-inject.html    the page serving now
        parallaxx-nav.js                         built from PtNav v3.dc.html
        parallaxx-footer.js                      built from PtFooter v3.dc.html

OUTPUT  reconnected-man-wix-inject.html
        reconnected-woman-wix-inject.html

The pages' own design and copy are untouched. The only changes are chrome: the
little fixed brand chip in the top-left comes out, the real nav and footer go
in, and the hero gets enough top padding to clear a fixed bar.

WHY THIS INLINES THE BUILT BUNDLES INSTEAD OF PORTING THE MARKUP
----------------------------------------------------------------
The first version of this script hand-ported PtNav.dc.html out of the design
folder. That was wrong twice over. The folder copy is stale, and the nav has
since been restructured around For Men / For Women, which is the whole
argument of the redesign. A hand port also drifts the moment the source moves.

So both custom elements are inlined byte for byte from the bundles this repo
already builds. Whatever PtNav v3 and PtFooter v3 say is what these pages get.
When the chrome changes, rebuild the bundles and rerun this. Nothing in here
needs editing by hand.

WHAT AN EMBED CANNOT FIX, AND WHY THIS IS A STOPGAP
---------------------------------------------------
Both pages ship as Wix HTML EMBEDS, so each renders inside a cross-origin
iframe with the site header and footer switched off by page code:

    $w.onReady(function () { $w('#header1').collapse(); $w('#footer1').collapse(); });

Three things follow that no amount of markup can undo:

  1. position:fixed inside an iframe pins to the IFRAME's viewport, not the
     browser window. It reads correctly because the embed is about window
     height, but it is not the same thing.
  2. Links inside an iframe load INSIDE the iframe. The shim below walks both
     shadow roots and sets target="_top" on every anchor so navigation escapes
     to the real page. Without it, clicking About loads the whole site inside
     the embed box.
  3. None of this is on the parent origin, so Google still attributes none of
     it to your URL.

The real fix is to stop collapsing the site header and footer and place
parallaxx-nav and parallaxx-footer as Wix Custom Elements, the way the
redesigned pages do. That is editor work. This gets the two live pages out of
being dead ends in the meantime.
"""
import re, pathlib, sys

HERE = pathlib.Path(__file__).parent
SRC  = HERE / "src"

NAV_BUNDLE    = HERE / "parallaxx-nav.js"
FOOTER_BUNDLE = HERE / "parallaxx-footer.js"

# LIVE FINGERPRINTS. Captured 6 Aug 2026 by fetching each page's embed
# straight off filesusr and hashing it, after a stale source shipped once.
#
# The build FAILS if a source does not match. That is the point: a source in
# src/ is only trustworthy if it is byte for byte what the site is serving, and
# there is no way to tell by looking. Re-capture with the recipe in
# LIVE-SOURCE-REFRESH.md whenever the live page is edited, and paste the new
# numbers here.
PAGES = [
    dict(src="reconnected-man-wix-inject.html",   root="trm-page", brand="trm-brand",
         active="men",   live_len=47675, live_hash=-283660525),
    dict(src="reconnected-woman-wix-inject.html", root="trw-page", brand="trw-brand",
         active="women", live_len=45668, live_hash=-178491467),
]


def jhash(s):
    """The 31-based rolling hash used to capture the live fingerprints, kept
    identical to the browser-side version so the numbers are comparable."""
    h = 0
    for ch in s:
        h = (h * 31 + ord(ch)) & 0xFFFFFFFF
        if h >= 2 ** 31:
            h -= 2 ** 32
    return h

# The nav is fixed, so the hero has to start below it. 16px padding either side
# of a 30px logo is a 62px bar; 118px gives it real clearance.
HERO_PAD = "118px 28px 72px"

SHIM = """
/* ── TARGET SHIM ──────────────────────────────────────────────────────────
   This page is a Wix HTML embed, so it lives in a cross-origin iframe. A link
   with no target loads INSIDE that iframe, which means clicking About would
   render the entire site inside the embed box. Both chrome elements keep
   their links in a shadow root, so this reaches in once each one upgrades and
   sets target="_top" on every anchor. The observer covers anything added
   later and costs nothing.

   If these pages ever stop being embeds, this whole block can go. */
(function () {
  function retarget(root) {
    if (!root) return;
    root.querySelectorAll('a[href]').forEach(function (a) {
      if (!a.target) a.target = '_top';
    });
  }
  function watch(tag) {
    customElements.whenDefined(tag).then(function () {
      var el = document.querySelector(tag);
      if (!el) return;
      var apply = function () { retarget(el.shadowRoot); };
      apply();
      if (el.shadowRoot && window.MutationObserver) {
        new MutationObserver(apply).observe(el.shadowRoot, {childList: true, subtree: true});
      }
      [60, 300, 1200].forEach(function (t) { setTimeout(apply, t); });
    });
  }
  watch('parallaxx-nav');
  watch('parallaxx-footer');
})();
"""

# The chrome lives in shadow roots, so the page's #trm-page / #trw-page rules
# cannot reach inside it. These two lines are only about how the HOSTS sit in
# the page: the pages centre their text and the footer host would inherit it.
HOST_CSS = """
parallaxx-nav{display:block;position:relative;z-index:200}
parallaxx-footer{display:block;position:relative;z-index:2;text-align:left}
"""


def read_bundle(p):
    if not p.exists():
        sys.exit(f"FAIL: missing {p.name}. Build the chrome bundles first "
                 f"(python3 build-chrome-bundles.py), then rerun this.")
    return p.read_text(encoding="utf-8")


def build(page, nav_js, footer_js):
    src = SRC / page["src"]
    if not src.exists():
        sys.exit(f"FAIL: missing {src}. Put the LIVE embed files in src/ first.")
    s = src.read_text(encoding="utf-8")
    before = len(s)
    root, brand = page["root"], page["brand"]

    # Refuse to build from a source that is not what the site is serving.
    if len(s) != page["live_len"] or jhash(s) != page["live_hash"]:
        sys.exit(
            f"FAIL: src/{page['src']} is not the live page.\n"
            f"       source {len(s):,} chars, hash {jhash(s)}\n"
            f"       live   {page['live_len']:,} chars, hash {page['live_hash']}\n"
            f"       Re-capture it (see LIVE-SOURCE-REFRESH.md) before building.\n"
            f"       Building on a stale source is how the wrong copy ships.")

    if f'id="{root}"' not in s:
        sys.exit(f"FAIL: no #{root} in {page['src']}. Wrong source file?")
    if "parallaxx-nav" in s:
        sys.exit(f"FAIL: {page['src']} already has the chrome. Build from a clean source.")

    # 1. The old fixed brand chip is exactly what the nav replaces.
    s, n = re.subn(rf'<a class="{brand}".*?</a>\s*', '', s, count=1, flags=re.S)
    if not n:
        sys.exit(f"FAIL: could not find .{brand} to remove in {page['src']}.")

    # 2. Nav first thing inside the page root, footer last thing in it.
    s = s.replace(f'<div id="{root}">',
                  f'<div id="{root}">\n<parallaxx-nav active="{page["active"]}"></parallaxx-nav>\n', 1)

    i = s.rfind('</section>')
    if i < 0:
        sys.exit(f"FAIL: no </section> in {page['src']}.")
    i += len('</section>')
    s = s[:i] + "\n<parallaxx-footer></parallaxx-footer>\n" + s[i:]

    # 3. Hero clears the fixed bar.
    s, n = re.subn(r'(#hero\s*\{[^}]*?padding:\s*)72px 28px', r'\g<1>' + HERO_PAD,
                   s, count=1, flags=re.S)
    if not n:
        print(f"  warn: hero padding unchanged in {page['src']}; check it clears the nav.")

    # 4. Host CSS after the page's own stylesheet.
    j = s.find('</style>')
    s = s[:j] + '</style>\n<style>' + HOST_CSS + '</style>' + s[j + len('</style>'):]

    # 5. Both bundles verbatim, then the shim.
    s = s.rstrip() + (
        "\n\n<!-- ══ PARALLAXX CHROME ══════════════════════════════════════════════\n"
        "     parallaxx-nav and parallaxx-footer, inlined byte for byte from the\n"
        "     built bundles. DO NOT EDIT THEM HERE. Edit PtNav v3.dc.html or\n"
        "     PtFooter v3.dc.html, run build-chrome-bundles.py, then rerun\n"
        "     build-embed-chrome.py. Anything changed by hand below is overwritten.\n"
        "     ═══════════════════════════════════════════════════════════════════ -->\n"
        "<script>\n" + nav_js + "\n</script>\n"
        "<script>\n" + footer_js + "\n</script>\n"
        "<script>" + SHIM + "</script>\n"
    )

    out = HERE / page["src"]
    out.write_text(s, encoding="utf-8")
    print(f'built {out.name}  ({len(s):,} bytes, was {before:,})  nav active="{page["active"]}"')


if __name__ == "__main__":
    nav_js    = read_bundle(NAV_BUNDLE)
    footer_js = read_bundle(FOOTER_BUNDLE)
    for p in PAGES:
        build(p, nav_js, footer_js)
    print("\nBoth live embeds now carry parallaxx-nav v3 and parallaxx-footer v3.")

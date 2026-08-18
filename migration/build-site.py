#!/usr/bin/env python3
"""
build-site.py — assemble the Cloudflare Pages site into dist/.

WHY THIS EXISTS
---------------
Until now every page in this repo was a Wix Custom Element: a .js bundle that
Wix loaded into a widget, with the <head> (title, description, canonical, OG)
supplied by Wix page settings. Moving off Wix means nobody supplies the <head>
any more. If we deployed the preview harnesses as-is, every page would ship the
title "… (preview)", no description, no canonical and no share image, and the
site would lose the SEO it currently has on all nine URLs.

So this script owns the <head> that Wix used to own. The metadata in ROUTES was
harvested verbatim from the live Wix pages before cancellation — it is not
rewritten copy, it is the existing SEO carried across intact.

WHAT IT DOES
------------
  1. Emits dist/<route>/index.html for every page: real <head>, then the
     custom-element tag and its bundle. Same rendering path as today.
  2. Copies the bundles and static assets across.
  3. Rewrites absolute https://www.parallaxxtransformations.com/... links to
     root-relative. Without this, every nav link on a vercel.app preview jumps
     back to the live Wix site and the deploy cannot be tested honestly.
  4. Localises Wix-hosted images and video IF wix-assets/ is present, so the
     site stops depending on a CDN we are about to stop paying for.
  5. Writes sitemap.xml and robots.txt.

Deployed by Cloudflare Pages with build command:
    python3 migration/build-site.py --local     (output directory: dist)

Run:  python3 build-site.py          (Wix asset URLs left intact — works today)
      python3 build-site.py --local  (rewrite to local assets; needs wix-assets/)
"""

import json
import re
import shutil
import sys
from pathlib import Path

# This script lives in migration/ but builds the repo that contains it. HERE is
# where the migration's own files sit (asset map, downloaded assets); REPO is
# where the page bundles live and where dist/ is written. Cloudflare Pages takes
# its config from _redirects and _headers inside the output directory, so there
# is nothing to write at the repository root.
HERE = Path(__file__).resolve().parent
REPO = HERE.parent
DIST = REPO / "dist"
ORIGIN = "https://www.parallaxxtransformations.com"

# The Reconnected Woman bundle pulls its nav and footer from GitHub Pages by
# absolute URL. Left alone, the new site would still be reaching across to
# github.io for its chrome on every load — a cross-origin dependency on a host
# we are supposedly migrating off, and one that goes stale the moment a bundle
# is rebuilt here but not pushed there. Made root-relative instead.
GH_PAGES = "https://parallaxxlifeco.github.io/parallaxx-transformations/"

# 'Lumios Marker' was never uploaded, so this @font-face has always pointed at
# the literal placeholder string and 404'd on seven pages. The font stack already
# falls through to Permanent Marker, so dropping the rule changes nothing on
# screen and removes a failed request per page. Fixed in the built copy only —
# the sources keep the TODO, so uploading the real .woff2 stays a one-line job.
FONTFACE_RE = re.compile(
    r"@font-face\s*\{[^}]*LUMIOS_MARKER_WOFF2_URL[^}]*\}", re.IGNORECASE
)

# ── ROUTES ──────────────────────────────────────────────────────────────
# path, custom element tag, bundle, and the <head> harvested from live Wix.
# `bg` matches the page's own background so there is no white flash before
# the bundle boots — the harnesses each set this and it must not be lost.
ROUTES = [
    dict(
        path="/",
        tag="parallaxx-home",
        bundle="parallaxx-home.js",
        bg="#061938",
        title="Personal Leadership Facilitator Daniel Lawson | Parallaxx Transformations",
        desc="Ask how you're doing and you say fine. Or busy. Same answer for years. "
             "Coaching for people who handle it all on their own.",
        og_title="Coaching for people who handle it all on their own.",
        og_desc="Ask how you're doing and you say fine. Or busy. Same answer for years.",
        og_img="img/og-home.jpg",
    ),
    dict(
        path="/men",
        tag="parallaxx-home-men",
        bundle="parallaxx-home-men.js",
        bg="#04122A",
        title="Coaching for Married Men Who Feel Distant | Parallaxx",
        desc="You handle everything at home and still feel unreachable. Coaching for men in "
             "long term relationships who stopped asking for anything. Find the pattern you are running.",
        og_title="You handled it all yourself. That's the distance.",
        og_desc="A husband who sorts everything. And a man she never feels. "
                "Find which of the five patterns you are running.",
        og_img="img/og-men.jpg",
    ),
    dict(
        path="/women",
        tag="parallaxx-home-women",
        bundle="parallaxx-home-women.js",
        bg="#04122A",
        title="Coaching for Professional Women | Parallaxx Transformations",
        desc="You've hit every target and you're still behind. Take the Priority Audit. "
             "Ninety seconds to find out your most important focus — your answer is on the screen.",
        og_title="You've hit every target. And you still feel behind.",
        og_desc="What is your most important focus? Priority Audit for an ordinary week. "
                "Ninety seconds, the answer's on the screen, and nothing lands in your inbox.",
        og_img="img/og-women.jpg",
    ),
    dict(
        path="/the-reconnected-man",
        tag="parallaxx-reconnected-man",
        bundle="parallaxx-reconnected-man.js",
        bg="#04122A",
        title="RECONNECTED MAN | Parallaxx Transformations",
        desc="A brotherhood for men done living in disconnection and loneliness. Join The "
             "Reconnected Man — weekly group containers, live coaching, and real connection. "
             "Facilitated by Daniel Lawson. €59/month.",
        og_title="RECONNECTED MAN | Parallaxx Transformations",
        og_desc="For men done living in disconnection and loneliness. Real connection, deep love, "
                "true intimacy — not just with women, but in every relationship that defines you.",
        og_img="img/og-reconnected-man.png",
    ),
    dict(
        path="/the-reconnected-woman",
        tag="parallaxx-reconnected-woman",
        bundle="parallaxx-reconnected-woman.js",
        bg="#04122A",
        title="RECONNECTED WOMAN | Parallaxx Transformations",
        desc="For women done abandoning themselves to keep it all together. An Inner Circle for "
             "high-achieving women coming back into integrity. By application only.",
        og_title="RECONNECTED WOMAN | Parallaxx Transformations",
        og_desc="For women done abandoning themselves to keep it all together. An Inner Circle for "
                "high-achieving women coming back into integrity. By application only.",
        og_img="img/og-reconnected-woman.png",
    ),
    dict(
        path="/priority-audit",
        tag="parallaxx-priority-audit",
        bundle="parallaxx-priority-audit.js",
        bg="#04122A",
        title="Free Priority Audit | Parallaxx Transformations",
        desc="Fifteen statements, ninety seconds. Find the one thing feeding everything else "
             "in an ordinary week. Nothing lands in your inbox.",
        og_title="Free Priority Audit | Parallaxx Transformations",
        og_desc="Fifteen statements, ninety seconds. The answer is on the screen.",
        og_img="img/og-priority-audit.jpg",
    ),
    dict(
        path="/about-daniel-lawson",
        tag="parallaxx-about-page",
        bundle="parallaxx-about-page.js",
        bg="#04122A",
        title="Daniel Lawson | Personal Leadership Facilitator | Parallaxx",
        desc="Discover Daniel Lawson, Personal Leadership expert, guiding clients to purpose-driven "
             "impact and inner peace through transformative retreats and coaching.",
        og_title="About Daniel Lawson | Parallaxx Transformations",
        og_desc="Daniel Lawson, an authority in Personal Leadership and retreat facilitation, empowers "
                "attendees to achieve purposeful impact and inner peace. Explore his journey and discover "
                "how he helps individuals lead themselves to fulfilling and meaningful lives.",
        og_img="img/og-about.png",
    ),
    dict(
        path="/testimonials-daniel-lawson",
        tag="parallaxx-testimonials",
        bundle="parallaxx-testimonials.js",
        bg="#04122A",
        title="Reconnect You Testimonials | Client Stories | Daniel Lawson",
        desc="Written and filmed stories from Reconnect You clients across Europe, the US and "
             "Australia. Every word is theirs.",
        og_title="They all tried to do it on their own first.",
        og_desc="Written and filmed stories from Reconnect clients across Europe, the US and "
                "Australia. Every word is theirs.",
        og_img="img/og-testimonials-page.jpg",
    ),
    dict(
        path="/the-archetype-quiz",
        tag="parallaxx-quiz",
        bundle="parallaxx-quiz.js",
        bg="#04122A",
        title="The Protection Archetype Quiz | Parallaxx Transformations",
        desc="Five patterns. Find which one you are running, and what it is costing the people "
             "closest to you.",
        og_title="Which of the five patterns are you running?",
        og_desc="The Protection Archetype Quiz. A few minutes, and the answer is on the screen.",
        og_img="og-quiz.jpg",
    ),
    dict(
        path="/wheel-of-reconnect",
        tag="parallaxx-wheel-of-reconnect",
        bundle="parallaxx-wheel-of-reconnect.js",
        bg="#04122A",
        title="The Wheel of Reconnect | Parallaxx Transformations",
        desc="An interactive look at the areas of life that hold each other up — and the one "
             "that is carrying the rest.",
        og_title="The Wheel of Reconnect",
        og_desc="The areas of life that hold each other up, and the one carrying the rest.",
        og_img="img/og-home.jpg",
        noindex=False,
    ),
]

# ── LEGACY URL REDIRECTS ────────────────────────────────────────────────
# Every URL in the live Wix sitemap that has no home on the new site. Left to
# 404, these lose their Google rankings and break every old link in show notes,
# emails and social posts. A 301 keeps the link equity and the visitor.
REDIRECTS = {
    "/home": "/",
    "/about-daniel": "/about-daniel-lawson",
    "/what-is-your-archetype": "/the-archetype-quiz",
    "/archetype-quiz-form-follow": "/the-archetype-quiz",
    "/assesment-page": "/the-archetype-quiz",
    "/your-identity-challenge": "/the-archetype-quiz",
    "/vault": "https://vault.parallaxxtransformations.com",
    # Offers and funnels that no longer have a page of their own.
    "/reconnect": "/",
    "/programs": "/",
    "/coaching-experiences": "/",
    "/digital-coaching-products": "/",
    "/limitless-potential": "/",
    "/application-form-limitless-potential": "/",
    "/elite-life-challenge": "/",
    "/copy-of-elite-life-challenge": "/",
    "/i-want-intimacy-and-challenge": "/",
    "/morning-mastery-club": "/",
    "/peakperformance-community": "/",
    "/reconnect-facebook-community": "/",
    "/members": "/",
    "/free-guide": "/",
    "/free-gift-tmg": "/",
    "/free-ebook-three-toxic-lies": "/",
    "/three-toxic-lies": "/",
    "/personal-leadership-resources": "/",
    # Content pages.
    "/blog": "/",
    "/ptjournal": "/",
    "/parallaxx-perspectives-podcast": "/",
    "/reconnect-you-podcast-with-daniel-lawson": "/",
    "/daniel-lawson-as-seen-in": "/",
    "/daniel-lawson-speaking": "/",
    "/facilitating": "/",
    # Contact and booking. TODO: these want real pages. 'Parallaxx Contact.dc.html'
    # is already authored in this repo and is a short build away; until then the
    # nav's Contact item lands on the home page.
    "/contact-daniel-lawson": "/",
    "/contact-form-start-today": "/",
    "/book-a-call-with-daniel-lawson": "/",
    # Legal. Also want real pages before any ad platform audits the site.
    "/privacy-policy": "/",
    "/terms-of-use": "/",
    # Thank-you pages, which only ever had meaning mid-funnel.
    "/thankyou": "/",
    "/giveitallthankyou": "/",
    "/speaker-thankyou": "/",
    "/appreciation": "/",
}

# The 15 Wix blog posts, all under /post/. Handled with one wildcard rather
# than fifteen entries.
WILDCARD_REDIRECTS = [{"source": "/post/:slug*", "destination": "/", "permanent": True}]

STATIC_FILES = [
    "support.js",
    "og-home-men.jpg",
    "og-priority-audit.jpg",
    "og-quiz.jpg",
]
STATIC_DIRS = ["covers"]


def head_html(r: dict) -> str:
    canonical = ORIGIN + ("" if r["path"] == "/" else r["path"])
    # Resolve the share image against what actually shipped. Localised assets
    # land under /assets/, but a few OG images are repo-root files copied to the
    # root of dist — so a single hardcoded prefix gets one of the two wrong.
    # Getting it wrong is invisible on the site and only shows up as a blank
    # thumbnail when someone shares the link, which is the worst place to find
    # out. Warn loudly rather than emit a URL that 404s.
    og_img = r["og_img"]
    if og_img.startswith("http"):
        og_abs = og_img
    elif (DIST / "assets" / og_img).exists():
        og_abs = f"{ORIGIN}/assets/{og_img}"
    elif (DIST / og_img).exists():
        og_abs = f"{ORIGIN}/{og_img}"
    else:
        og_abs = f"{ORIGIN}/{og_img}"
        print(f"WARNING: og:image for {r['path']} not found in dist — {og_img}")
    robots = "noindex,nofollow" if r.get("noindex") else "index,follow,max-image-preview:large"
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{r['title']}</title>
<meta name="description" content="{r['desc']}">
<link rel="canonical" href="{canonical}">
<meta name="robots" content="{robots}">

<meta property="og:type" content="website">
<meta property="og:site_name" content="Parallaxx Transformations">
<meta property="og:url" content="{canonical}">
<meta property="og:title" content="{r['og_title']}">
<meta property="og:description" content="{r['og_desc']}">
<meta property="og:image" content="{og_abs}">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">

<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{r['og_title']}">
<meta name="twitter:description" content="{r['og_desc']}">
<meta name="twitter:image" content="{og_abs}">

<link rel="icon" href="/favicon.png">
<link rel="apple-touch-icon" href="/favicon.png">
<meta name="theme-color" content="{r['bg']}">

<style>html,body{{margin:0;padding:0;background:{r['bg']}}} {r['tag']}{{display:block}}</style>
</head>
<body>
<{r['tag']}></{r['tag']}>
<script src="/{r['bundle']}"></script>
</body>
</html>
"""


def detach(text: str) -> tuple:
    """Cut every tie to the hosts we are leaving: Wix for the domain, GitHub
    Pages for the chrome. Returns the text plus the counts, so the build says
    out loud how many ties it cut rather than claiming success silently."""
    n_wix = text.count(ORIGIN)
    text = text.replace(ORIGIN + "/", "/").replace(ORIGIN, "/")
    n_gh = text.count(GH_PAGES)
    text = text.replace(GH_PAGES, "/")
    text, n_font = FONTFACE_RE.subn("", text)
    return text, n_wix, n_gh, n_font


def localise(text: str, asset_map: list) -> tuple:
    """Point Wix CDN URLs at our own copies. Longest URL first, so a transform
    variant is never clipped by the bare media URL that is its own prefix."""
    hits = 0
    for row in sorted(asset_map, key=lambda r: -len(r["url"])):
        if row["url"] in text:
            hits += text.count(row["url"])
            text = text.replace(row["url"], "/assets/" + row["file"])
    return text, hits


def main() -> int:
    local = "--local" in sys.argv

    if DIST.exists():
        shutil.rmtree(DIST)
    DIST.mkdir()

    asset_map = []
    if local:
        mp = HERE / "asset-map.json"
        src = HERE / "wix-assets"
        if not mp.exists():
            print("ERROR: --local needs asset-map.json beside this script, in migration/.")
            return 1
        if not src.exists():
            print("ERROR: --local needs migration/wix-assets/ — run download-wix-assets.sh first.")
            return 1
        asset_map = json.loads(mp.read_text())
        # Note: r["url"] is what the bundles reference and r.get("src") is where
        # the bytes came from. Only "url" is ever matched against bundle text —
        # rewriting that to a different resolution silently un-links four videos.
        missing = [r["file"] for r in asset_map if not (src / r["file"]).exists()]
        if missing:
            print(f"ERROR: {len(missing)} assets missing from wix-assets/, first few:")
            for m in missing[:8]:
                print("  " + m)
            print("Re-run download-wix-assets.sh — it skips what it already has.")
            return 1
        shutil.copytree(src, DIST / "assets")
        print(f"assets   copied {len(asset_map)} files into dist/assets/")

    # Bundles: cut the host ties, optionally localise assets.
    total_links = total_gh = total_font = total_assets = 0
    bundles = [r["bundle"] for r in ROUTES] + ["parallaxx-nav.js", "parallaxx-footer.js"]
    for name in dict.fromkeys(bundles):
        b = REPO / name
        if not b.exists():
            if name in ("parallaxx-nav.js", "parallaxx-footer.js"):
                continue
            print(f"ERROR: missing bundle {name}")
            return 1
        text, n_wix, n_gh, n_font = detach(b.read_text(encoding="utf-8"))
        total_links += n_wix
        total_gh += n_gh
        total_font += n_font
        if local:
            text, n = localise(text, asset_map)
            total_assets += n
        (DIST / name).write_text(text, encoding="utf-8")

    for f in STATIC_FILES:
        if (REPO / f).exists():
            shutil.copy2(REPO / f, DIST / f)
    for d in STATIC_DIRS:
        if (REPO / d).is_dir():
            shutil.copytree(REPO / d, DIST / d)

    # Every page's <head> asks for /favicon.png, so it has to be produced rather
    # than assumed. Resolved from the asset map rather than a hardcoded filename:
    # the name is derived from the Wix media ID, and guessing it wrong fails
    # silently — the build succeeds and every browser tab shows a blank icon.
    # Prefer an uncropped logo, then the largest: the asset set contains a
    # stray 8KB crop that sorts first alphabetically and makes an unusable icon.
    cands = [
        DIST / "assets" / row["file"]
        for row in asset_map
        if "logo" in row["file"].lower() and (DIST / "assets" / row["file"]).exists()
    ]
    cands.sort(key=lambda p: ("crop" in p.name.lower(), -p.stat().st_size))
    logo = cands[0] if cands else None
    if logo:
        shutil.copy2(logo, DIST / "favicon.png")
        print(f"favicon  from {logo.name}")
    elif local:
        print("WARNING: no logo in the asset map — /favicon.png will 404")

    # Pages.
    for r in ROUTES:
        out = DIST / "index.html" if r["path"] == "/" else DIST / r["path"].strip("/") / "index.html"
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(head_html(r), encoding="utf-8")

    # sitemap + robots.
    urls = "\n".join(
        f"  <url><loc>{ORIGIN}{'' if r['path'] == '/' else r['path']}</loc>"
        f"<changefreq>weekly</changefreq></url>"
        for r in ROUTES if not r.get("noindex")
    )
    (DIST / "sitemap.xml").write_text(
        f'<?xml version="1.0" encoding="UTF-8"?>\n'
        f'<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{urls}\n</urlset>\n',
        encoding="utf-8",
    )
    (DIST / "robots.txt").write_text(
        f"User-agent: *\nAllow: /\n\nSitemap: {ORIGIN}/sitemap.xml\n", encoding="utf-8"
    )

    # Cloudflare Pages configures redirects and headers with two plain-text files
    # inside the output directory, not a JSON file at the repo root. Pages serves
    # /about from /about/index.html on its own, so no cleanUrls equivalent is
    # needed. Order matters in _redirects: the first match wins, so the /post/*
    # wildcard goes last or it would swallow nothing but is safer at the end.
    lines = [
        "# Legacy Wix URLs. 301 so Google moves the ranking rather than dropping it,",
        "# and so old links in show notes, emails and social posts still land.",
        "# Generated by migration/build-site.py — edit REDIRECTS there, not here.",
        "",
    ]
    width = max(len(s) for s in REDIRECTS) + 2
    for src, dest in REDIRECTS.items():
        lines.append(f"{src.ljust(width)}{dest}  301")
    lines += ["", "# The 15 Wix blog posts, caught by one splat rather than fifteen rules.",
              "/post/*".ljust(width) + "/  301"]
    (DIST / "_redirects").write_text("\n".join(lines) + "\n", encoding="utf-8")

    (DIST / "_headers").write_text(
        "# Generated by migration/build-site.py\n\n"
        "/*\n"
        "  X-Content-Type-Options: nosniff\n"
        "  Referrer-Policy: strict-origin-when-cross-origin\n"
        "  X-Frame-Options: SAMEORIGIN\n"
        "\n"
        "# Asset filenames carry a Wix media hash, so they are safe to cache forever.\n"
        "/assets/*\n"
        "  Cache-Control: public, max-age=31536000, immutable\n"
        "\n"
        "# Bundles keep their names across deploys, so they must revalidate or a\n"
        "# push would not reach anyone still holding a cached copy.\n"
        "/*.js\n"
        "  Cache-Control: public, max-age=3600, must-revalidate\n",
        encoding="utf-8",
    )
    redirects = list(REDIRECTS) + ["/post/*"]

    # vercel.json is no longer used. Left behind it would be dead config that
    # reads as live, so it goes.
    stale = REPO / "vercel.json"
    if stale.exists():
        stale.unlink()
        print("removed  vercel.json (superseded by dist/_redirects and dist/_headers)")

    print(f"pages    {len(ROUTES)} written")
    print(f"links    {total_links} absolute Wix-domain links made root-relative")
    print(f"ghpages  {total_gh} GitHub Pages references cut")
    print(f"fonts    {total_font} broken Lumios @font-face rules removed")
    if local:
        print(f"assets   {total_assets} Wix CDN references repointed at /assets/")
    else:
        print("assets   left on the Wix CDN (run with --local once wix-assets/ exists)")
    print(f"redirect {len(redirects)} rules written to dist/_redirects")
    print(f"output   {DIST}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

"""
Articles: markdown in, static HTML out.

Added 16 Sep 2026. Imported and called by build-site.py, which is the only
script Cloudflare Pages runs — so everything here is inside the deploy path,
including the confidentiality guard. A guard outside the deploy path is
documentation, not a guard.

WHY THIS IS NOT A .dc.html BUNDLE
---------------------------------
Every other route on this site is a hand-designed visual document: a .dc.html
compiled by a build-*-bundle.py into a ~100KB custom-element bundle, with the
copy lifted back out at build time so crawlers can read it. That is the right
shape for a page whose layout IS the message.

An article is text. Routing it through that pipeline would ship 100KB of
JavaScript to render three thousand words, and put the body behind a script
again — the exact problem the 14 Sep pre-render work existed to fix. Articles
are therefore plain static HTML with inline CSS. They are the fastest and most
crawlable pages on the site, and they need no bundle at all.

WHY THE MARKDOWN RENDERER IS HAND-WRITTEN
-----------------------------------------
`python-markdown` is installed on Daniel's Mac. Whether it is installed in the
Cloudflare Pages build image is not something this repo controls, and finding
out by way of a failed deploy is the wrong way to find out. So this renders a
deliberately small subset with no dependencies at all, and RAISES on anything
it does not understand rather than silently mangling it. If a writer needs a
construct that is not here, add it here — do not work around it in the content.

Supported: ## and ### headings, paragraphs, - bullets, 1. numbered lists,
> blockquotes, | tables |, **bold**, *italic*, [links](url), --- rules.
"""

import html
import re
from datetime import date
from pathlib import Path

# ── THE CONFIDENTIALITY GUARD ──────────────────────────────────────────
# The rooms are recorded "internal use only, confidential". The precedent is
# commit 4879c42: nothing said in a room goes public without the person who
# said it agreeing. AND THIS REPO IS PUBLIC — anything committed is visible
# forever, in history, even if deleted later.
#
# Articles draw on patterns observed across several people. They never carry
# one person's identifiable arc: stripping a name off one person's story does
# not make it not their story. They will recognise it, and so will their spouse.
#
# These patterns fail the build. They are deliberately blunt and will sometimes
# catch an innocent sentence — rewrite the sentence. A guard that is argued
# with is a guard that stops working.
# Each entry is (pattern, why, flags). Most are case-insensitive. Two are NOT,
# and that is the point of carrying flags per pattern rather than passing re.I
# to all of them:
#
#   - The location rule keys off a CAPITALISED place name. Compiled with re.I,
#     its `[A-Z]` matches any letter, so "a man in the group" fires as though it
#     said "a man in Melbourne". That happened on the first article written
#     through this guard. A rule that fires on ordinary sentences gets worked
#     around rather than obeyed, which is worse than not having it.
#   - Job titles are capitalised in real life. Case-insensitively, "Head of"
#     catches "head of steam" and "head of the queue".
#
# The rest stay blunt on purpose and will sometimes catch an innocent sentence.
# Rewrite the sentence.
CONFIDENTIALITY_PATTERNS = [
    (r"\b(?:aged?|he'?s|she'?s|he is|she is)\s+(?:2[0-9]|[3-7][0-9])\b",
     "an age attached to a person", re.I),
    (r"\b(?:2[0-9]|[3-7][0-9])[- ]year[- ]old\b", "an age attached to a person", re.I),
    (r"(?i:\b(?:a|one|this)\s+(?:client|man|woman|member|participant)\s+(?:in|from)\s+)[A-Z]",
     "a person placed in a named location", 0),
    (r"\b(?:his|her|their)\s+(?:wife|husband|partner)\s+(?:of|works|is a)\b",
     "an identifying detail about a named person's spouse", re.I),
    (r"\b(?:CFO|CTO|CEO|COO|VP of|Head of|Director of|Partner at)\b",
     "a job title specific enough to identify someone", 0),
    (r"\b(?:two|three|four|2|3|4)\s+(?:kids|children|daughters|sons)\b",
     "a child count", re.I),
]

# Verbatim quotes are permitted only from material already cleared for public
# use: the three Reconnected Man testimonials and the 16 blockquotes already
# live across the five main bundles. Anything else in a blockquote must be
# Daniel's own words. A quote in an article must carry an attribution line so
# this is checkable by eye; an unattributed blockquote fails.
QUOTE_ATTRIB_RE = re.compile(r"^>\s*—\s*\S", re.M)


def guard(text: str, where: str) -> list:
    """Every reason this file must not ship. Empty list means it may."""
    problems = []
    for pattern, why, flags in CONFIDENTIALITY_PATTERNS:
        for m in re.finditer(pattern, text, flags):
            problems.append(f"{where}: {why} — {m.group(0)!r}")

    # A blockquote run must end with an attribution line.
    lines = text.split("\n")
    run = []
    for line in lines + [""]:
        if line.startswith(">"):
            run.append(line)
            continue
        if run:
            if not QUOTE_ATTRIB_RE.search("\n".join(run)):
                problems.append(
                    f"{where}: a blockquote with no '> — attribution' line. "
                    f"Quotes are cleared material or Daniel's own words, and "
                    f"either way they say whose they are.")
            run = []
    return problems


# ── FRONT MATTER ───────────────────────────────────────────────────────
# Flat `key: value` only. No nested YAML, no lists-of-dicts, because this
# parser is twelve lines and a real YAML parser is another dependency this
# repo does not need. The FAQ is derived from the body instead (see below),
# which also means the on-page questions and the FAQPage schema cannot drift
# apart — they are the same text.
SOURCE_ID = re.compile(r"(?:RM-S[1-6]|RW-W[1-4]|PM-\d{2}|PW-\d{2}|DL)-\d{3}")

REQUIRED_KEYS = ("title", "pillar", "intent", "question", "answer", "description",
                 "published", "updated", "sources", "offer")


def parse_front_matter(raw: str, where: str) -> tuple:
    if not raw.startswith("---\n"):
        raise ValueError(f"{where}: no front matter — the file must open with ---")
    _, fm, body = raw.split("---\n", 2)
    meta = {}
    for line in fm.strip().split("\n"):
        if not line.strip():
            continue
        if ":" not in line:
            raise ValueError(f"{where}: front matter line is not key: value — {line!r}")
        k, v = line.split(":", 1)
        meta[k.strip()] = v.strip()
    missing = [k for k in REQUIRED_KEYS if k not in meta or not meta[k]]
    if missing:
        raise ValueError(f"{where}: front matter missing {', '.join(missing)}")

    # `sources` is the whole point of the engine. An article with no source id
    # is an article invented out of nothing, which is the thing this pipeline
    # exists NOT to publish at scale.
    meta["sources"] = [s.strip() for s in meta["sources"].split(",") if s.strip()]
    if not meta["sources"]:
        raise ValueError(f"{where}: sources is empty. Every article cites at "
                         f"least one id from the corpus index.")

    # THIS REPO IS PUBLIC AND `sources` IS COMMITTED IN PLAIN TEXT.
    # The corpus originally keyed participant profiles by first name — PM-SHRI,
    # PW-JULIA — and two of those ids reached article front matter before anyone
    # noticed. The rendered page never shows `sources`, but the .md does, on
    # GitHub, to anyone. The corpus prefixes are opaque now (PM-06, PW-04) and
    # the only mapping lives in the private corpus folder. This keeps it that
    # way: an id shape that is not on the list fails the build.
    for sid in meta["sources"]:
        if not SOURCE_ID.fullmatch(sid):
            raise ValueError(
                f"{where}: source id {sid!r} is not a recognised shape. Valid: "
                f"RM-S1..S6-nnn, RW-W1..W4-nnn, PM-nn-nnn, PW-nn-nnn, DL-nnn. "
                f"If that is a name-keyed id, it must NOT be committed — this "
                f"repo is public. Look it up in corpus-index/people-map.json "
                f"and cite the opaque id instead.")

    # The lede is what an answer engine extracts. The studies converge on the
    # first 50-80 words carrying disproportionate weight, so this is a hard
    # limit rather than a style note.
    words = len(meta["answer"].split())
    if not 25 <= words <= 80:
        raise ValueError(f"{where}: `answer` is {words} words. It is the first "
                         f"thing a model reads and the thing it quotes — keep "
                         f"it between 25 and 80, and make it a complete answer "
                         f"on its own.")
    if len(meta["description"]) > 158:
        raise ValueError(f"{where}: description is {len(meta['description'])} "
                         f"chars; Google truncates past ~158.")
    return meta, body


# ── THE MARKDOWN SUBSET ────────────────────────────────────────────────
INLINE = [
    (re.compile(r"\[([^\]]+)\]\(([^)]+)\)"), r'<a href="\2">\1</a>'),
    (re.compile(r"\*\*([^*]+)\*\*"), r"<strong>\1</strong>"),
    (re.compile(r"(?<!\*)\*([^*]+)\*(?!\*)"), r"<em>\1</em>"),
]


def inline(text: str) -> str:
    out = html.escape(text, quote=False)
    for pattern, repl in INLINE:
        out = pattern.sub(repl, out)
    return out


def slugify(text: str) -> str:
    s = re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")
    return s[:80]


def render_body(body: str, where: str) -> tuple:
    """Returns (html, faq) where faq is [(question, answer_text), ...]."""
    out, faq = [], []
    lines = body.split("\n")
    i = 0
    in_faq = False
    pending_q = None

    def close_para(buf):
        if buf:
            out.append(f"<p>{inline(' '.join(buf))}</p>")
            buf.clear()

    para = []
    while i < len(lines):
        line = lines[i].rstrip()

        if not line.strip():
            close_para(para)
            i += 1
            continue

        if line.startswith("## "):
            close_para(para)
            heading = line[3:].strip()
            in_faq = heading.lower() in ("common questions", "questions people ask")
            out.append(f'<h2 id="{slugify(heading)}">{inline(heading)}</h2>')
            i += 1
            continue

        if line.startswith("### "):
            close_para(para)
            heading = line[4:].strip()
            out.append(f'<h3 id="{slugify(heading)}">{inline(heading)}</h3>')
            # Inside the FAQ section an H3 is a question and the paragraph that
            # follows is its answer. That is the whole FAQPage schema — no
            # second copy of the text to fall out of sync with the page.
            pending_q = heading if in_faq else None
            i += 1
            continue

        if line.startswith(">"):
            close_para(para)
            quote, attrib = [], None
            while i < len(lines) and lines[i].startswith(">"):
                t = lines[i].lstrip(">").strip()
                if t.startswith("—"):
                    attrib = t.lstrip("—").strip()
                elif t:
                    quote.append(t)
                i += 1
            cite = f"<cite>{inline(attrib)}</cite>" if attrib else ""
            out.append(f"<blockquote><p>{inline(' '.join(quote))}</p>{cite}</blockquote>")
            continue

        if line.startswith("|"):
            close_para(para)
            rows = []
            while i < len(lines) and lines[i].startswith("|"):
                cells = [c.strip() for c in lines[i].strip().strip("|").split("|")]
                if not all(re.fullmatch(r":?-{2,}:?", c) for c in cells):
                    rows.append(cells)
                i += 1
            if rows:
                head = "".join(f"<th>{inline(c)}</th>" for c in rows[0])
                body_rows = "".join(
                    "<tr>" + "".join(f"<td>{inline(c)}</td>" for c in r) + "</tr>"
                    for r in rows[1:])
                out.append(f"<table><thead><tr>{head}</tr></thead>"
                           f"<tbody>{body_rows}</tbody></table>")
            continue

        m_ul = re.match(r"^[-*]\s+(.*)", line)
        m_ol = re.match(r"^\d+\.\s+(.*)", line)
        if m_ul or m_ol:
            close_para(para)
            tag = "ul" if m_ul else "ol"
            items = []
            while i < len(lines):
                mm = (re.match(r"^[-*]\s+(.*)", lines[i]) if tag == "ul"
                      else re.match(r"^\d+\.\s+(.*)", lines[i]))
                if not mm:
                    break
                items.append(f"<li>{inline(mm.group(1))}</li>")
                i += 1
            out.append(f"<{tag}>{''.join(items)}</{tag}>")
            continue

        if line.startswith("---"):
            close_para(para)
            i += 1
            continue

        if line[0] in "#`<=+~":
            raise ValueError(
                f"{where}: line {i + 1} starts with {line[0]!r}, which this "
                f"renderer does not support: {line[:60]!r}. Add it to "
                f"migration/articles.py rather than working around it.")

        para.append(line.strip())
        if pending_q:
            faq.append((pending_q, line.strip()))
            pending_q = None
        i += 1

    close_para(para)
    return "\n".join(out), faq


# ── PILLARS ────────────────────────────────────────────────────────────
# Four clusters, matching the two doors and the two mechanics underneath them.
# Every article belongs to exactly one and links up to its hub. The hub copy
# here is a placeholder headline only — the hub BODY is hand-written by Daniel
# in content/insights/<pillar>/_hub.md, because the four hubs are the anchor
# pages and should be the best writing on the site, not generated.
PILLARS = {
    # Decided 16 Sep 2026 by reading all 153 question rows in the corpus index
    # against what people actually search. The rationale, and what was killed
    # and why, is in the index's POSITIONING.md. Four provisional pillars died:
    # "self-trust" and "asking for what you want" are internal language (the
    # second is the method, so it is the answer nearly every article lands on,
    # not a bucket); "the distant husband" is a crowded lane searched by HER,
    # not him; "the insecure overachiever" maps to "high-functioning burnout",
    # which is saturated and is not her word anyway -- she says trade-off.
    #
    # All five carry both doors. Hub copy uses plain "you" and the articles
    # beneath each commit to one door, because a man and a woman described in
    # one breath reads as couples work and loses both buyers.
    #
    # Internal language is kept OUT of pillar names, slugs, h1s, titles and
    # descriptions -- those have to match what a person types -- and is welcome
    # IN the body, where a coined concept is what makes a piece memorable rather
    # than interchangeable. Found in their words, remembered in his.
    "knowing-and-not-doing": dict(
        name="Knowing your pattern and still running it",
        blurb="You can describe the thing you do. You do it anyway.",
        offer="/the-archetype-quiz",
    ),
    "being-the-capable-one": dict(
        name="Being the one who can handle it",
        blurb="It never looks like self-abandonment. It looks like being good at life.",
        offer="/women",
    ),
    "not-knowing-what-you-want": dict(
        name="Not knowing what you want",
        blurb="Somebody asks what you want and you come up empty.",
        offer="/priority-audit",
    ),
    "getting-what-you-wanted": dict(
        name="Getting what you wanted and feeling nothing",
        blurb="You hit the thing you spent years on, and the view stays the same.",
        offer="/men",
    ),
    "what-the-work-costs": dict(
        name="What the work costs",
        blurb="The part nobody selling this will tell you about.",
        offer="/women",
    ),
}

# An article's `offer` may name one destination or two, comma-separated. Two is
# the door-neutral close: both rooms named, neither characterised. Naming them
# is safe; *describing* a man and a woman in the same breath is the thing that
# makes a piece read as couples work, and a bare pair of links does not.
OFFER_LABELS = {
    "/the-reconnected-man": "The Reconnected Man",
    "/the-reconnected-woman": "The Reconnected Woman",
    "/men": "Coaching for men",
    "/women": "Coaching for women",
    "/priority-audit": "Take the Priority Audit",
    "/the-archetype-quiz": "Take the archetype quiz",
}

BG = "#04122A"
CSS = """
:root{--ink:#F1ECE1;--dim:#B1BFD7;--mute:#7C89A3;--gold:#E8C65F;--bg:#04122A;--deep:#061938}
*{box-sizing:border-box}
html,body{margin:0;padding:0;background:var(--bg);color:var(--ink)}
body{font:400 17px/1.7 system-ui,-apple-system,"Segoe UI",sans-serif;
 -webkit-font-smoothing:antialiased}
/* 42rem puts a 17px line at ~66 characters. It was 46rem, which measured
   73 — readable, but at the top of the comfortable band rather than in it.
   The 7rem top clears the fixed nav, which is 76px tall. */
.wrap{max-width:42rem;margin:0 auto;padding:7rem 1.25rem 6rem}
h1,h2,h3{font-family:'Montserrat',system-ui,sans-serif;line-height:1.25;
 letter-spacing:-.01em;margin:0}
h1{font-size:clamp(1.9rem,5vw,2.75rem);font-weight:700;margin-bottom:1.25rem}
/* Cream, not gold. Saturated yellow at heading size vibrates against navy
   even though the contrast ratio is fine (~11:1, AAA). Gold is kept for the
   small accents: the lede rule, the quote rule, table headers, links. */
h2{font-size:1.45rem;font-weight:600;margin:3rem 0 .85rem;color:var(--ink)}
h3{font-size:1.12rem;font-weight:600;margin:2rem 0 .6rem}
p{margin:0 0 1.15rem}
a{color:var(--gold);text-underline-offset:.18em}
.meta{font-size:.82rem;color:var(--mute);letter-spacing:.06em;
 text-transform:uppercase;margin-bottom:1.5rem}
.lede{font-size:1.2rem;line-height:1.6;color:var(--ink);border-left:3px solid var(--gold);
 padding:.1rem 0 .1rem 1.15rem;margin:0 0 2.5rem}
ul,ol{margin:0 0 1.15rem;padding-left:1.3rem}li{margin-bottom:.45rem}
blockquote{margin:2rem 0;padding:1.1rem 1.3rem;background:rgba(232,198,95,.06);
 border-left:3px solid rgba(232,198,95,.45)}
blockquote p{margin:0 0 .5rem;font-style:italic;color:var(--ink)}
blockquote cite{font-style:normal;font-size:.85rem;color:var(--mute)}
table{width:100%;border-collapse:collapse;margin:1.75rem 0;font-size:.94rem}
th,td{text-align:left;padding:.65rem .7rem;border-bottom:1px solid rgba(177,191,215,.18)}
th{color:var(--gold);font-weight:600;font-size:.82rem;letter-spacing:.05em;
 text-transform:uppercase}
.next{margin-top:3.5rem;padding-top:1.75rem;border-top:1px solid rgba(177,191,215,.18);
 font-size:.95rem;color:var(--dim)}
.next a{display:block;margin-top:.6rem}
.cards{list-style:none;margin:2rem 0 0;padding:0}
.cards li{margin-bottom:1.6rem}
.cards a{font-family:'Montserrat',system-ui,sans-serif;font-size:1.08rem;
 font-weight:600;text-decoration:none}
.cards p{margin:.35rem 0 0;color:var(--dim);font-size:.95rem}
/* Index pillar cards. Same furniture as the og share cards: navy panel,
   gold hairline, a corner bracket top right, a gold tick down the left of
   the heading. */
.pillar{position:relative;margin:2.5rem 0 0;padding:1.7rem 1.6rem 1.5rem;
 background:var(--deep);border:1px solid rgba(232,198,95,.16)}
.pillar::after{content:"";position:absolute;top:13px;right:13px;width:28px;height:28px;
 border-top:1px solid rgba(232,198,95,.4);border-right:1px solid rgba(232,198,95,.4)}
.pillar h2{margin:0;font-size:1.22rem;color:var(--ink);
 border-left:2px solid var(--gold);padding-left:.85rem;padding-right:2.5rem}
.pillar h2 a{color:inherit;text-decoration:none}
.pillar h2 a:hover{color:var(--gold)}
.pillar>p{margin:.6rem 0 0 .85rem;color:var(--dim);font-size:.95rem}
.pillar .cards{margin:1.2rem 0 0 .85rem}
.pillar .cards li{margin-bottom:.7rem}
.pillar .cards a{font-size:1rem;font-weight:500;color:var(--dim)}
.pillar .cards a:hover{color:var(--gold)}
@media(max-width:34rem){.wrap{padding:5.5rem 1.1rem 4rem}body{font-size:16px}
 .pillar{padding:1.4rem 1.2rem 1.2rem}}
"""


def _page(ctx, canonical, title, desc, og_title, og_desc, schema, inner,
          og_type="website", og_img=None, extra=""):
    """One shell for articles, hubs and the index. No bundle, no page JS.

    `og_desc` is the SHORT description, not the lede. It was the lede until
    16 Sep 2026, which meant a 279-character og:description on a card that
    LinkedIn truncates around 150 — so every share cut off mid-sentence. The
    `description` field is capped at 158 by the front-matter check and is
    written for exactly this job.
    """
    og_img = og_img or f"{ctx['origin']}/assets/img/og-home.jpg"
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(title)}</title>
<meta name="description" content="{html.escape(desc, quote=True)}">
<link rel="canonical" href="{canonical}">
<meta name="robots" content="index,follow,max-image-preview:large">

<meta property="og:type" content="{og_type}">
<meta property="og:site_name" content="Parallaxx Transformations">
<meta property="og:url" content="{canonical}">
<meta property="og:title" content="{html.escape(og_title, quote=True)}">
<meta property="og:description" content="{html.escape(og_desc, quote=True)}">
<meta property="og:image" content="{og_img}">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
{extra}
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{html.escape(og_title, quote=True)}">
<meta name="twitter:description" content="{html.escape(og_desc, quote=True)}">
<meta name="twitter:image" content="{og_img}">

<link rel="icon" href="/favicon.png">
<meta name="theme-color" content="{BG}">

{schema}

<style>{CSS}</style>
{ctx['analytics_head']}
</head>
<body>
<parallaxx-nav></parallaxx-nav>
<main class="wrap">
{inner}
</main>
<parallaxx-footer></parallaxx-footer>
<script src="/parallaxx-nav.js"></script>
<script src="/parallaxx-footer.js"></script>
{ctx['analytics_body']}
</body>
</html>
"""


def article_schema(ctx, a) -> str:
    """Article + FAQPage + BreadcrumbList, all pointing at the one #daniel node.

    The author is a reference, not a copy: every article reinforces the same
    Person entity rather than creating a new one. That is the whole reason the
    build emits stable @ids.
    """
    origin = ctx["origin"]
    url = a["url"]
    graph = [{
        "@type": "Article",
        "@id": url + "#article",
        "headline": a["meta"]["title"],
        "description": a["meta"]["description"],
        "url": url,
        "datePublished": a["meta"]["published"],
        "dateModified": a["meta"]["updated"],
        "author": {"@id": ctx["person_id"]},
        "publisher": {"@id": ctx["org_id"]},
        "isPartOf": {"@id": ctx["org_id"]},
        "mainEntityOfPage": url,
        "inLanguage": "en",
    }, {
        "@type": "BreadcrumbList",
        "@id": url + "#crumbs",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Insights",
             "item": f"{origin}/insights"},
            {"@type": "ListItem", "position": 2, "name": a["pillar"]["name"],
             "item": f"{origin}/insights/{a['meta']['pillar']}"},
            {"@type": "ListItem", "position": 3, "name": a["meta"]["title"]},
        ],
    }]
    if a["faq"]:
        graph.append({
            "@type": "FAQPage",
            "@id": url + "#faq",
            "mainEntity": [
                {"@type": "Question", "name": q,
                 "acceptedAnswer": {"@type": "Answer", "text": ans}}
                for q, ans in a["faq"]
            ],
        })
    return ctx["dump_schema"](graph)


def render_article(ctx, a) -> str:
    m = a["meta"]
    pillar_url = f"/insights/{m['pillar']}"
    published = date.fromisoformat(m["published"]).strftime("%-d %B %Y")
    updated = date.fromisoformat(m["updated"]).strftime("%-d %B %Y")
    stamp = published if m["published"] == m["updated"] else f"{published} · updated {updated}"
    # Siblings carry each other's full question as the anchor text. Two pages in
    # one cluster linking to each other with their DIFFERENCE spelled out is how
    # the pair tells a crawler they are distinct rather than duplicate.
    siblings = "".join(
        f'<a href="{sib["path"]}">{inline(sib["meta"]["title"])}</a>\n'
        for sib in a.get("siblings", []))
    offers = "\n".join(
        f'<a href="{o}">{html.escape(OFFER_LABELS.get(o, "See how the work is done"))}</a>'
        for o in [x.strip() for x in m["offer"].split(",") if x.strip()])
    inner = f"""<article>
<div class="meta">{html.escape(a['pillar']['name'])} · {stamp}</div>
<h1>{inline(m['title'])}</h1>
<p class="lede">{inline(m['answer'])}</p>
{a['body']}
<div class="next">
Written by Daniel Lawson, Reconnection Coach.
{siblings}<a href="{pillar_url}">More on {html.escape(a['pillar']['name'].lower())}</a>
{offers}
</div>
</article>"""
    return _page(ctx, a["url"], f"{m['title']} | Parallaxx Transformations",
                 m["description"], m["title"], m["description"],
                 article_schema(ctx, a), inner,
                 og_type="article",
                 og_img=a.get("og_img"),
                 extra=f'<meta property="article:published_time" content="{m["published"]}">\n'
                       f'<meta property="article:modified_time" content="{m["updated"]}">')


def render_hub(ctx, slug, pillar, articles, hub_body) -> str:
    url = f"{ctx['origin']}/insights/{slug}"
    cards = "".join(
        f'<li><a href="{a["path"]}">{inline(a["meta"]["title"])}</a>'
        f'<p>{inline(a["meta"]["answer"][:150])}…</p></li>'
        for a in articles)
    graph = [{
        "@type": "CollectionPage",
        "@id": url + "#webpage",
        "url": url,
        "name": pillar["name"],
        "description": pillar["blurb"],
        "isPartOf": {"@id": ctx["org_id"]},
        "about": {"@id": ctx["person_id"]},
    }]
    inner = (f'<div class="meta">Insights</div><h1>{html.escape(pillar["name"])}</h1>'
             f'<p class="lede">{html.escape(pillar["blurb"])}</p>'
             f'{hub_body}<ul class="cards">{cards}</ul>'
             f'<div class="next"><a href="{pillar["offer"]}">See how the work is done</a></div>')
    return _page(ctx, url, f"{pillar['name']} | Parallaxx Transformations",
                 pillar["blurb"], pillar["name"], pillar["blurb"],
                 ctx["dump_schema"](graph), inner)


def render_index(ctx, by_pillar) -> str:
    url = f"{ctx['origin']}/insights"
    blocks = []
    # A pillar with no articles is SKIPPED, not rendered unlinked. Its hub
    # does not exist yet either -- render_hub holds a hub back until it has
    # children -- so linking one served the homepage at that URL, which is the
    # soft-404 pattern Google penalises. Three of the five did exactly that.
    for slug, pillar in PILLARS.items():
        items = by_pillar.get(slug, [])
        if not items:
            continue
        cards = "".join(
            f'<li><a href="{a["path"]}">{inline(a["meta"]["title"])}</a></li>'
            for a in items[:6])
        blocks.append(
            f'<section class="pillar">'
            f'<h2><a href="/insights/{slug}">{html.escape(pillar["name"])}</a></h2>'
            f'<p>{html.escape(pillar["blurb"])}</p>'
            f'<ul class="cards">{cards}</ul></section>')
    graph = [{
        "@type": "CollectionPage", "@id": url + "#webpage", "url": url,
        "name": "Insights", "isPartOf": {"@id": ctx["org_id"]},
        "about": {"@id": ctx["person_id"]},
    }]
    inner = ('<h1>Insights</h1><p class="lede">Questions that come up in the '
             'rooms, answered the way they get answered there.</p>'
             + "".join(blocks))
    return _page(ctx, url, "Insights | Parallaxx Transformations",
                 "Questions that come up in the rooms, answered the way they "
                 "get answered there.", "Insights",
                 "Questions that come up in the rooms.",
                 ctx["dump_schema"](graph), inner)


# ── ENTRY POINT ────────────────────────────────────────────────────────
def build(ctx, content_dir: Path, dist: Path) -> tuple:
    """Writes every article, hub and the index. Returns (urls, errors).

    urls feed the sitemap. A non-empty errors list must fail the build —
    build-site.py is responsible for making that so.
    """
    errors, by_pillar = [], {}
    if not content_dir.is_dir():
        return [], []

    for path in sorted(content_dir.rglob("*.md")):
        where = str(path.relative_to(content_dir.parent))
        raw = path.read_text(encoding="utf-8")
        if path.name == "_hub.md":
            # Guarded and parsed HERE, not in the pillar loop below, because a
            # hub only renders once its pillar has articles. Checking it only
            # at render time means a hub intro written months earlier gets its
            # first confidentiality check on the day it silently goes live.
            errors.extend(guard(raw, where))
            try:
                render_body(raw, where)
            except ValueError as e:
                errors.append(str(e))
            continue
        errors.extend(guard(raw, where))
        try:
            meta, body_md = parse_front_matter(raw, where)
            body, faq = render_body(body_md, where)
        except ValueError as e:
            errors.append(str(e))
            continue
        if meta["pillar"] not in PILLARS:
            errors.append(f"{where}: unknown pillar {meta['pillar']!r}. "
                          f"Known: {', '.join(PILLARS)}")
            continue
        slug = meta.get("slug") or path.stem
        rel = f"/insights/{meta['pillar']}/{slug}"
        by_pillar.setdefault(meta["pillar"], []).append(dict(
            meta=meta, body=body, faq=faq, path=rel,
            url=ctx["origin"] + rel, pillar=PILLARS[meta["pillar"]]))

    # ── THE CANNIBALISATION GUARD ──────────────────────────────────────
    # Two pages answering the same question is the failure this pipeline is
    # most likely to produce at volume, because the keyword map counts QUERIES
    # and a query is not an intent. Pillar 1's four winnable rows turned out to
    # be two intents, and two of the first three articles argued the same thing
    # in different words. Google picks one, both underperform, and a model
    # choosing which page of yours to quote has no reason to prefer either.
    #
    # `intent` is declared per article and must be unique across the whole site.
    # The test for whether two pages may coexist is not whether their queries
    # differ. It is: WOULD THE CORRECT ANSWER BE DIFFERENT? Same answer, same
    # intent, one page — and the other phrasings become headings inside it.
    seen = {}
    for items in by_pillar.values():
        for a in items:
            key = a["meta"]["intent"].strip().lower()
            if key in seen:
                errors.append(
                    f"{a['path']}: intent {key!r} is already claimed by "
                    f"{seen[key]}. Two pages answering the same question compete "
                    f"with each other. Fold one into the other and make its "
                    f"phrasing a heading, or change the claim so the answers "
                    f"genuinely differ.")
            seen[key] = a["path"]

    # A softer signal for the near-misses a declared intent will not catch:
    # two ledes made of the same words are usually two versions of one page.
    def words(t):
        return {w for w in re.findall(r"[a-z']{4,}", t.lower())}
    flat = [a for items in by_pillar.values() for a in items]
    for i, a in enumerate(flat):
        for b in flat[i + 1:]:
            wa, wb = words(a["meta"]["answer"]), words(b["meta"]["answer"])
            if wa and wb:
                j = len(wa & wb) / len(wa | wb)
                if j > 0.42:
                    print(f"WARNING: {a['path']} and {b['path']} have ledes "
                          f"{j:.0%} alike. Check they answer different questions.")

    if errors:
        return [], errors

    # Resolve each article's share card against what is actually in dist/, the
    # same way head_html() resolves the routes' og images. A card declared in
    # front matter with no PNG behind it would otherwise emit a URL that 404s,
    # and a blank thumbnail is only ever discovered by someone sharing the link.
    urls = []
    for slug, items in by_pillar.items():
        items.sort(key=lambda a: a["meta"]["published"], reverse=True)
        for a in items:
            rel = f"img/og-{a['meta'].get('slug') or ''}.png"
            if (dist / "assets" / rel).exists():
                a["og_img"] = f"{ctx['origin']}/assets/{rel}"
            elif a["meta"].get("card"):
                print(f"WARNING: {a['path']} declares a card line but "
                      f"assets/{rel} is missing. Run og_card_articles.py and "
                      f"commit the PNG. Falling back to the site's default "
                      f"share image.")
            a["siblings"] = [x for x in items if x is not a][:3]
            out = dist / a["path"].strip("/") / "index.html"
            out.parent.mkdir(parents=True, exist_ok=True)
            out.write_text(render_article(ctx, a), encoding="utf-8")
            urls.append((a["path"], a["meta"]["updated"]))

    for slug, pillar in PILLARS.items():
        items = by_pillar.get(slug, [])
        if not items:
            continue  # An empty hub is a thin page. It ships when it has children.
        hub_md = content_dir / slug / "_hub.md"
        hub_body = ""
        if hub_md.exists():  # already guarded and parsed in the loop above
            hub_body, _ = render_body(hub_md.read_text(encoding="utf-8"),
                                      f"{slug}/_hub.md")
        out = dist / "insights" / slug / "index.html"
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(render_hub(ctx, slug, pillar, items, hub_body), encoding="utf-8")
        urls.append((f"/insights/{slug}", max(a["meta"]["updated"] for a in items)))

    if by_pillar:
        out = dist / "insights" / "index.html"
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(render_index(ctx, by_pillar), encoding="utf-8")
        urls.append(("/insights", max(u[1] for u in urls)))

    return urls, errors

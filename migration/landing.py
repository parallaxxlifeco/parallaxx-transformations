"""
landing.py -- small single-purpose pages that are not Wix ports and not articles.

Each one is a plain static page: the shared nav and footer, one job, no page
bundle. Built by build-site.py after the articles, into the same dist/.

They are noindex and left out of the sitemap on purpose. These are pages Daniel
sends to someone (a DM, an email, an ad), and their content already lives on an
indexed page -- Brian's clip is on /men. Indexing a second page holding the same
49 seconds would only compete with the page that has the context around it.

To add another: copy the TESTIMONIAL_BRIAN dict, change the fields, and add it
to PAGES. Video and poster are given as their Wix CDN URLs, exactly as the
asset map lists them, so a --local build serves our own copies -- or as
/assets/ paths for files added straight to migration/wix-assets/.
"""

import html
import pathlib
import re
from datetime import date

REPO = pathlib.Path(__file__).resolve().parent.parent

BOOK_CALL = "/contact-daniel-lawson"
TESTIMONIALS = "/testimonials-daniel-lawson"

TESTIMONIAL_BRIAN = dict(
    path="/testimonial-brian",
    title="Brian’s shared experience | Parallaxx Transformations",
    desc="Brian B, Reconnect client, United Kingdom, in his own words.",
    heading="Brian’s shared experience",
    # The 82s recut made for this page (5 Oct 2026), not the 49s clip on /men.
    # Both files live in migration/wix-assets/, which the build copies to
    # /assets/. The poster is the frame at 7.5s, with his name card on screen.
    video="/assets/video/brian-reconnect-testimonial-90s.mp4",
    poster="/assets/img/brian-reconnect-testimonial-poster.jpg",
    primary=("Book Complimentary Call", BOOK_CALL),
    secondary=("See more of what others are saying", TESTIMONIALS),
)

# After the Three Toxic Lies sign-up (15 Oct 2026). The form posts to GHL
# and sends the browser here. Daniel's brief: the book is in their inbox,
# check Promotions, and reply when it arrives (a reply is what tells the
# inbox these emails are wanted).
TTL_THANKS = dict(
    path="/three-toxic-lies/thank-you",
    title="It’s on its way | Three Toxic Lies",
    desc="Three Toxic Lies is on its way to your inbox.",
    eyebrow="Your free book",
    heading="Three Toxic Lies is on its way to your inbox.",
    image="/assets/img/toxic-lies-cover.png",
    steps=[
        ("Give it a few minutes",
         "If it’s not there, check your Promotions tab or spam folder, and move it to "
         "your inbox so the next ones arrive there too."),
        ("Hit reply when it arrives", "Let me know it got to you."),
    ],
    primary=("Check out the Insights", "/insights/"),
    lead="three_toxic_lies",
)


# ── THANK-YOU PAGES THAT COUNT SIGN-UPS (30 Oct 2026) ────────────────────
# GA4 can't see inside the GHL forms (they are iframes), so each form's
# on-submit setting in GHL sends the whole browser to one of these pages,
# and the page fires one GA4 event:
#     generate_lead { form_name, source_page }
# source_page is the last page the visitor was on before this one. Every page
# on the site stores its path in sessionStorage as px-src (analytics_body() in
# build-site.py), and these pages are left out of that, so the value they read
# is the page the form was on: for the Insights form, which article.
# The event fires once per form per browser tab (sessionStorage px-lead-<form>),
# so a refresh doesn't count twice.
#
# TO ADD ONE FOR A NEW FORM: copy a dict below, give it its own path under
# /thanks/, a new `lead` name (lowercase_with_underscores), add it to PAGES,
# then set that form's on-submit in GHL to Redirect to URL with the full
# https://www.parallaxxtransformations.com/thanks/<name>/ address.
#
# LAYOUT (31 Oct 2026, Daniel: an oversized title over a wall of text is poor
# UX): a small eyebrow, a modest heading saying what they signed up for, a
# session card on the circle pages, then numbered steps and one button.
#
# The circle pages read their open-session date and times from the same
# element the circle page uses (#rw-open / #rm-open), so the monthly date edit
# carries over.
#
# BETWEEN SESSIONS (Daniel, 30 Oct 2026). Once the date has passed, and until
# the next date is set and pushed, the page switches itself to the waiting-list
# version: "You're on the list", a card reading "Next open session / Date to
# be confirmed", and a first step saying she'll be emailed the moment the next
# date is set. That matches what GHL sends in the same gap (the dateless
# "You're on the list" email). Setting the next date on the circle page and
# pushing is the only edit; this page follows it. The waiting-list wording is
# _LIST_STEP and _LIST_EYEBROW below.
# (Old note:) Once the date has passed the card says "Next open session"
# and drops the times rather than naming a gone day.

def _open_session(src, el_id):
    """(ISO date, 'Tuesday 24 November', '08:30 CET / 15:30 GMT+8')."""
    s = (REPO / src).read_text(encoding="utf-8")
    m = re.search(r'id="%s"(.*?)></div>' % el_id, s, re.S)
    if not m:
        raise SystemExit(f"landing.py: no #{el_id} in {src}")
    a = m.group(1)
    d = re.search(r'data-open-at="(\d{4})-(\d{2})-(\d{2})', a)
    t = re.search(r'data-open-times="([^"]*)"', a)
    if not d:
        raise SystemExit(f"landing.py: no data-open-at on #{el_id} in {src}")
    dd = date(int(d[1]), int(d[2]), int(d[3]))
    return dd.isoformat(), f"{dd:%A} {dd.day} {dd:%B}", (t[1] if t else "")


_LIST_EYEBROW = "You’re on the list"
_LIST_STEP = ("Watch your inbox",
              "The next date is being set. As soon as it is, I’ll email you the date, the "
              "time and the link to join. Check your Promotions tab or spam folder too, and "
              "move my email to your inbox so it gets to you.")

_INBOX_STEP = ("Check your inbox",
               "Your confirmation has the time and the link to join. If it’s not there in "
               "a few minutes, check your Promotions tab or spam folder and move it to your "
               "inbox, so the reminders get to you too.")

RW_THANKS = dict(
    path="/thanks/reconnected-woman",
    title="You’re registered | The Reconnected Woman",
    desc="Your place at The Reconnected Woman open session.",
    eyebrow="You’re registered",
    heading="The Reconnected Woman open session",
    open_session=("reconnected-woman-v10-preview.html", "rw-open"),
    steps=[
        _INBOX_STEP,
        ("Take the Priority Audit",
         "It takes ten minutes, it shows you which priority gives you the most return, "
         "and I’ll have your results before we meet."),
    ],
    primary=("Take the Priority Audit", "/priority-audit/"),
    lead="reconnected_woman",
)

# Built now; the men's GHL form keeps its old on-submit until the men's
# confirmation sequence is live (Daniel, 30 Oct 2026), because this page
# promises a confirmation email.
RM_THANKS = dict(
    path="/thanks/reconnected-man",
    title="You’re registered | The Reconnected Man",
    desc="Your place at The Reconnected Man open session.",
    eyebrow="You’re registered",
    heading="The Reconnected Man open session",
    open_session=("reconnected-man-v2-preview.html", "rm-open"),
    steps=[
        _INBOX_STEP,
        ("Take the Protection Archetype Quiz",
         "It takes a few minutes, it shows you which of five patterns you’re running and "
         "what it’s costing the people closest to you, and I’ll have your results before "
         "we meet."),
    ],
    primary=("Take the quiz", "/the-archetype-quiz/"),
    lead="reconnected_man",
)

# Double opt-in: this fires when the form is submitted, BEFORE the reader
# confirms by email, so GA4's insights_subscribe count runs higher than the
# confirmed subscribers in GHL (tag insights-subscriber).
SUB_THANKS = dict(
    path="/thanks/subscribed",
    title="Check your inbox | Insights",
    desc="Confirm your subscription to the weekly Insights roundup.",
    eyebrow="The weekly Insights roundup",
    heading="Nearly there. Check your inbox.",
    steps=[
        ("Confirm your email",
         "I’ve sent you an email with a link to confirm. Click it and you’re on the list "
         "for the weekly roundup, every Sunday."),
        ("Can’t see it?", "Check your Promotions tab or spam folder."),
    ],
    primary=("Back to the Insights", "/insights/"),
    back_to_article=True,
    lead="insights_subscribe",
)

PAGES = [TESTIMONIAL_BRIAN, TTL_THANKS, RW_THANKS, RM_THANKS, SUB_THANKS]

LEAD_JS = """<script>
(function(){
  var F = %s, src = '', k = 'px-lead-' + F, done = null;
  try { src = sessionStorage.getItem('px-src') || ''; done = sessionStorage.getItem(k); } catch (e) {}
  if (!done && typeof gtag === 'function') {
    gtag('event', 'generate_lead', {form_name: F, source_page: src || '(not set)'});
    try { sessionStorage.setItem(k, '1'); } catch (e) {}
  }%s
})();
</script>"""

DATE_JS = """
  var w = document.querySelector('.js-open-when');
  if (w) {
    var t = new Date(), today = t.getFullYear() + '-' + ('0' + (t.getMonth() + 1)).slice(-2) + '-' + ('0' + t.getDate()).slice(-2);
    if (w.getAttribute('data-at') < today) {
      w.textContent = 'Next open session';
      var tm = document.querySelector('.js-open-times'); if (tm) tm.textContent = 'Date to be confirmed';
      var ps = document.querySelectorAll('[data-past]');
      for (var i = 0; i < ps.length; i++) ps[i].textContent = ps[i].getAttribute('data-past');
    }
  }"""

BACK_JS = """
  var b = document.getElementById('px-back');
  if (b && /^\\/insights\\/./.test(src)) { b.href = src; b.firstChild.nodeValue = 'Back to the article '; }"""

CSS = """
:root{--bg:#061938;--deep:#04122A;--cream:#F1ECE1;--mist:#B1BFD7;--slate:#7C89A3;
 --gold:#E8C65F;--coral:#FF501F;--coral-lift:#FF6A3D;--border:#1B2C46}
*{box-sizing:border-box}
html,body{margin:0;background:var(--bg);color:var(--mist)}
body{font:400 16px/1.6 'Montserrat',system-ui,-apple-system,sans-serif;-webkit-font-smoothing:antialiased;
 min-height:100vh;display:flex;flex-direction:column}
main{flex:1;display:flex;align-items:center;justify-content:center;
 padding:clamp(104px,14vh,150px) 20px clamp(56px,9vh,96px);
 background:radial-gradient(ellipse at 50% 0%,#0F2448 0%,var(--bg) 62%)}
.tm{width:100%;max-width:820px;text-align:center}
.tm h1{margin:0 0 26px;font:500 clamp(1.7rem,4.6vw,2.6rem)/1.2 'Poppins',system-ui,sans-serif;
 letter-spacing:-.01em;color:var(--cream)}
.vid{position:relative;border-radius:16px;overflow:hidden;border:1px solid var(--border);
 background:#000;aspect-ratio:16/9;box-shadow:0 24px 60px rgba(0,0,0,.45)}
.vid video{display:block;width:100%;height:100%;object-fit:cover;background:#000}
.cta{display:flex;flex-direction:column;align-items:center;gap:16px;margin-top:34px}
.btn{display:inline-flex;align-items:center;justify-content:center;gap:10px;
 background:var(--coral);color:#fff;text-decoration:none;font:600 1rem/1 'Poppins',system-ui,sans-serif;
 padding:17px 32px;border-radius:999px;box-shadow:0 12px 32px rgba(255,80,31,.3);
 transition:background .2s,transform .2s}
.btn:hover,.btn:focus-visible{background:var(--coral-lift);transform:translateY(-1px)}
.btn:focus-visible{outline:2px solid var(--cream);outline-offset:3px}
.sec{color:var(--cream);text-decoration:none;font-weight:600;font-size:.92rem;
 padding:6px 2px;border-bottom:1px solid rgba(232,198,95,.5)}
.sec:hover,.sec:focus-visible{color:var(--gold);border-bottom-color:var(--gold)}
@media(max-width:520px){.btn{width:100%}}
.msgpage .cover{width:min(300px,70vw);height:auto;margin:0 auto 22px;display:block;
 filter:drop-shadow(0 24px 40px rgba(0,0,0,.5))}
.msgpage p{max-width:46ch;margin:0 auto 14px;font-size:1.05rem;line-height:1.7;text-wrap:balance}
.msgpage h1{text-wrap:balance}
/* THANK-YOU LAYOUT (31 Oct 2026): eyebrow, modest heading, session card,
   numbered steps, one button. Left-aligned in a narrow column. */
.ty{width:100%;max-width:560px;text-align:left}
.ty .cover{width:112px;height:auto;display:block;margin:0 0 22px;
 filter:drop-shadow(0 16px 28px rgba(0,0,0,.5))}
.ty .ey{margin:0 0 10px;font:700 .68rem/1.4 'Poppins',system-ui,sans-serif;letter-spacing:.2em;
 text-transform:uppercase;color:var(--gold)}
.ty h1{margin:0 0 24px;font:600 clamp(1.45rem,3.2vw,1.95rem)/1.25 'Poppins',system-ui,sans-serif;
 letter-spacing:-.01em;color:var(--cream);text-wrap:balance}
.ty .card{display:grid;gap:3px;margin:0 0 28px;padding:16px 20px;border:1px solid var(--border);
 border-left:2px solid var(--gold);border-radius:4px;background:rgba(10,29,60,.65)}
.ty .card .d{font:600 1.12rem/1.35 'Poppins',system-ui,sans-serif;color:var(--cream)}
.ty .card .t{color:var(--mist);font-size:.95rem}
.ty .card .w{color:var(--slate);font-size:.88rem}
.ty .steps{list-style:none;counter-reset:st;margin:0 0 30px;padding:0;display:grid;gap:20px}
.ty .steps li{display:grid;grid-template-columns:32px minmax(0,1fr);gap:16px;align-items:start}
.ty .steps li::before{counter-increment:st;content:counter(st);width:32px;height:32px;border-radius:50%;
 border:1px solid rgba(232,198,95,.6);color:var(--gold);display:flex;align-items:center;
 justify-content:center;font:600 .85rem/1 'Poppins',system-ui,sans-serif}
.ty .steps h2{margin:5px 0 4px;font:600 1rem/1.35 'Poppins',system-ui,sans-serif;color:var(--cream)}
.ty .steps p{margin:0;font-size:.97rem;line-height:1.6;color:var(--mist)}
"""


def _inner(p, e) -> str:
    """A video page (the testimonial) or a message page (a thank-you)."""
    if p.get("video"):
        return f"""  <div class="tm">
    <h1>{e(p['heading'])}</h1>
    <div class="vid">
      <video controls playsinline preload="metadata" poster="{e(p['poster'])}" src="{e(p['video'])}"></video>
    </div>
    <div class="cta">
      <a class="btn" href="{e(p['primary'][1])}">{e(p['primary'][0])} <span aria-hidden="true">&rarr;</span></a>
      <a class="sec" href="{e(p['secondary'][1])}">{e(p['secondary'][0])}</a>
    </div>
  </div>"""
    img = f'<img class="cover" src="{e(p["image"])}" alt="">' if p.get("image") else ""
    card = ""
    if p.get("open_session"):
        iso, pretty, times = _open_session(*p["open_session"])
        card = (f'<div class="card"><span class="d js-open-when" data-at="{iso}">{e(pretty)}</span>'
                f'<span class="t js-open-times">{e(times)}</span>'
                f'<span class="w">Online, wherever you are</span></div>')
    dated = bool(p.get("open_session"))
    def _past(i, k):
        # the waiting-list wording, swapped in by DATE_JS once the date has gone
        if not dated or i != 0:
            return ""
        return f' data-past="{e(_LIST_STEP[k])}"'
    steps = "".join(f'<li><div><h2{_past(i, 0)}>{e(h)}</h2><p{_past(i, 1)}>{e(t)}</p></div></li>'
                    for i, (h, t) in enumerate(p.get("steps", [])))
    steps = f'<ol class="steps">{steps}</ol>' if steps else ""
    prim = ""
    if p.get("primary"):
        bid = ' id="px-back"' if p.get("back_to_article") else ""
        prim = (f'<a class="btn"{bid} href="{e(p["primary"][1])}">'
                f'{e(p["primary"][0])} <span aria-hidden="true">&rarr;</span></a>')
    eyp = f' data-past="{e(_LIST_EYEBROW)}"' if dated else ""
    ey = f'<p class="ey"{eyp}>{e(p["eyebrow"])}</p>' if p.get("eyebrow") else ""
    return f"""  <div class="ty">
    {img}
    {ey}
    <h1>{e(p['heading'])}</h1>
    {card}
    {steps}
    {prim}
  </div>"""


def _lead_js(p) -> str:
    if not p.get("lead"):
        return ""
    extra = (DATE_JS if p.get("open_session") else "") + (BACK_JS if p.get("back_to_article") else "")
    return LEAD_JS % ("'" + p["lead"] + "'", extra)


def render(ctx, p) -> str:
    # Trailing slash: Pages 301s the slashless form, so the canonical must be the final URL.
    canonical = ctx["origin"] + "/" + p["path"].strip("/") + "/"
    e = lambda s: html.escape(s, quote=True)
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(p['title'])}</title>
<meta name="description" content="{e(p['desc'])}">
<link rel="canonical" href="{canonical}">
<meta name="robots" content="noindex,follow">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Parallaxx Transformations">
<meta property="og:url" content="{canonical}">
<meta property="og:title" content="{e(p['title'])}">
<meta property="og:description" content="{e(p['desc'])}">
<meta property="og:image" content="{e(p.get('poster') or p.get('image',''))}">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="/favicon.png">
<meta name="theme-color" content="#061938">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@400;600;700&family=Poppins:wght@500;600&display=swap" rel="stylesheet">
<style>{CSS}</style>
{ctx['analytics_head']}
</head>
<body>
<parallaxx-nav></parallaxx-nav>
<main>
{_inner(p, e)}
</main>
<parallaxx-footer></parallaxx-footer>
<script src="/parallaxx-nav.js"></script>
<script src="/parallaxx-footer.js"></script>
{ctx['analytics_body']}
{_lead_js(p)}
</body>
</html>
"""


def build(ctx, dist, localise=None) -> list:
    """Write every page in PAGES. Returns the paths written."""
    written = []
    for p in PAGES:
        text = render(ctx, p)
        if localise:
            text = localise(text)
        # og:image has to be absolute for the scrapers, and the poster is a
        # root-relative /assets/ path.
        text = text.replace('property="og:image" content="/',
                            'property="og:image" content="' + ctx["origin"] + '/')
        out = dist / p["path"].strip("/") / "index.html"
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(text, encoding="utf-8")
        written.append(p["path"])
    return written

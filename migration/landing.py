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

PAGES = [TESTIMONIAL_BRIAN]

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
"""


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
<meta property="og:image" content="{e(p['poster'])}">
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
  <div class="tm">
    <h1>{e(p['heading'])}</h1>
    <div class="vid">
      <video controls playsinline preload="metadata" poster="{e(p['poster'])}" src="{e(p['video'])}"></video>
    </div>
    <div class="cta">
      <a class="btn" href="{e(p['primary'][1])}">{e(p['primary'][0])} <span aria-hidden="true">&rarr;</span></a>
      <a class="sec" href="{e(p['secondary'][1])}">{e(p['secondary'][0])}</a>
    </div>
  </div>
</main>
<parallaxx-footer></parallaxx-footer>
<script src="/parallaxx-nav.js"></script>
<script src="/parallaxx-footer.js"></script>
{ctx['analytics_body']}
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

"""
rw_join.py -- The Reconnected Woman: the page a woman joins from.

One job: she picks her currency, sees the price in it, and goes to Stripe.
Built by landing.py (so it is noindex and out of the sitemap). It carries no
site menu and no site footer, only the site's own analytics. No form, and nothing
is sent anywhere from this page: the button is a plain link to Stripe.

EDIT THE ONE TABLE BELOW AND NOTHING ELSE FOR A PRICE OR LINK CHANGE.
"""

# ── THE PRICE TABLE ─────────────────────────────────────────────────────
# One row per currency: code, how the amount is written, the monthly amount,
# the first-month amount, and THAT CURRENCY'S OWN Stripe Payment Link.
#
# The picker is real: the currency she chooses is the Payment Link the Join
# button opens, so she is billed in that currency. The amounts here are only
# what the page shows; each must match the amounts set on its own link in
# Stripe.
#
# To switch a currency on, paste its Payment Link between the quotes (it
# starts with https://buy.stripe.com/). A row whose link still reads
# PLACEHOLDER is not offered in the picker. EUR must stay first and must
# have a link before the page can go live: it is the fallback.
PRICES = [
    # code   written   monthly  first month  Stripe Payment Link
    ("EUR", "€",         119,     89,  "PLACEHOLDER_STRIPE_LINK_EUR"),
    ("AUD", "A$",        199,    149,  "PLACEHOLDER_STRIPE_LINK_AUD"),
    ("USD", "US$",       139,     99,  "PLACEHOLDER_STRIPE_LINK_USD"),
    ("GBP", "£",          99,     75,  "PLACEHOLDER_STRIPE_LINK_GBP"),
    ("CAD", "CA$",       189,    139,  "PLACEHOLDER_STRIPE_LINK_CAD"),
    ("NZD", "NZ$",       239,    179,  "PLACEHOLDER_STRIPE_LINK_NZD"),
    ("SGD", "S$",        175,    129,  "PLACEHOLDER_STRIPE_LINK_SGD"),
    ("CHF", "CHF ",      109,     85,  "PLACEHOLDER_STRIPE_LINK_CHF"),
    ("ZAR", "R",        2299,   1699,  "PLACEHOLDER_STRIPE_LINK_ZAR"),
]

# ── THE FIRST-MONTH PROMOTION CODE ──────────────────────────────────────
# The first-month price is one Stripe promotion code. The Join button adds
# it to whichever currency's Payment Link is chosen, as
# ?prefilled_promo_code=FIRSTMONTH, so Stripe opens with it already applied.
# Leave it empty ("") to add nothing. The code must exist in Stripe and the
# Payment Link must allow promotion codes, or Stripe ignores it.
PROMO_CODE = "FIRSTMONTH"

# Which currency a browser's country gets by default. Anywhere not listed,
# and any currency whose link is not set yet, gets EUR.
COUNTRY_CURRENCY = {
    "AU": "AUD", "US": "USD", "GB": "GBP", "CA": "CAD",
    "NZ": "NZD", "SG": "SGD", "CH": "CHF", "LI": "CHF", "ZA": "ZAR",
}

# ── WORDING ─────────────────────────────────────────────────────────────
# All of it is Daniel's, as he gave it on 23 Nov 2026 (the top line and the two
# questions are from the Reconnected Woman page). Two spellings were his
# typing put right, and he can reverse either: "monthly membership" (he typed
# "month membership") and "accountability" (he typed "accountably").
#
# Anything he has NOT written goes in PLACEHOLDERS, is shown on the page in a
# dashed box, and stops the live site building while it is left. There are
# none at the moment.
WORDS = dict(
    eyebrow="The Reconnected Woman",
    # Across the top, above both columns, set as a quotation: the reminder of
    # why she is joining.
    # (Variable names still say "quote"; since 23 Nov it carries no quotation
    # marks. The second part is the part set in gold.)
    quote="Figure out what you want, ask for it, and get ",
    quote_gold="better results with less effort.",
    # The page's one h1, above the payment column.
    heading="Join Us",
    included_heading="Included in your monthly membership",
    includes=[
        "Four unique weekly sessions together",
        "Intention and accountability to ensure your progress sticks",
        "Live facilitation and hot seat coaching opportunities",
        "Whatsapp community support between sessions",
        "Complimentary 1:1 call on week 6",
    ],
    terms="Your joining membership price is saved and never increases as long as you "
          "stay. Memberships roll over monthly. Cancel anytime.",
    # Under the payment column. Set bonus_heading to "" to drop the whole box.
    bonus_heading="ACTION TAKER BONUS",
    bonus="The first 3 registrations in will be gifted a personalised accelerator 1:1 "
          "with Daniel designed to fast track your first month results. ACT NOW - "
          "limited to 3 spots only.",
    faq=[
        ("Can I cancel?",
         "Yes, any time. It’s month to month, and your membership runs to the end of "
         "the month you’ve paid for."),
        ("What if I’m away for a month?",
         "You can pause once a year, for up to a month, and you keep your price. Ask "
         "before your next payment."),
    ],
)

PLACEHOLDERS = dict()

# Plain labels. Not sales copy.
LABEL_FIRST = "First month"
LABEL_THEN = "Then"
LABEL_MONTH = "a month"
LABEL_PICKER = "Select your currency"
BUTTON = "Join"


def _has_link(row) -> bool:
    return row[4].startswith("https://")


def join_url(link: str) -> str:
    """The Payment Link with the promotion code added. Copes with a link that
    already has a ?query or a #fragment, and never adds the code twice."""
    if not PROMO_CODE:
        return link
    from urllib.parse import urlsplit, urlunsplit, parse_qsl, urlencode
    u = urlsplit(link)
    q = [(k, v) for k, v in parse_qsl(u.query, keep_blank_values=True) if k != "prefilled_promo_code"]
    q.append(("prefilled_promo_code", PROMO_CODE))
    return urlunsplit((u.scheme, u.netloc, u.path, urlencode(q), u.fragment))


def offered() -> list:
    """The rows the picker offers: those with a Payment Link. On a preview
    with no links at all, every row is shown so the page can be looked at,
    and the button is switched off."""
    rows = [r for r in PRICES if _has_link(r)]
    return rows or list(PRICES)


def check(live: bool) -> list:
    """Problems that must stop the LIVE site from building. On a preview they
    are only warnings, so the page can be looked at before it is finished."""
    problems = []
    if PRICES[0][0] != "EUR":
        problems.append("rw_join.py: EUR must be the first row of PRICES")
    elif not _has_link(PRICES[0]):
        problems.append("rw_join.py: the EUR Stripe Payment Link is still a placeholder")
    for k, v in PLACEHOLDERS.items():
        if "PLACEHOLDER" in v:
            problems.append(f"rw_join.py: PLACEHOLDERS['{k}'] is still a placeholder")
    return problems


def _amount(written, n):
    return f"{written}{n}"


CSS = """
/* LAYOUT. Across the top, full width: the eyebrow and the opening line. On a phone
   everything then stacks: Join Us and the payment block, the bonus, then what
   is included. From 900px it is two columns: payment and bonus on the LEFT
   (they stay in view while the right side scrolls), the details on the RIGHT. */
.jn{width:100%;max-width:560px;text-align:left;display:grid;gap:28px;
 grid-template-columns:minmax(0,1fr);grid-template-areas:"head" "pay" "det"}
.jn-head{grid-area:head}.jn-pay{grid-area:pay}.jn-det{grid-area:det}
@media(min-width:900px){
 main{align-items:flex-start}
 .jn{max-width:1040px;column-gap:clamp(36px,5vw,72px);row-gap:clamp(34px,5vh,52px);
  grid-template-columns:minmax(0,380px) minmax(0,1fr);grid-template-areas:"head head" "pay det"}
 .jn-pay{align-self:start;position:sticky;top:36px}
}
/* NO MENU AND NO FOOTER on this page, so the top padding that cleared the
   fixed menu comes down. */
body.bare main{padding-top:clamp(36px,7vh,72px)}
/* THE ANALYTICS NOTICE, kept as on every page but quieter here: smaller
   type, less padding, plainer buttons. Same words, same two choices. */
body.bare #px-consent{font-size:12px;line-height:1.45;padding:9px 14px;gap:6px 12px;
 background:#04122A;color:#B1BFD7;box-shadow:none;border-top:1px solid #1B2C46}
body.bare #px-consent a{color:#B1BFD7}
body.bare #px-consent button{padding:5px 12px;border-color:#7C89A3;color:#B1BFD7}
body.bare #px-consent button.px-yes{background:transparent;color:#F1ECE1;border-color:#B1BFD7}

.jn .ey{margin:0 0 14px;font:800 .62rem/1.4 'Poppins',system-ui,sans-serif;letter-spacing:.24em;
 text-transform:uppercase;color:var(--gold)}
.jn .quote{margin:0;padding:2px 0 2px 20px;border-left:2px solid var(--gold);
 font:italic 500 clamp(1.15rem,4.6vw,1.6rem)/1.45 'Montserrat',system-ui,sans-serif;color:var(--cream);
 text-wrap:balance;max-width:34em}
.jn .quote .g{color:var(--gold)}
.jn h1,.jn .h2{margin:0 0 16px;font:600 clamp(1.35rem,4.8vw,1.7rem)/1.25 'Poppins',system-ui,sans-serif;
 letter-spacing:-.01em;color:var(--cream);text-wrap:balance}
.jn .bonus{margin:18px 0 0;padding:18px 22px 20px;border:1px solid var(--border);border-left:2px solid var(--coral);
 background:rgba(10,29,60,.65)}
.jn .bonus h2{margin:0 0 8px;font:800 .68rem/1.4 'Poppins',system-ui,sans-serif;letter-spacing:.2em;
 text-transform:uppercase;color:var(--gold)}
.jn .bonus p{margin:0;font-size:.95rem;line-height:1.6;color:var(--mist)}
.jn .inc{list-style:none;margin:0;padding:0}
.jn .inc li{position:relative;padding:9px 0 9px 26px;border-top:1px solid var(--border);
 font-size:1rem;color:var(--mist)}
.jn .inc li:last-child{border-bottom:1px solid var(--border)}
.jn .inc li:before{content:'';position:absolute;left:0;top:1.35em;width:11px;height:1px;background:var(--gold)}
.jn .price{margin:0;padding:22px 22px 24px;background:#0A1D3C;border:1px solid var(--border);
 border-top:2px solid var(--gold)}
.jn .price .row{display:flex;align-items:baseline;justify-content:space-between;gap:14px}
.jn .price .lab{font:700 .68rem/1.4 'Poppins',system-ui,sans-serif;letter-spacing:.16em;
 text-transform:uppercase;color:var(--mist)}
.jn .price .first{font:700 clamp(2.1rem,9vw,2.9rem)/1 'Poppins',system-ui,sans-serif;color:var(--gold);
 white-space:nowrap}
.jn .price .then{margin:12px 0 0;padding-top:12px;border-top:1px solid var(--border);
 font-size:1rem;color:var(--cream)}
.jn .price .then b{font-weight:600;color:var(--cream)}
.jn .pick{display:flex;flex-direction:column;align-items:flex-start;gap:7px;margin:16px 0 0;font-size:.82rem;color:var(--mist)}
.jn .pick select{appearance:auto;background:var(--bg);color:var(--cream);border:1px solid var(--border);
 border-radius:2px;padding:9px 10px;font:600 .9rem/1 'Montserrat',system-ui,sans-serif;min-height:40px}
.jn .pick select:focus-visible{outline:2px solid var(--gold);outline-offset:2px}
.jn .join{display:block;width:100%;margin:20px 0 0;text-align:center;text-decoration:none;
 background:var(--coral);color:#fff;font:700 .82rem/1 'Poppins',system-ui,sans-serif;letter-spacing:.13em;
 text-transform:uppercase;padding:19px 30px;border-radius:2px;transition:background .22s ease,transform .22s ease}
.jn .join:hover,.jn .join:focus-visible{background:var(--coral-lift);transform:translateY(-2px)}
.jn .join:focus-visible{outline:2px solid var(--gold);outline-offset:3px}
.jn .join[aria-disabled=true]{background:#3A4660;color:#B1BFD7;pointer-events:none;transform:none}
.jn .terms{margin:22px 0 0;font-size:.95rem;line-height:1.65;color:var(--slate)}
.jn .ph{margin:18px 0 0;padding:12px 14px;border:1px dashed var(--gold);color:var(--gold);
 font-size:.9rem;line-height:1.5}
.jn .faq{margin:30px 0 0;border-top:1px solid var(--border)}
.jn .faq h2{margin:16px 0 4px;font:600 1rem/1.35 'Poppins',system-ui,sans-serif;color:var(--cream)}
.jn .faq p{margin:0 0 14px;font-size:.97rem;line-height:1.6;color:var(--mist)}
"""

# Picks the currency from the browser's language list (the first entry that
# names a country), then shows that currency's two amounts and points the
# Join button at that currency's Payment Link. Remembers nothing and sends
# nothing. Without JavaScript the page shows euros and the button opens the
# euro link.
JS = """<script>
(function(){
  var P = %(prices)s, C = %(countries)s;
  var sel = document.getElementById('jn-cur'), f = document.getElementById('jn-first'), m = document.getElementById('jn-month'), j = document.getElementById('jn-join');
  if (!sel || !f || !m || !j) return;
  function show(code){
    var p = P[code] || P.EUR;
    f.textContent = p[0] + p[2];
    m.textContent = p[0] + p[1];
    if (p[3]) j.setAttribute('href', p[3]);
  }
  var pick = 'EUR', langs = navigator.languages && navigator.languages.length ? navigator.languages : [navigator.language || ''];
  for (var i = 0; i < langs.length; i++) {
    var r = /[-_]([A-Za-z]{2})\\b/.exec(langs[i] || '');
    if (r) { pick = C[r[1].toUpperCase()] || 'EUR'; break; }
  }
  if (!P[pick]) pick = 'EUR';
  sel.value = pick; show(pick);
  sel.addEventListener('change', function(){ show(sel.value); });
})();
</script>"""


def inner(e) -> str:
    """The page body. `e` is landing.py's HTML-escape."""
    rows = offered()
    code0, written0, month0, first0, link0 = rows[0]
    ready = _has_link(rows[0])
    inc = "".join(f"<li>{e(x)}</li>" for x in WORDS["includes"])
    opts = "".join(f'<option value="{e(r[0])}">{e(r[0])}</option>' for r in rows)
    faq = "".join(f"<h2>{e(q)}</h2><p>{e(a)}</p>" for q, a in WORDS["faq"])
    bonus_html = ""
    if WORDS.get("bonus_heading"):
        bonus_html = (f'<div class="bonus"><h2>{e(WORDS["bonus_heading"])}</h2>'
                      f'<p>{e(WORDS["bonus"])}</p></div>')
    ph_html = "".join(f'<p class="ph">{e(v)}</p>' for v in PLACEHOLDERS.values() if v)
    if ready:
        btn = f'<a class="join" id="jn-join" href="{e(join_url(link0))}" rel="noopener">{e(BUTTON)}</a>'
        btn_note = ""
    else:
        btn = f'<a class="join" id="jn-join" aria-disabled="true">{e(BUTTON)}</a>'
        btn_note = ('<p class="ph">PLACEHOLDER: no Stripe Payment Link is set yet, so this button is '
                    'switched off. Once links are in, only the currencies that have one are offered.</p>')
    return f"""  <div class="jn">
    <div class="jn-head">
      <p class="ey">{e(WORDS['eyebrow'])}</p>
      <p class="quote">{e(WORDS['quote'])}<span class="g">{e(WORDS['quote_gold'])}</span></p>
    </div>
    <div class="jn-pay">
      <h1>{e(WORDS['heading'])}</h1>
      <div class="price">
        <div class="row"><span class="lab">{e(LABEL_FIRST)}</span><span class="first" id="jn-first">{e(_amount(written0, first0))}</span></div>
        <p class="then">{e(LABEL_THEN)} <b id="jn-month">{e(_amount(written0, month0))}</b> {e(LABEL_MONTH)}</p>
        <label class="pick"><span>{e(LABEL_PICKER)}</span><select id="jn-cur" aria-label="{e(LABEL_PICKER)}">{opts}</select></label>
        <!-- THE CHECKOUT SLOT. Today it holds the Join button, a plain link to
             the chosen currency's Payment Link. An embedded Stripe form would
             go in this div in place of the button (it needs a checkout session
             made by a server, so it is not here yet). The column is 380px wide
             on a desktop and the full width on a phone. -->
        <div class="jn-checkout" id="jn-checkout">
          {btn}
          {btn_note}
        </div>
      </div>
      {bonus_html}
    </div>
    <div class="jn-det">
      <h2 class="h2">{e(WORDS['included_heading'])}</h2>
      <ul class="inc">{inc}</ul>
      <p class="terms">{e(WORDS['terms'])}</p>
      {ph_html}
      <div class="faq">{faq}</div>
    </div>
  </div>"""


def script() -> str:
    import json
    prices = {r[0]: [r[1], r[2], r[3], join_url(r[4]) if _has_link(r) else ""] for r in offered()}
    return JS % dict(prices=json.dumps(prices, ensure_ascii=False),
                     countries=json.dumps(COUNTRY_CURRENCY))

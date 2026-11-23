"""
rw_join.py -- The Reconnected Woman: the page a woman joins from.

One job: she picks her currency, sees the price in it, and goes to Stripe.
Built by landing.py (so it is noindex, out of the sitemap, and carries the
site's own nav, footer and analytics and nothing else). No form, and nothing
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
]

# Which currency a browser's country gets by default. Anywhere not listed,
# and any currency whose link is not set yet, gets EUR.
COUNTRY_CURRENCY = {
    "AU": "AUD", "US": "USD", "GB": "GBP", "CA": "CAD",
    "NZ": "NZD", "SG": "SGD", "CH": "CHF", "LI": "CHF",
}

# ── WORDING ─────────────────────────────────────────────────────────────
# Everything in WORDS is Daniel's, lifted word for word from the Reconnected
# Woman page (reconnected-woman-v10-preview.html). Anything he has not
# written is in PLACEHOLDERS, shown on the page inside a dashed box, and the
# live site refuses to build while one is left. Set a placeholder to "" to
# drop that line from the page.
WORDS = dict(
    eyebrow="The Reconnected Woman",
    heading="Stay, and the four weeks run like this.",
    lede="Figure out what you want, ask for it, and get better results with less effort.",
    includes=[
        "Four sessions a month, each month a new theme with its own workbook",
        "An intention for your week, every week, and we keep you to it",
        "Live facilitation and hot seat work",
        "The WhatsApp group with the other women between sessions",
        "Complimentary 1:1 call on week 6",
    ],
    # His sentence on the page opens "€119 a month, and your membership price
    # is grandfathered." The amount is in the price block here, so it starts
    # at "Your membership price".
    terms="Your membership price is grandfathered. It never increases as long as you "
          "stay. Memberships roll over monthly. Cancel anytime.",
    faq=[
        ("Can I cancel?",
         "Yes, any time. It’s month to month, and your membership runs to the end of "
         "the month you’ve paid for."),
        ("What if I’m away for a month?",
         "You can pause once a year, for up to a month, and you keep your price. Ask "
         "before your next payment."),
    ],
)

PLACEHOLDERS = dict(
    # The bonus for joining straight after the open session.
    bonus="PLACEHOLDER: Daniel’s line about the bonus personal 1:1 with him for "
          "joining right away.",
)

# Plain labels and the one line about Stripe. Not sales copy.
LABEL_FIRST = "First month"
LABEL_THEN = "Then"
LABEL_MONTH = "a month"
LABEL_PICKER = "Pay in"
BUTTON = "Join"
BILLED_LINE = "You are billed in the currency you choose, the same amount every month."


def _has_link(row) -> bool:
    return row[4].startswith("https://")


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
/* LAYOUT. On a phone it stacks: heading and its one line, the payment block,
   then the details. From 900px it is two columns: payment on the LEFT (it
   stays in view while the right side scrolls), everything else on the RIGHT. */
.jn{width:100%;max-width:560px;text-align:left;display:grid;gap:26px;
 grid-template-columns:minmax(0,1fr);grid-template-areas:"head" "pay" "det"}
.jn-head{grid-area:head}.jn-pay{grid-area:pay}.jn-det{grid-area:det}
@media(min-width:900px){
 main{align-items:flex-start}
 .jn{max-width:1040px;column-gap:clamp(36px,5vw,72px);row-gap:0;
  grid-template-columns:minmax(0,380px) minmax(0,1fr);grid-template-areas:"pay head" "pay det"}
 .jn-pay{align-self:start;position:sticky;top:112px}
 .jn-det{margin-top:22px}
}
.jn .ey{margin:0 0 13px;font:800 .62rem/1.4 'Poppins',system-ui,sans-serif;letter-spacing:.24em;
 text-transform:uppercase;color:var(--gold)}
.jn h1{margin:0 0 10px;font:600 clamp(1.5rem,5.4vw,2rem)/1.22 'Poppins',system-ui,sans-serif;
 letter-spacing:-.01em;color:var(--cream);text-wrap:balance}
.jn .lede{margin:0;color:var(--mist);font-size:1rem;line-height:1.68}
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
.jn .pick{display:flex;align-items:center;gap:10px;margin:16px 0 0;font-size:.88rem;color:var(--slate)}
.jn .pick select{appearance:auto;background:var(--bg);color:var(--cream);border:1px solid var(--border);
 border-radius:2px;padding:9px 10px;font:600 .9rem/1 'Montserrat',system-ui,sans-serif;min-height:40px}
.jn .pick select:focus-visible{outline:2px solid var(--gold);outline-offset:2px}
.jn .join{display:block;width:100%;margin:20px 0 0;text-align:center;text-decoration:none;
 background:var(--coral);color:#fff;font:700 .82rem/1 'Poppins',system-ui,sans-serif;letter-spacing:.13em;
 text-transform:uppercase;padding:19px 30px;border-radius:2px;transition:background .22s ease,transform .22s ease}
.jn .join:hover,.jn .join:focus-visible{background:var(--coral-lift);transform:translateY(-2px)}
.jn .join:focus-visible{outline:2px solid var(--gold);outline-offset:3px}
.jn .join[aria-disabled=true]{background:#3A4660;color:#B1BFD7;pointer-events:none;transform:none}
.jn .billed{margin:10px 0 0;font-size:.88rem;line-height:1.55;color:var(--slate)}
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
    bonus = PLACEHOLDERS.get("bonus", "")
    bonus_html = ""
    if bonus:
        cls = "ph" if "PLACEHOLDER" in bonus else "terms"
        bonus_html = f'<p class="{cls}">{e(bonus)}</p>'
    if ready:
        btn = f'<a class="join" id="jn-join" href="{e(link0)}" rel="noopener">{e(BUTTON)}</a>'
        btn_note = ""
    else:
        btn = f'<a class="join" id="jn-join" aria-disabled="true">{e(BUTTON)}</a>'
        btn_note = ('<p class="ph">PLACEHOLDER: no Stripe Payment Link is set yet, so this button is '
                    'switched off. Once links are in, only the currencies that have one are offered.</p>')
    return f"""  <div class="jn">
    <div class="jn-head">
      <p class="ey">{e(WORDS['eyebrow'])}</p>
      <h1>{e(WORDS['heading'])}</h1>
      <p class="lede">{e(WORDS['lede'])}</p>
    </div>
    <div class="jn-pay">
      <div class="price">
        <div class="row"><span class="lab">{e(LABEL_FIRST)}</span><span class="first" id="jn-first">{e(_amount(written0, first0))}</span></div>
        <p class="then">{e(LABEL_THEN)} <b id="jn-month">{e(_amount(written0, month0))}</b> {e(LABEL_MONTH)}</p>
        <label class="pick"><span>{e(LABEL_PICKER)}</span><select id="jn-cur" aria-label="{e(LABEL_PICKER)}">{opts}</select></label>
        <p class="billed">{e(BILLED_LINE)}</p>
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
    </div>
    <div class="jn-det">
      <ul class="inc">{inc}</ul>
      <p class="terms">{e(WORDS['terms'])}</p>
      {bonus_html}
      <div class="faq">{faq}</div>
    </div>
  </div>"""


def script() -> str:
    import json
    prices = {r[0]: [r[1], r[2], r[3], r[4] if _has_link(r) else ""] for r in offered()}
    return JS % dict(prices=json.dumps(prices, ensure_ascii=False),
                     countries=json.dumps(COUNTRY_CURRENCY))

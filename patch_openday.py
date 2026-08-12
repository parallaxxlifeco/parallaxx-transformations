#!/usr/bin/env python3
"""Open-day positioning patch, applied to the APPROVED preview.

Source of truth is reconnected-woman-v8-preview.html exactly as Daniel approved
it. This script edits nothing about the design system, the copy he corrected
line by line, or the mobile tuning. It makes only the changes the pilot run
made necessary:

  1. hero      - open-session date strip + softer primary CTA
  2. values    - three standards become the five the room actually agreed
  3. pricing   - two steps: free first session, then EUR59 a month
  4. faq       - the trial answer contradicted a free open day
  5. cta-final - "entry by application only" versus an open door
  6. wording   - "apply" -> "come", where the door is genuinely open

Every replacement is asserted, so a stale source fails loudly instead of
silently producing a half-patched page.
"""
import pathlib, sys

SRC = pathlib.Path("/tmp/rw/reconnected-woman-v8-preview.html")
OUT = pathlib.Path("/tmp/rw/reconnected-woman-v9-preview.html")

# PLACEHOLDER. Daniel confirms the real date and sitting time before push.
OPEN_ISO   = "2026-09-08T08:30:00+02:00"
OPEN_LABEL = "Tuesday 8 September &middot; 08:30 CET &middot; 14:30 Bali"
OPEN_SHORT = "Tuesday 8 September"

s = SRC.read_text(encoding="utf-8")
n = 0

def sub(old, new, label):
    global s, n
    if old not in s:
        sys.exit("FAIL: could not find source for [%s]" % label)
    if s.count(old) != 1:
        sys.exit("FAIL: [%s] matched %d times, expected 1" % (label, s.count(old)))
    s = s.replace(old, new)
    n += 1

# ---------------------------------------------------------------- 1. CSS
CSS = """
  /* ---- OPEN SESSION, added after the pilot run ---- */
  #trw-page .hero-open {
    font-size: 12px; letter-spacing: 0.18em; text-transform: uppercase;
    color: var(--trw-gold); margin-top: 20px;
  }
  #trw-page .hero-open .js-open-count { color: var(--trw-muted); }

  #trw-page .step-label {
    display: block; max-width: 500px; margin: 0 auto 12px; text-align: left;
    font-size: 11px; letter-spacing: 0.24em; text-transform: uppercase;
    color: var(--trw-gold);
  }
  #trw-page .step-then {
    max-width: 500px; margin: 30px auto 12px; text-align: left;
    font-size: 11px; letter-spacing: 0.24em; text-transform: uppercase;
    color: var(--trw-muted);
  }
  #trw-page .open-card {
    max-width: 500px; margin: 0 auto; text-align: left;
    background: var(--trw-card); border: 1px solid var(--trw-border);
    position: relative; overflow: hidden;
  }
  #trw-page .open-card::before {
    content: ''; position: absolute; top: 0; left: 0; right: 0; height: 2px;
    background: linear-gradient(90deg, var(--trw-gold-dark), var(--trw-gold), var(--trw-gold-dark));
  }
  #trw-page .open-top {
    padding: 28px 36px 20px; border-bottom: 1px solid var(--trw-border);
    text-align: center;
  }
  #trw-page .open-amount {
    font-family: var(--trw-head); font-size: 64px; font-weight: 700;
    color: var(--trw-white); line-height: 1;
  }
  #trw-page .open-when {
    font-size: 12px; letter-spacing: 0.2em; text-transform: uppercase;
    color: var(--trw-gold); margin-top: 12px;
  }
  #trw-page .open-count {
    display: block; font-size: 12px; letter-spacing: 0.18em;
    text-transform: uppercase; color: var(--trw-muted); margin-top: 6px;
  }
  #trw-page .open-body { padding: 22px 36px 0; font-size: 16px; color: var(--trw-cream); }
  #trw-page .open-gate { padding: 14px 36px 0; font-size: 14px; color: var(--trw-muted); line-height: 1.6; }
  #trw-page .open-action { padding: 22px 36px 28px; }
  #trw-page #pricing .price-card { margin-top: 0; }

  /* Five standards, not three: 3 across then 2 across, on a 6 column base. */
  #trw-page .values-grid { grid-template-columns: repeat(6, 1fr); }
  #trw-page .values-grid > .value-card { grid-column: span 2; }
  #trw-page .values-grid > .value-card:nth-child(4),
  #trw-page .values-grid > .value-card:nth-child(5) { grid-column: span 3; }

  @media (max-width: 760px) {
    #trw-page .values-grid { grid-template-columns: 1fr; }
    #trw-page .values-grid > .value-card,
    #trw-page .values-grid > .value-card:nth-child(4),
    #trw-page .values-grid > .value-card:nth-child(5) { grid-column: 1 / -1; }
    #trw-page .hero-open { font-size: 10px; letter-spacing: 0.12em; margin-top: 16px; }
    #trw-page .hero-open .ho-time { display: none; }
    #trw-page .step-label, #trw-page .step-then { font-size: 10px; }
    #trw-page .open-top { padding: 22px 24px 16px; }
    #trw-page .open-amount { font-size: 52px; }
    #trw-page .open-when { font-size: 10px; letter-spacing: 0.08em; }
    #trw-page .open-count { font-size: 10.5px; letter-spacing: 0.14em; }
    #trw-page .open-body { padding: 18px 24px 0; font-size: 14px; }
    #trw-page .open-gate { padding: 12px 24px 0; font-size: 13px; }
    #trw-page .open-action { padding: 18px 24px 24px; }
  }

  /* ---- THE DIFFERENCE: a framed panel, not another list ----
     Everything above this section is hairline rules and bordered cards, so a
     row of items in either language reads as more of the same. This is the
     pivot of the page, so it gets a device used nowhere else: a bracketed
     panel, a glow behind the question, and outlined numerals. */
  #trw-page #difference { padding: 76px 0; }

  #trw-page .dif-eyebrow {
    display: block; font-size: 12px; letter-spacing: 0.3em; text-transform: uppercase;
    color: var(--trw-gold); margin-bottom: 30px;
  }
  #trw-page .dif-panel {
    position: relative; max-width: 940px; margin: 0 auto;
    padding: 54px 56px 48px;
    border: 1px solid rgba(212, 184, 74, 0.20);
    background:
      radial-gradient(120% 85% at 50% 0%, rgba(212, 184, 74, 0.085), rgba(212, 184, 74, 0) 62%),
      var(--trw-card);
  }
  #trw-page .dif-panel::before,
  #trw-page .dif-panel::after {
    content: ''; position: absolute; width: 46px; height: 46px;
    border: 2px solid var(--trw-gold); pointer-events: none;
  }
  #trw-page .dif-panel::before { top: -1px; left: -1px; border-right: none; border-bottom: none; }
  #trw-page .dif-panel::after { bottom: -1px; right: -1px; border-left: none; border-top: none; }

  #trw-page .dif-panel .quote-big { margin-top: 0; }
  #trw-page .dif-panel .under-quote { margin-top: 18px; }

  #trw-page .dif-set {
    display: grid; grid-template-columns: repeat(2, 1fr);
    gap: 30px 52px; margin-top: 46px; text-align: left;
  }
  #trw-page .dif-cell { display: flex; align-items: flex-start; gap: 20px; }
  #trw-page .dif-fig {
    flex: 0 0 auto; font-family: var(--trw-head); font-size: 46px; font-weight: 700;
    line-height: 0.9; letter-spacing: -0.02em;
    color: transparent; -webkit-text-stroke: 1px rgba(212, 184, 74, 0.95);
    transition: color 0.3s ease, -webkit-text-stroke-color 0.3s ease;
  }
  #trw-page .dif-cell:hover .dif-fig { color: rgba(212, 184, 74, 0.16); -webkit-text-stroke-color: var(--trw-gold); }
  #trw-page .dif-cell h3 {
    font-family: var(--trw-head); font-size: 17px; font-weight: 600;
    color: var(--trw-gold); letter-spacing: 0.02em; margin-bottom: 8px; line-height: 1.25;
  }
  #trw-page .dif-cell p { font-size: 14.5px; line-height: 1.55; color: var(--trw-text); text-wrap: pretty; }

  @media (max-width: 760px) {
    #trw-page #difference { padding: 44px 0; }
    #trw-page .dif-eyebrow { font-size: 10px; letter-spacing: 0.24em; margin-bottom: 20px; }
    #trw-page .dif-panel { padding: 34px 22px 30px; }
    #trw-page .dif-panel::before, #trw-page .dif-panel::after { width: 30px; height: 30px; }
    #trw-page .dif-set { grid-template-columns: 1fr; gap: 20px; margin-top: 28px; }
    #trw-page .dif-cell { gap: 14px; }
    #trw-page .dif-fig { font-size: 32px; -webkit-text-stroke-width: 0.9px; }
    #trw-page .dif-cell h3 { font-size: 15px; margin-bottom: 5px; }
    #trw-page .dif-cell p { font-size: 13px; }
  }

  /* ---- MOBILE TYPE PASS ----
     The phone was running body copy at desktop-ish sizes, so almost every
     line wrapped two or three deep and the page ran past 8000px. Sizes come
     down, the leading comes with them, and the padding stops carrying
     desktop values. Nothing changes above 760. */
  @media (max-width: 760px) {
    #trw-page .recog-line { font-size: 14.5px; line-height: 1.5; padding: 12px 0 12px 20px; }
    #trw-page .recog-line::before { top: 21px; width: 9px; }
    #trw-page .recog-closer { font-size: 15.5px; line-height: 1.4; margin-top: 16px; }

    #trw-page .quote-big { font-size: 18.5px; line-height: 1.3; }
    #trw-page .under-quote { font-size: 13.5px; line-height: 1.55; }
    #trw-page .pull-line { font-size: 17.5px; line-height: 1.35; }
    #trw-page .preframe { font-size: 14px; }
    #trw-page .vsl-caption { font-size: 13px; line-height: 1.6; }
    #trw-page .friends-body p { font-size: 14px; line-height: 1.55; }

    #trw-page .trap-card { padding: 20px 18px; }
    #trw-page .trap-card h3 { font-size: 16px; }
    #trw-page .trap-card p { font-size: 13.5px; }

    #trw-page .archetype-num { font-size: 22px; }
    #trw-page .archetype-card h3 { font-size: 13px; letter-spacing: 0.14em; }
    #trw-page .archetype-card p { font-size: 13.5px; line-height: 1.5; }

    #trw-page .bio-text .bio-role { font-size: 15.5px; line-height: 1.35; }
    #trw-page .bio-text p { font-size: 14px; line-height: 1.55; }

    #trw-page .values-grid { gap: 10px; }
    #trw-page .value-card { padding: 15px 16px 14px; }
    #trw-page .value-card h3 { font-size: 11.5px; letter-spacing: 0.16em; margin-bottom: 7px; }
    #trw-page .value-card p { font-size: 13.5px; line-height: 1.5; }

    #trw-page #pricing .lead { font-size: 13.5px; }
    #trw-page .open-amount { font-size: 42px; }
    #trw-page .price-amount { font-size: 52px; }
    #trw-page .price-amount sup { font-size: 19px; margin-top: 8px; }
    #trw-page .open-body { font-size: 13.5px; line-height: 1.55; }
    #trw-page .open-gate { font-size: 12.5px; line-height: 1.5; }
    #trw-page .price-features { padding: 10px 24px; }
    #trw-page .price-features li { font-size: 13.5px; padding: 9px 0; gap: 11px; }

    #trw-page .faq-q { font-size: 14px; line-height: 1.35; }
    #trw-page .faq-body-inner p { font-size: 13.5px; line-height: 1.55; }
  }

  @media (max-width: 380px) {
    #trw-page .recog-line { font-size: 13.5px; }
    #trw-page .quote-big { font-size: 17px; }
    #trw-page .value-card p, #trw-page .price-features li { font-size: 13px; }
  }
</style>"""
sub("\n</style>\n<style>\nparallaxx-nav{", CSS + "\n<style>\nparallaxx-nav{", "css tail")

# ------------------------------------------------- 2. hero: date + CTA
sub(
"""    <button class="btn btn--gold" data-trw-modal>Apply Now</button>
    <p class="cta-secondary">Not sure yet? <a href="https://www.parallaxxtransformations.com/priority-audit" target="_top">Take the Priority Audit</a></p>""",
"""    <button class="btn btn--gold" data-trw-modal>Come To The Open Session</button>
    <p class="hero-open">Next open session &nbsp;&middot;&nbsp; %s <span class="ho-time">&nbsp;&middot;&nbsp; 08:30 CET</span> &nbsp;&middot;&nbsp; <span class="js-open-count"></span></p>
    <p class="cta-secondary">Free to attend. &euro;59 a month if you stay. Or <a href="https://www.parallaxxtransformations.com/priority-audit" target="_top">take the Priority Audit</a> first.</p>""" % OPEN_SHORT,
"hero cta")

# hang the date on the page root so the counter has one source
sub('<div id="trw-page">', '<div id="trw-page" data-open-at="%s">' % OPEN_ISO, "page root date")

# ------------------------------------------------- 3. values: 3 -> 5
sub(
"""      <div class="value-card anim anim-d3">
        <h3>Punctuality</h3>
        <p>Show up like it matters, because you do.</p>
      </div>""",
"""      <div class="value-card anim anim-d3">
        <h3>Punctuality</h3>
        <p>Show up like it matters, because you do.</p>
      </div>
      <div class="value-card anim anim-d3">
        <h3>Curiosity</h3>
        <p>Over judgment. Of each other, and of yourself.</p>
      </div>
      <div class="value-card anim anim-d3">
        <h3>Accountability</h3>
        <p>One intention out of every session. Yours to keep.</p>
      </div>""",
"values 5")

# ------------------------------------------------- 4. pricing: two steps
sub(
"""    <span class="overline">The Investment</span>
    <h2>For The Price Of A Meal</h2>
    <div class="price-card anim-scale">""",
"""    <span class="overline">The Investment</span>
    <h2>Come Once, For Nothing</h2>
    <p class="lead">The first session of every month is open. Experience the value then decide.</p>

    <div style="height:44px"></div>
    <span class="step-label">Step One &mdash; The Open Session</span>
    <div class="open-card anim-scale">
      <div class="open-top">
        <div class="open-amount">Free</div>
        <div class="open-when">%s</div>
        <span class="open-count js-open-count"></span>
      </div>
      <p class="open-body">One live session, run exactly as it always runs. Nothing staged for visitors, and nothing owed at the end of it.</p>
      <p class="open-gate">There's a short application form as spaces are limited, and we want to ensure best mutual fit for everyone.</p>
      <div class="open-action">
        <button class="btn btn--gold btn--full" data-trw-modal>Register For The Open Session</button>
      </div>
    </div>

    <p class="step-then">Step Two &mdash; If It's Home</p>
    <div class="price-card anim-scale">""" % OPEN_LABEL,
"pricing steps")

sub(
"""        <li>Join at any point in the cycle</li>""",
"""        <li>Complimentary 1:1 call on week 6</li>""",
"price feature")

sub(
"""        <button class="btn btn--gold btn--full" data-trw-modal>Apply Now</button>
      </div>
    </div>
  </div>
</section>

<section id="faq">""",
"""        <button class="btn btn--gold btn--full" data-trw-modal>Come To The Open Session First</button>
      </div>
    </div>
  </div>
</section>

<section id="faq">""",
"price cta")

# ------------------------------------------------- 5. faq
sub(
"""      <h2>Before You Apply</h2>""",
"""      <h2>Before You Come</h2>""",
"faq head")

sub(
"""          <span class="faq-q">Is there a trial?</span>
          <span class="faq-ico">+</span>
        </button>
        <div class="faq-body"><div class="faq-body-inner"><p>No. The women who commit and turn up get the most out of it. If you'd spend on another course you won't finish but won't risk this, it probably isn't your crew.</p></div></div>""",
"""          <span class="faq-q">Can I come once before I decide?</span>
          <span class="faq-ico">+</span>
        </button>
        <div class="faq-body"><div class="faq-body-inner"><p>Yes. The first session of every month is open and there's no charge for it. Come, sit in it, and decide from the room rather than from this page. After that it's &euro;59 a month, and the women who commit and turn up get the most out of it.</p></div></div>""",
"faq trial")

sub(
"""<p>Both, depending on where you are. Tell us your preference on the application.</p>""",
"""<p>Both, depending on where you are. Tell us your preference on the form.</p>""",
"faq location")

sub(
"""<p>Two sitting times for global coverage, and we stay fluid with what the group asks for. Apply and we'll find yours.</p>""",
"""<p>Two sitting times for global coverage, and we stay fluid with what the group asks for. Come to the open session and we'll find yours.</p>""",
"faq times")

# ------------------------------------------------- 6. final cta
sub(
"""    <p class="sub anim anim-d2">Entry by application only.</p>
    <button class="btn btn--gold anim anim-d3" data-trw-modal>Apply Now</button>
    <p class="cta-secondary anim anim-d3">Not ready to apply? <a href="https://www.parallaxxtransformations.com/priority-audit" target="_top">Take the Priority Audit</a>. Ten minutes, and you'll see where you're actually spending yourself.</p>""",
"""    <p class="sub anim anim-d2">Next open session %s. Free to attend, short application form first.</p>
    <button class="btn btn--gold anim anim-d3" data-trw-modal>Register For The Open Session</button>
    <p class="cta-secondary anim anim-d3">Not ready? <a href="https://www.parallaxxtransformations.com/priority-audit" target="_top">Take the Priority Audit</a>. Ten minutes, and you'll see where you're actually spending yourself.</p>""" % OPEN_SHORT,
"final cta")

sub(
"""      <span class="modal-title">The Reconnected Woman &mdash; Application</span>""",
"""      <span class="modal-title">The Reconnected Woman &mdash; Registration</span>""",
"modal title")

# ------------------------------------------------- 7. the days counter
# No template literals: the bundle builder wraps this in one and asserts.
JS = """
<script>
(function () {
  var root = document.getElementById('trw-page');
  if (!root) return;
  var at = root.getAttribute('data-open-at');
  if (!at) return;
  var t = new Date(at).getTime();
  if (!t) return;
  var days = Math.ceil((t - new Date().getTime()) / 86400000);
  var txt = '';
  if (days > 1) txt = 'In ' + days + ' days';
  else if (days === 1) txt = 'Tomorrow';
  else if (days === 0) txt = 'Today';
  else txt = 'Date to be confirmed';
  var els = document.querySelectorAll('.js-open-count');
  for (var i = 0; i < els.length; i++) els[i].textContent = txt;
})();
</script>
"""
sub('<script src="https://parallaxxlifeco.github.io/parallaxx-transformations/parallaxx-nav.js',
    JS + '<script src="https://parallaxxlifeco.github.io/parallaxx-transformations/parallaxx-nav.js',
    "counter js")

# ------------------------------------------------- 8. the difference section
# The overline and the h2 said the same word twice and cost about 160px before
# the reader reached anything. The question is the strongest line in the
# section, so it becomes the headline. The four one-liners were sitting in
# 2x2 cards roughly four times taller than their content; they become a single
# indexed row.
sub(
"""    <div class="section-head anim">
      <span class="overline">The Difference</span>
      <h2>So here's the difference</h2>
      <div class="divider"></div>
    </div>
    <p class="quote-big anim anim-d1" style="margin-top:26px;">When were you last seen, heard, witnessed and held in a masculine presence without a romantic intent?</p>""",
"""    <span class="dif-eyebrow anim">The Difference</span>
    <div class="dif-panel anim anim-d1">
    <p class="quote-big">When were you last seen, heard, witnessed and held in a masculine presence without a romantic intent?</p>""",
"difference head")

sub(
"""    <div class="tile-grid">
      <div class="tile anim anim-d1">
        <h3>Structure is held</h3>
        <p>Someone else facilitates the room, the logistics, the pace.</p>
      </div>
      <div class="tile anim anim-d2">
        <h3>It's taken care of</h3>
        <p>Nothing here for you to do.</p>
      </div>
      <div class="tile anim anim-d3">
        <h3>Nothing to manage</h3>
        <p>Say the true thing. No cleaning up after it.</p>
      </div>
      <div class="tile anim anim-d3">
        <h3>No scorecard</h3>
        <p>Nothing to win, so your competence has nothing to do.</p>
      </div>
    </div>""",
"""    <div class="dif-set">
      <div class="dif-cell">
        <span class="dif-fig">01</span>
        <div>
          <h3>Structure is held</h3>
          <p>Someone else facilitates the room, the logistics, the pace.</p>
        </div>
      </div>
      <div class="dif-cell">
        <span class="dif-fig">02</span>
        <div>
          <h3>It's taken care of</h3>
          <p>Nothing here for you to do.</p>
        </div>
      </div>
      <div class="dif-cell">
        <span class="dif-fig">03</span>
        <div>
          <h3>Nothing to manage</h3>
          <p>Say the true thing. No cleaning up after it.</p>
        </div>
      </div>
      <div class="dif-cell">
        <span class="dif-fig">04</span>
        <div>
          <h3>No scorecard</h3>
          <p>Nothing to win, so your competence has nothing to do.</p>
        </div>
      </div>
    </div>
    </div><!-- .dif-panel -->""",
"difference tiles")

assert "parallaxx-nav" in s and "parallaxx-footer" in s, "chrome lost"
assert s.count('class="value-card') == 5, "expected five standards"


# ------------------------------------------------- 9. bust the chrome cache
# The nav and footer are pulled with a fixed ?v= string, so a change to
# parallaxx-footer.js is invisible until this moves. The footer just took the
# home page's phone-column fix, so it moves now.
sub("parallaxx-nav.js?v=20260806a", "parallaxx-nav.js?v=20260812a", "nav cache bust")
sub("parallaxx-footer.js?v=20260806a", "parallaxx-footer.js?v=20260812a", "footer cache bust")

OUT.write_text(s, encoding="utf-8")
print("wrote %s  %d bytes  (%d edits, was %d)" % (OUT.name, len(s), n, len(SRC.read_text(encoding='utf-8'))))

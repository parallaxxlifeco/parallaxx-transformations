#!/usr/bin/env python3
"""Build the v8 preview from the live embed source.

Reads the byte-for-byte live capture, keeps its <style>, <script> and modal
untouched, and swaps the body sections for the v8 copy. Writes a standalone
preview file. Does NOT touch src/, because build-embed-chrome.py fingerprints
that against the live page and a mismatch there fails the chrome build.
"""
import re, pathlib

SRC = pathlib.Path("/mnt/user-data/uploads/Parallaxx Transformations Redesign/_repo-push-chrome/src/reconnected-woman-wix-inject.html")
OUT = pathlib.Path("/tmp/rw/reconnected-woman-v8-preview.html")

html = SRC.read_text(encoding="utf-8")

# ---------------------------------------------------------------- extra CSS
EXTRA_CSS = """
  /* ===== v8 additions ===== */
  #trw-page #recognition { background: var(--trw-black); text-align: center; padding: 88px 0; }
  #trw-page #trap        { background: var(--trw-dark);  text-align: center; padding: 58px 0;
                           border-top: 1px solid var(--trw-border); border-bottom: 1px solid var(--trw-border); }
  #trw-page #friends     { background: var(--trw-black); text-align: center; padding: 88px 0; }
  #trw-page #difference  { background: var(--trw-dark);  text-align: center; padding: 88px 0;
                           border-top: 1px solid var(--trw-border); border-bottom: 1px solid var(--trw-border); }
  #trw-page #recognition .section-head,
  #trw-page #trap .section-head,
  #trw-page #friends .section-head,
  #trw-page #difference .section-head { text-align: center; margin-bottom: 40px; }
  #trw-page #trap .section-head { margin-bottom: 22px; }
  #trw-page #recognition h2,
  #trw-page #trap h2,
  #trw-page #friends h2,
  #trw-page #difference h2 { font-size: clamp(26px, 3.5vw, 40px); line-height: 1.15; }
  #trw-page #recognition .recog-list { text-align: left; }

  #trw-page .preframe {
    font-family: var(--trw-body); font-size: 17px; font-weight: 300;
    color: var(--trw-cream); line-height: 1.6; text-align: center;
    max-width: 720px; margin: 0 auto;
  }
  #trw-page .vsl-caption {
    font-family: var(--trw-body); font-size: 16px; font-weight: 300; font-style: italic;
    color: var(--trw-text); line-height: 1.7; text-align: center;
    max-width: 760px; margin: 34px auto 0; border-left: 2px solid var(--trw-gold);
    padding-left: 22px; text-align: left;
  }

  #trw-page .recog-list {
    max-width: 1000px; margin: 44px auto 0;
    display: grid; grid-template-columns: 1fr 1fr;
    column-gap: 48px; row-gap: 0; align-items: stretch;
  }
  #trw-page .recog-line {
    font-family: var(--trw-body); font-size: 20px; font-weight: 300;
    color: var(--trw-cream); line-height: 1.55;
    padding: 20px 0 20px 30px; border-bottom: 1px solid var(--trw-border);
    position: relative;
  }
  #trw-page .recog-line::before {
    content: ''; position: absolute; left: 0; top: 30px;
    width: 14px; height: 1px; background: var(--trw-gold);
  }
  #trw-page .recog-line:nth-last-child(-n+2) { border-bottom: none; }
  #trw-page .recog-closer {
    margin-top: 40px; text-align: center;
    font-family: var(--trw-head); font-size: 22px; font-weight: 500;
    color: var(--trw-white); line-height: 1.5;
  }

  #trw-page .trap-grid {
    display: grid; grid-template-columns: 1fr 1fr; gap: 18px;
    margin-top: 26px; max-width: 900px; margin-left: auto; margin-right: auto;
  }
  #trw-page .trap-card {
    background: var(--trw-card); border: 1px solid var(--trw-border);
    padding: 20px 24px; text-align: center;
  }
  #trw-page .trap-card h3 {
    font-family: var(--trw-head); font-size: 19px; font-weight: 600;
    color: var(--trw-white); margin-bottom: 6px; line-height: 1.3;
  }
  #trw-page .trap-card p {
    font-family: var(--trw-body); font-size: 15px; font-weight: 300;
    color: var(--trw-text); line-height: 1.5;
  }
  #trw-page #trap .pull-line { margin-top: 28px; font-size: 24px; }
  #trw-page .pull-line {
    margin-top: 44px; text-align: center;
    font-family: var(--trw-head); font-size: 28px; font-weight: 600;
    color: var(--trw-gold); line-height: 1.3;
  }

  #trw-page .chip-row {
    display: flex; flex-wrap: wrap; justify-content: center; gap: 12px;
    margin-top: 40px;
  }
  #trw-page .chip {
    font-family: var(--trw-body); font-size: 12px; font-weight: 600;
    letter-spacing: 0.14em; text-transform: uppercase;
    color: var(--trw-cream); border: 1px solid var(--trw-border);
    background: var(--trw-card); padding: 11px 18px;
  }

  #trw-page .tile-grid {
    display: grid; grid-template-columns: repeat(2, 1fr); gap: 20px;
    margin-top: 44px;
  }
  #trw-page .tile {
    border: 1px solid var(--trw-border); background: var(--trw-card);
    padding: 26px 24px; position: relative; overflow: hidden;
  }
  #trw-page .tile::after {
    content: ''; position: absolute; bottom: 0; left: 0; right: 0;
    height: 2px; background: var(--trw-gold);
  }
  #trw-page .tile h3 {
    font-family: var(--trw-head); font-size: 17px; font-weight: 600;
    color: var(--trw-gold); margin-bottom: 10px; letter-spacing: 0.02em;
  }
  #trw-page .tile p {
    font-family: var(--trw-body); font-size: 15px; font-weight: 300;
    color: var(--trw-text); line-height: 1.6;
  }

  #trw-page .quote-big {
    font-family: var(--trw-head); font-size: 30px; font-weight: 300;
    color: var(--trw-white); line-height: 1.4; text-align: center;
    max-width: 860px; margin: 0 auto;
  }
  #trw-page .under-quote {
    font-family: var(--trw-body); font-size: 17px; font-weight: 300;
    color: var(--trw-text); line-height: 1.7; text-align: center;
    max-width: 760px; margin: 28px auto 0;
  }
  #trw-page .friends-body {
    max-width: 720px; margin: 40px auto 0; text-align: center;
  }
  #trw-page .friends-body p {
    font-family: var(--trw-body); font-size: 18px; font-weight: 300;
    color: var(--trw-cream); line-height: 1.7; margin-bottom: 18px;
  }
  #trw-page .bio-text .bio-role {
    font-family: var(--trw-head); font-size: 21px; font-weight: 500;
    letter-spacing: 0; text-transform: none; color: var(--trw-white);
    line-height: 1.4; margin-bottom: 20px; display: block;
  }
  #trw-page .cta-secondary {
    margin-top: 26px; font-family: var(--trw-body); font-size: 14px;
    font-weight: 300; color: var(--trw-text);
  }
  #trw-page .cta-secondary a { color: var(--trw-gold); text-decoration: none; border-bottom: 1px solid rgba(212,184,74,0.4); }

  /* Give the wide one-line blocks room so each sentence holds a single line. */
  #trw-page .hero-tagline { max-width: 860px; margin-bottom: 34px; }
  #trw-page #distinction .under-quote { max-width: 900px; }
  #trw-page #friends .container { max-width: 1080px; }
  #trw-page .friends-body { max-width: 1000px; }
  #trw-page .friends-body p { margin-bottom: 12px; }
  #trw-page #cta-final h2 { max-width: 900px; margin-left: auto; margin-right: auto; }

  /* Tighter vertical rhythm across the page. */
  #trw-page section { padding: 58px 0; }
  #trw-page #recognition, #trw-page #friends, #trw-page #difference { padding: 62px 0; }
  #trw-page .section-head { margin-bottom: 28px; }
  #trw-page #vsl .section-head { margin-bottom: 22px; }
  #trw-page .recog-list { margin-top: 28px; }
  #trw-page .recog-closer { margin-top: 26px; }
  #trw-page .chip-row { margin-top: 26px; }
  #trw-page .tile-grid { margin-top: 30px; }
  #trw-page .friends-body { margin-top: 24px; }
  #trw-page #friends .pull-line { margin-top: 30px; }
  #trw-page #difference .under-quote { margin-top: 20px; }

  #trw-page .trw-mt { margin-top: 30px; }
  @media (max-width: 760px) { #trw-page .trw-mt { margin-top: 20px; } }

  /* trap heading sits on one line */
  #trw-page #trap h2 { font-size: clamp(22px, 2.6vw, 32px); max-width: none; }

  /* No orphans. Balance headings and short blocks, avoid single-word last lines
     in body copy. Chrome and Safari honour both; older engines just ignore them
     and fall back to normal wrapping. */
  #trw-page h1,
  #trw-page h2,
  #trw-page h3,
  #trw-page .hero-tagline,
  #trw-page .pull-line,
  #trw-page .recog-closer,
  #trw-page .quote-big,
  #trw-page .archetype-label,
  #trw-page .bio-role,
  #trw-page .position-box p,
  #trw-page .price-note,
  #trw-page #cta-final .sub { text-wrap: balance; }

  #trw-page .recog-line,
  #trw-page .preframe,
  #trw-page .under-quote,
  #trw-page .vsl-caption,
  #trw-page .friends-body p,
  #trw-page .tile p,
  #trw-page .trap-card p,
  #trw-page .value-card p,
  #trw-page .archetype-card p,
  #trw-page .bio-text p,
  #trw-page .cta-secondary,
  #trw-page .faq-body-inner p,
  #trw-page .price-features li { text-wrap: pretty; }

  @media (max-width: 760px) {
    /* My base rules sit after the page's own media block, so mobile spacing has
       to be restated here or the desktop values win. */
    #trw-page section { padding: 44px 0; }
    #trw-page #recognition, #trw-page #trap,
    #trw-page #friends, #trw-page #difference { padding: 44px 0; }
    #trw-page #hero { padding: 74px 20px 52px; }
    #trw-page .section-head { margin-bottom: 20px; }
    #trw-page .recog-list { margin-top: 16px; }
    #trw-page .recog-closer { margin-top: 20px; }
    #trw-page .chip-row { margin-top: 20px; gap: 8px; }
    #trw-page .chip { font-size: 11px; padding: 9px 13px; letter-spacing: 0.1em; }
    #trw-page .tile-grid { margin-top: 22px; }
    #trw-page .trap-grid { margin-top: 20px; }
    #trw-page .friends-body { margin-top: 18px; }
    #trw-page #friends .pull-line,
    #trw-page #trap .pull-line { margin-top: 22px; }
    #trw-page #difference .under-quote { margin-top: 16px; }
    #trw-page .hero-tagline { max-width: 340px; margin-bottom: 28px; }
    #trw-page .cta-secondary { margin-top: 16px; }

    /* 1. hero foot: the rule and the strip were carrying desktop margins */
    #trw-page #hero { padding: 74px 20px 38px; }
    #trw-page .hero-rule { margin-top: 26px; padding-top: 20px; }

    /* 2. five chips onto two rows */
    #trw-page .chip-row { gap: 6px; }
    #trw-page .chip { font-size: 9px; padding: 7px 9px; letter-spacing: 0.04em; }

    /* 3. adjacent sections were stacking two full paddings */
    #trw-page section { padding: 36px 0; }
    #trw-page #recognition, #trw-page #trap,
    #trw-page #friends, #trw-page #difference { padding: 36px 0; }
    #trw-page #hero { padding: 74px 20px 38px; }

    /* 4. four credential tags onto two rows */
    #trw-page .bio-text .tags { gap: 6px; }
    #trw-page .bio-text .tag { font-size: 9px; padding: 6px 9px; letter-spacing: 0.03em; }

    /* 5. friends headline holds one line */
    #trw-page #friends h2 { font-size: 19px; }

    /* the two paddings plus the page's own #distinction rule were stacking */
    #trw-page #distinction { padding: 36px 0 30px; }
    #trw-page #friends { padding: 30px 0 36px; }
    #trw-page .archetype-grid { margin-bottom: 0; }
    #trw-page #recognition h2, #trw-page #trap h2,
    #trw-page #friends h2, #trw-page #difference h2 { font-size: 22px; line-height: 1.2; }
    #trw-page .trap-grid { grid-template-columns: 1fr; gap: 16px; }
    #trw-page .tile-grid { grid-template-columns: 1fr; gap: 14px; }
    #trw-page .recog-list { grid-template-columns: 1fr; column-gap: 0; max-width: 560px; }
    #trw-page .recog-line { font-size: 16px; padding: 16px 0 16px 24px; }
    #trw-page .recog-line:nth-last-child(-n+2) { border-bottom: 1px solid var(--trw-border); }
    #trw-page .recog-line:last-child { border-bottom: none; }
    #trw-page .recog-line::before { top: 25px; width: 10px; }
    #trw-page .recog-closer { font-size: 17px; }
    #trw-page .quote-big { font-size: 21px; }
    #trw-page .under-quote { font-size: 15px; }
    #trw-page .pull-line { font-size: 20px; }
    #trw-page .preframe { font-size: 15px; }
    #trw-page .vsl-caption { font-size: 14px; }
    #trw-page .friends-body p { font-size: 15px; }
    #trw-page .trap-card { padding: 26px 20px; }
    #trw-page .trap-card h3 { font-size: 18px; }
    #trw-page .bio-text .bio-role { font-size: 17px; }
  }

  /* Small phones. The block above is tuned for ~390; these hold the same line
     counts down at 360 and below. */
  @media (max-width: 380px) {
    #trw-page #friends h2 { font-size: 17px; }
    #trw-page .chip { font-size: 8.5px; padding: 7px 8px; letter-spacing: 0.03em; }
    #trw-page .bio-text .tag { font-size: 8.5px; padding: 6px 8px; letter-spacing: 0.02em; }
    #trw-page .recog-line { font-size: 15px; }
  }
"""

# Wix wraps this fragment in a bare document with a charset meta and nothing
# else, so with no viewport meta the embed lays out at 980px on a phone and the
# @media (max-width:760px) block never fires. Browsers honour a viewport meta
# wherever it appears, so it goes at the top of the fragment.
VIEWPORT = '<meta name="viewport" content="width=device-width, initial-scale=1">\n'
html = VIEWPORT + html

html = html.replace("</style>", EXTRA_CSS + "\n</style>", 1)

# ------------------------------------------------------------------- body
def grab_div(text, start_marker):
    """Return the full <div ...>...</div> block that starts at start_marker."""
    a = text.index(start_marker)
    i, depth = a, 0
    for m in re.finditer(r'<div\b|</div>', text[a:]):
        depth += 1 if m.group(0) == '<div' else -1
        if depth == 0:
            return text[a:a + m.end()]
    raise ValueError("unbalanced div for " + start_marker)

vsl_video = grab_div(html, '<div class="video-wrap video-wrap--landscape')
bio_video = grab_div(html, '<div class="bio-img-wrap anim-left">')

BODY = """<section id="hero">
  <div class="hero-inner">
    <h1>The<br><span class="accent">Reconnected</span><br>Woman</h1>
    <p class="hero-tagline">You've competed with men. Led men. Carried men.<br><strong>The masculine is provided. You don't have to, for a change.</strong></p>
    <button class="btn btn--gold" data-trw-modal>Apply Now</button>
    <p class="cta-secondary">Not sure yet? <a href="https://www.parallaxxtransformations.com/priority-audit" target="_top">Take the Priority Audit</a></p>
    <p class="hero-rule">Real Integrity &nbsp;&middot;&nbsp; Deep Self-Trust &nbsp;&middot;&nbsp; True Connection</p>
  </div>
</section>


<section id="vsl">
  <div class="container">
    <div class="section-head anim">
      <span class="overline">Watch This First</span>
      <div class="divider"></div>
    </div>
    <p class="preframe anim anim-d1" style="margin-top:0;">Nobody here is going to teach you how to be a woman.</p>
    __VSL_VIDEO__
    <p class="vsl-caption anim anim-d2">"I've got no interest in you becoming more feminine, or more spiritual, or more of anything. I want to see you being more of you."</p>
  </div>
</section>


<section id="recognition">
  <div class="container">
    <div class="section-head anim">
      <span class="overline">Sounds Like You?</span>
      <div class="divider"></div>
    </div>
    <div class="recog-list">
      <p class="recog-line anim">You said yes again this week. There was no room for it.</p>
      <p class="recog-line anim">You're the one everyone talks to. Nobody asks about you.</p>
      <p class="recog-line anim">You hit the target. The target moves.</p>
      <p class="recog-line anim">You cancelled on someone who matters. Again.</p>
      <p class="recog-line anim">You're holding it together for more people than you'd admit to.</p>
      <p class="recog-line anim">You look at the men around you and not one of them is carrying anything for you.</p>
    </div>
    <p class="recog-closer anim">You're winning. You're delivering.<br>And you're the only one who feels what it costs.</p>
  </div>
</section>


<section id="trap">
  <div class="container">
    <div class="section-head anim">
      <span class="overline">The Trap</span>
      <h2>You've had two options. Neither works.</h2>
      <div class="divider"></div>
    </div>
    <div class="trap-grid">
      <div class="trap-card anim anim-d1">
        <h3>&ldquo;Slow down. Do less.&rdquo;</h3>
        <p>Like being asked to stop being you.</p>
      </div>
      <div class="trap-card anim anim-d2">
        <h3>&ldquo;Push harder.&rdquo;</h3>
        <p>You're already at full capacity.</p>
      </div>
    </div>
    <p class="pull-line anim anim-d3">So this is about doing different.</p>
  </div>
</section>


<section id="distinction">
  <div class="container-wide">
    <div class="section-head anim">
      <span class="overline">Be Clear On What This Is</span>
      <h2>What This Isn't</h2>
      <div class="divider"></div>
    </div>
    <div class="chip-row anim anim-d1">
      <span class="chip">No sage</span>
      <span class="chip">No palo santo</span>
      <span class="chip">No goddess circle</span>
      <span class="chip">No womb wisdom</span>
      <span class="chip">No priestess</span>
    </div>
    <p class="under-quote anim anim-d2" style="margin-top:24px;">Nobody's asking you to soften or surrender.<br>This is somewhere your competence has nothing to do.</p>
    <div class="archetype-grid trw-mt">
      <div class="archetype-card anim anim-d1">
        <div class="archetype-num">01</div>
        <div class="archetype-body">
          <h3 class="archetype-label">Not A Women's Circle</h3>
          <p>No performance of it.</p>
        </div>
      </div>
      <div class="archetype-card anim anim-d2">
        <div class="archetype-num">02</div>
        <div class="archetype-body">
          <h3 class="archetype-label">Not A Sisterhood</h3>
          <p>No loyalty pact, no comfort without change.</p>
        </div>
      </div>
      <div class="archetype-card anim anim-d3">
        <div class="archetype-num">03</div>
        <div class="archetype-body">
          <h3 class="archetype-label">Not A Coaching Program</h3>
          <p>Except the coaching you give yourself.</p>
        </div>
      </div>
    </div>
  </div>
</section>


<section id="friends">
  <div class="container">
    <div class="section-head anim">
      <span class="overline">Friends And Peers</span>
      <h2>Your friends can't do this</h2>
      <div class="divider"></div>
    </div>
    <div class="friends-body">
      <p class="anim anim-d1">Friendship runs on co-regulation. You leave feeling better and nothing has changed.</p>
      <p class="anim anim-d2">Put yourself in a room of women exactly like you and you'll find a way to help. You always do.</p>
    </div>
    <p class="pull-line anim anim-d3">Every other room like this one is run by someone exactly like you.</p>
  </div>
</section>


<section id="difference">
  <div class="container-wide">
    <div class="section-head anim">
      <span class="overline">The Difference</span>
      <h2>So here's the difference</h2>
      <div class="divider"></div>
    </div>
    <p class="quote-big anim anim-d1" style="margin-top:26px;">When were you last seen, heard, witnessed and held in a masculine presence without a romantic intent?</p>
    <p class="under-quote anim anim-d2">You've been over-functioning your masculinity to make up for the masculine you didn't get from the men in your world. Put it down for a change.</p>
    <div class="tile-grid">
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
    </div>
  </div>
</section>


<!-- WHAT CHANGES: hidden until the pilot returns real outcomes.
<section id="outcome">
  <div class="container">
    <div class="section-head anim">
      <span class="overline">What Changes</span>
      <h2>You already have the integrity.<br>It points outward.</h2>
      <div class="divider"></div>
    </div>
    <p class="under-quote anim anim-d1">Our work here is turning it inward. Same standard, pointed at you.</p>
  </div>
</section>
-->


<section id="bio">
  <div class="container-wide">
    <div class="bio-grid">
      __BIO_VIDEO__
      <div class="bio-text anim-right">
        <span class="overline">Who's Running It</span>
        <h2>Daniel Lawson</h2>
        <span class="bio-role">I don't know what it's like to be a woman. I'm not one.</span>
        <p>I do know what it's like to be obsessed with productivity and to compete for success.</p>
        <p>Business development, tech company, Australia. I hit my target and it cost me my soul. The next year the number went up another 10%.</p>
        <p>I resigned. Then I lost my sense of identity.</p>
        <p><strong>I got out. And I understand the codes.</strong></p>
        <div class="tags">
          <span class="tag">ICG Accredited</span>
          <span class="tag">6 Years Coaching</span>
          <span class="tag">Global Facilitator</span>
          <span class="tag">Relational Connection System&trade;</span>
        </div>
      </div>
    </div>
  </div>
</section>


<!-- VOICES: hidden until quotes are in.
<section id="voices">
  <div class="container-wide">
    <div class="section-head anim">
      <span class="overline">Proof</span>
      <h2>From women already in the work</h2>
      <div class="divider"></div>
    </div>
  </div>
</section>
-->


<section id="values">
  <div class="container-wide">
    <div class="section-head anim">
      <span class="overline">What We Stand For</span>
      <h2>The Standard Here</h2>
      <div class="divider"></div>
    </div>
    <div class="values-grid">
      <div class="value-card anim anim-d1">
        <h3>Your Space</h3>
        <p>Not for the women. Not to contribute.</p>
      </div>
      <div class="value-card anim anim-d2">
        <h3>Your Truth</h3>
        <p>That's the contribution. Performance is at the door.</p>
      </div>
      <div class="value-card anim anim-d3">
        <h3>Punctuality</h3>
        <p>Show up like it matters, because you do.</p>
      </div>
    </div>
  </div>
</section>


<section id="pricing">
  <div class="container">
    <span class="overline">The Investment</span>
    <h2>For The Price Of A Meal</h2>
    <div class="price-card anim-scale">
      <div class="price-top">
        <div class="price-amount"><sup>&euro;</sup>59</div>
        <div class="price-note">Per Month &nbsp;&middot;&nbsp; Cancel Anytime</div>
      </div>
      <ul class="price-features">
        <li>One live session a week, in four-week cycles</li>
        <li>Live facilitation and hot seat work</li>
        <li>Access to the group between sessions</li>
        <li>First access to new frameworks and resources</li>
        <li>Join at any point in the cycle</li>
      </ul>
      <div class="price-action">
        <button class="btn btn--gold btn--full" data-trw-modal>Apply Now</button>
      </div>
    </div>
  </div>
</section>

__FAQ__

<section id="cta-final">
  <div class="container">
    <span class="overline anim">Ready?</span>
    <h2 class="anim anim-d1">Come back to you.</h2>
    <p class="sub anim anim-d2">Entry by application only.</p>
    <button class="btn btn--gold anim anim-d3" data-trw-modal>Apply Now</button>
    <p class="cta-secondary anim anim-d3">Not ready to apply? <a href="https://www.parallaxxtransformations.com/priority-audit" target="_top">Take the Priority Audit</a>. Ten minutes, and you'll see where you're actually spending yourself.</p>
  </div>
</section>
"""

# ------------------------------------------------------------------- FAQ
FAQ = [
    ("Isn't this just another women's circle?",
     "No. Most are built around becoming more feminine, and there's a performance in that. Here we call it as it is, so you can put something down instead of picking more up."),
    ("Why is a man hosting it?",
     "Because someone has to run it, and if it were another woman like you, you'd find a way to help inside ten minutes. Nothing to prove, nobody to be careful with. I've got the room."),
    ("I have great friends. Do I need this?",
     "Friendship runs on co-regulation and the women you'd go to are running your operating system. I'm not here to be your friend."),
    ("Is there a trial?",
     "No. The women who commit and turn up get the most out of it. If you'd spend on another course you won't finish but won't risk this, it probably isn't your crew."),
    ("Online or in person?",
     "Both, depending on where you are. Tell us your preference on the application."),
    ("Do I need to attend every session?",
     "No. But if you're already planning around not being there, it may not be the right fit."),
    ("When do sessions run?",
     "Two sitting times for global coverage, and we stay fluid with what the group asks for. Apply and we'll find yours."),
    ("What does the fee include?",
     "Facilitation, hot seat work, resources, and the people you'll meet. It's largely a filter."),
    ("Are there upsells coming?",
     "No. There's a deeper path through 1:1 work in the Reconnect Program if you ever want it, and your time here comes off the cost."),
]

items = "\n".join(
    f"""      <div class="faq-item anim">
        <button class="faq-btn" type="button">
          <span class="faq-q">{q}</span>
          <span class="faq-ico">+</span>
        </button>
        <div class="faq-body"><div class="faq-body-inner"><p>{a}</p></div></div>
      </div>""" for q, a in FAQ)

faq_section = f"""<section id="faq">
  <div class="container-wide">
    <div class="section-head anim">
      <span class="overline">Common Questions</span>
      <h2>Before You Apply</h2>
      <div class="divider"></div>
    </div>
    <div class="faq-wrap">
{items}
    </div>
  </div>
</section>"""

BODY = (BODY.replace("__VSL_VIDEO__", vsl_video)
            .replace("__BIO_VIDEO__", bio_video)
            .replace("__FAQ__", faq_section))

start = html.index('<section id="hero">')
end = html.index('</section>', html.index('<section id="cta-final">')) + len('</section>')
html = html[:start] + BODY + html[end:]


# ---------------------------------------------------------------- chrome
# Same steps build-embed-chrome.py applies, replicated here because that script
# fingerprints src/ against the live page and refuses to run on anything else.
# Keep these in sync with build-embed-chrome.py if it changes.
PAGES_BASE    = "https://parallaxxlifeco.github.io/parallaxx-transformations/"
PAGES_VERSION = "20260806a"
HERO_PAD      = "118px 28px 72px"
HOST_CSS = """
parallaxx-nav{display:block;position:relative;z-index:200}
parallaxx-footer{display:block;position:relative;z-index:2;text-align:left}
"""
SHIM = """
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

# 1. the fixed brand chip is exactly what the nav replaces
html, n = re.subn(r'<a class="trw-brand".*?</a>\s*', '', html, count=1, flags=re.S)
assert n == 1, "brand chip not found"

# 2. nav first inside the page root, footer after the last section
html = html.replace('<div id="trw-page">',
                    '<div id="trw-page">\n<parallaxx-nav active="women"></parallaxx-nav>\n', 1)
i = html.rfind('</section>') + len('</section>')
html = html[:i] + "\n<parallaxx-footer></parallaxx-footer>\n" + html[i:]

# 3. hero clears the fixed bar
html, n = re.subn(r'(#hero\s*\{[^}]*?padding:\s*)72px 28px', r'\g<1>' + HERO_PAD,
                  html, count=1, flags=re.S)
if not n:
    print("  warn: hero padding unchanged, check it clears the nav")

# 4. host css after the page stylesheet
j = html.find('</style>')
html = html[:j] + '</style>\n<style>' + HOST_CSS + '</style>' + html[j + len('</style>'):]

# 5. the chrome, then the shim
html = html.rstrip() + (
    "\n\n<!-- PARALLAXX CHROME: loaded from GitHub Pages, same host the rest of the\n"
    "     site uses. Rebuild the bundles and bump ?v= to update. -->\n"
    f'<script src="{PAGES_BASE}parallaxx-nav.js?v={PAGES_VERSION}"></script>\n'
    f'<script src="{PAGES_BASE}parallaxx-footer.js?v={PAGES_VERSION}"></script>\n'
    "<script>" + SHIM + "</script>\n")

OUT.write_text(html, encoding="utf-8")
print("wrote", OUT, len(html), "bytes  nav+footer: external")

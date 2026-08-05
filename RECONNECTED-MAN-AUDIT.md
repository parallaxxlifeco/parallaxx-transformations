# The Reconnected Man → Parallaxx v4
## Alignment audit + rebuild notes

**Baseline audited:** the live page at `parallaxxtransformations.com/the-reconnected-man`, captured 1 Aug 2026.
**Target system:** `Parallaxx Home Men.dc.html` + `PtNav.dc.html` + `PtFooter.dc.html` (the v4 "Everything Is Glass" redesign).
**Deliverable:** this audit, plus a rebuilt `The Reconnected Man.dc.html`.

---

## 0. Two things to know before the design notes

**The live page isn't the file in your folder.** `The Reconnected Man.dc.html` in the redesign folder stops dead at the testimonials section — no facilitator, no FAQ, no close, no form. The page actually serving is the older `reconnected-man-wix-inject.html` build. I audited and rebuilt against what's live.

**The live page is inside an iframe.** It's deployed as a Wix *HTML embed*, so the entire page renders inside a 1436 × 891px frame with its own scrollbar. The parent document's `scrollHeight` is 903px — it doesn't scroll at all. Every word of copy, every testimonial, every FAQ answer sits on a `filesusr.com` origin that Google does not attribute to your URL.

The page also runs this in its page code:

```js
$w.onReady(function () { $w('#header1').collapse(); $w('#footer1').collapse(); });
```

So the Parallaxx header and footer are switched off, and the embed supplies its own **GIVE IT ALL** nav instead. A man who lands on this page from an ad has no Parallaxx navigation, no footer, and no route into the rest of the site. The new home page avoids all of this by shipping as a Wix **Custom Element** (`<parallaxx-home-men>` + `parallaxx-home-men.js`) that renders inline at true document height with PtNav and PtFooter placed as siblings.

**This is the single highest-value change on the list, and it's a deployment change, not a design one.**

---

## 1. Brand elements

### 1.1 The accent rule — the big one

v4 assigns the two accents to two *speakers*, and the live page violates it on every button:

> **Gold `#E8C65F` — Daniel's voice.** Everything he says. Handwriting, pull-quotes, section hairlines, emphasis inside his prose.
> **Coral `#FF501F` — the reader.** His words, his actions, his moves. Buttons, links, controls, active states.
> *"Colour is a scarcity currency, and every coral word on the page devalues the coral BUTTON."*

The live page uses gold for **everything**: hero CTA, pricing CTA, nav pill, play buttons, list bullets, card top-rules, FAQ icons, star ratings, section labels. Nothing is coral. The result is a page where the eye can't find the one thing it's supposed to do, and where Daniel's voice and the reader's move are indistinguishable.

| Element | Live | v4 |
|---|---|---|
| Primary CTA | `#E8C65F` gold pill, navy text, pulsing | `#FF501F` coral pill, white text, no pulse |
| CTA hover | `translateY(-2px)` + gold glow | `#FF6A3D` + `translateY(-2px)` |
| Play control | gold SVG ring, centred | coral disc, **bottom-left** |
| List bullets / dividers | gold `—` | coral `—` |
| Card top rule | gold gradient | gold *or* coral by meaning — the price card is coral (it's the reader's move), the "who this is for" cards are bronze |
| Pull-quote | cream italic, no rule | gold, 2px gold left rule, handwritten `Daniel` cite |
| Eyebrow label | gold `.3em` uppercase | `#5E6B85` on navy, `#A08A5E` bronze on cream |

Also retired: `ptmPulse`, the infinite gold ring animation on the hero CTA. Nothing in v4 pulses — the system earns attention with contrast and motion-on-reveal, not with a heartbeat.

### 1.2 Cream doesn't exist on the live page

v4 alternates navy against cream so the page has a horizon line:

> *"the page now alternates properly: navy panes → cream fork → navy system → cream Daniel."* Never two creams adjacent; never three navies without a cream break.

The live page is **nine navy sections back to back** (`#04122A` / `#061938` / `#0D2350`). It reads as one continuous slab and the eye has nothing to rest on. The rebuild alternates: navy hero → navy VSL → **cream** who-this-is-for → navy values → **cream** investment → navy proof → **cream** Daniel → navy FAQ → **cream** close.

And the companion rule: **gold has no contrast on cream.** Bronze `#A08A5E` is the cream-side equivalent — same voice, legible. Every gold element that moved onto a cream section became bronze.

### 1.3 Typography — the roles are inverted

| | Live | v4 |
|---|---|---|
| Display face | Montserrat **800** | Poppins **300 / 400 / 500** (`.px-serif`) |
| Body face | Poppins 300 | Montserrat 400/500 |
| Handwriting | *absent* | Lumios Marker → Permanent Marker (`.px-hand`) |
| Hero size | `clamp(52px, 10vw, 116px)`, three stacked words | `clamp(38px, 5.6vw, 74px)`, two-line sentence |
| Heading case | Title Case | sentence case |
| Second line | — | italic 300 at `.66em`, muted |

The 116px Montserrat-800 hero is GIA's voice, not Parallaxx's. v4's H1 is a sentence with a roman first line and an italic-300 second line — quieter, and it lets the copy do the work. The design note in the source: *"Poppins at 300 goes weak and spindly at 60px, so the display weight comes UP to 400/500 and the tracking goes slightly negative only at large sizes."*

The handwriting face is a whole layer of Daniel's presence that the live page simply doesn't have. It's the system's signature and its absence is the most obvious tell that the page is from a different era.

### 1.4 Nav and footer

The live embed's nav is a GIVE IT ALL wordmark with a gold `G` badge and a gold "Apply Now" pill, linking mostly to `giveitallevent.com`. It's a Give It All page wearing a Parallaxx URL.

v4's answer to the family relationship is more precise: PtNav is fully Parallaxx (logo asset, coral CTA pill), and GIA appears **once**, in the footer, as a gold family card. *"GIA uses a gold pill here — same shape, different colour. That is the whole family/identity trick."* The rebuild drops the embedded nav entirely and defers to PtNav with `active="experiences"`.

### 1.5 Smaller tokens now matched

- Radius ladder: `999px` pills · `20px` cards · `18px` doors/darkbox/reels · `16px` video · `14px` panes · `12px` pills
- Hairlines: `rgba(232,198,95,.14)` on navy, `rgba(160,138,94,.5)` gradient rules on cream
- Section padding: `clamp(52px, 6.5vw, 92px)` with the `<560px` override
- Containers: `.px-wrap` 1240px, `.px-head` `min(1140px, 94vw)` — **px not `ch`**, because *"'ch' is measured against the BODY font size (~9px per char)… a 54px display headline needs ~1000px"*
- `::selection { background:#FF501F; color:#fff }`

---

## 2. Features

| Feature | Home (v4) | Live RM | In the rebuild |
|---|---|---|---|
| Kinetic line reveals (`.px-line`) | ✅ GSAP + ScrollTrigger | ❌ | ✅ |
| Fade-up reveals (`.px-fade`) | ✅ | ⚠️ CSS `ptmUp` on hero only | ✅ |
| Lenis smooth scroll | ✅ | ❌ | ✅ |
| Above-fold anti-clip fix | ✅ | n/a | ✅ |
| `prefers-reduced-motion` full fallback | ✅ | ⚠️ partial | ✅ |
| Click-to-load video facade | ✅ zero requests until click | ❌ `preload="metadata"` fetches bytes on load | ✅ |
| Runtime chip on video | ✅ always | ❌ | ✅ (values need confirming) |
| Play control bottom-left | ✅ *"a 62px centred button lands squarely on his MOUTH"* | ❌ centred, gold | ✅ |
| Testimonials as real text | ✅ `#px-voices` | ❌ flattened PNGs | ⚠️ **kit in place, needs transcription** |
| Two-door fork (`.px-door`) | class kit, unused | ❌ | ✅ RM → Reconnected Woman / Reconnect 1:1 |
| Credentials strip | ✅ | ❌ (prose only) | ✅ as chips |
| FAQ accordion | ❌ | ✅ | ✅ re-skinned |
| Application modal + GHL form | ❌ | ✅ | ✅ re-skinned |
| Screenshot lightbox | ❌ | ✅ | ✅ re-skinned |
| `sc-if` editor toggles | ❌ | ✅ | ✅ kept (pricing + bonus) |
| Renders as custom element | ✅ | ❌ iframe embed | ✅ (deploy step) |

Two features you already had that Home doesn't — the FAQ accordion and the GHL application modal — are genuinely good and I kept both, re-skinned onto v4 tokens. The `sc-if` pricing/bonus toggles are the same: a smart pattern, worth keeping.

**Not present anywhere in the system, and I didn't invent them:** exit-intent, sticky mobile CTA bar, countdown timer, carousel. If you want any of those they're net-new with no house pattern to copy.

---

## 3. Copy

The copy is in decent shape. It obeys most of the house rules already — no exclamation marks, agency-preserving, never framing women as the problem. Five things to change:

**1. Title Case → sentence case.** House rule throughout. "An Initiation For Men Who Are Intentionally Becoming" → "An initiation for men *who are intentionally becoming.*" Same for "What We Value", "Sounds Like You?", "The Brotherhood Is Waiting."

**2. Eyebrows are generic labels, not narrative.** "Social Proof", "Bonus Gift", "Who This Is For", "The Investment" describe the *section*. v4 eyebrows describe the *story*: `01. Watch this first`, `02. Who this is for`, `04. People who did it`, `05. Before you apply` — with handwritten eyebrows on the emotional beats (`what we stand for`, `and now me.`, `a note about this circle`). Numbered labels on prose sections, handwriting on emotional ones.

**3. Daniel's bio is third person.** The whole point of the v4 Daniel section is that he stops being described and starts talking — the eyebrow is literally *"and now me."* Rewrote to first person: "I've been coaching personal connection and relationships for six years…"

**4. "tens of dozens of graduates."** This one I'd change regardless. It's an unusual construction that reads as inflation, and the house rule is explicit: *"Modest and true over dramatic and vague. Calibrate outcomes down."* Replaced with "has taken graduates through the full arc, and hundreds more through retreats and facilitations worldwide" — same claim, no arithmetic the reader has to squint at. **Give me the real number and I'll put it back.**

**5. No qualifier in the hero.** Home's hero states who it's for in four words — "Married. Years in. Still care about her." RM's hero never says the price, the format, or that it's application-gated until far down the page. Added a `.px-label` line under the sub-head: `€59 a month · Application only · Online & in person`. It filters, and it removes the "how much?" tab-out.

Everything else — the crisis quote, the three "who this is for" statements, the values, all six FAQ answers, "you're joining a living conversation" — is carried over verbatim.

---

## 4. Section map: live → rebuilt

| # | Live | Rebuilt | Background |
|---|---|---|---|
| 01 | Hero (GIA nav + 116px stack) | Hero — Poppins two-line, coral CTA, qualifier line | `#04122A` navy |
| 02 | VSL "Watch This First" | `01. Watch this first` — facade player | `#0A1D3C` navy |
| 03 | Crisis quote (own section) | folded into 02 as a gold pull-quote | — |
| 04 | Who This Is For | `02. Who this is for` + handwriting rule + darkbox | **`#F1ECE1` cream** |
| 05 | Entry Requirements (own section) | folded into 05 as the qualifier above the price | — |
| 06 | What We Value | `what we stand for` — three glass panes | `#04122A` navy |
| 07 | Pricing + Bonus | `03. The investment` — coral-ruled price card, bonus as a cream card | **`#F7F3EA` cream** |
| 08 | Testimonials | `04. People who did it` — two reels + screenshot masonry | `#0A1D3C` navy |
| 09 | Facilitated By Daniel | `and now me.` — sticky reel, first-person prose, credential chips, ghost CTA | **`#F7F3EA` cream** |
| 10 | FAQ | `05. Before you apply` | `#04122A` navy |
| 11 | Closing + final CTA | `a note about this circle` + close + **two-door fork** | **`#F1ECE1` cream** |
| — | *(GIA nav / no footer)* | PtNav `active="experiences"` + PtFooter | — |

Sections went from 9 to 9, but three merges and one split gave the page a rhythm instead of a list. Ending on cream means PtFooter's navy CTA block lands as a change of key rather than more of the same — exactly how Home resolves.

---

## 5. What's left to do

Marked with `▸` in the rebuilt file.

1. **Transcribe the WhatsApp screenshots into real text.** Biggest remaining win. The `#px-voices` / `.px-face` / `.px-byline` kit is already in the file's stylesheet. The Home source is blunt about why: *"Google reads NONE of it, a screen reader gets nothing… Every one of these quotes was invisible to search."* Keep the screenshots as secondary verification if you like the texture, but the words need to be text.
2. **Upload `Lumios Marker` as `.woff2`** to Wix Media and replace `LUMIOS_MARKER_WOFF2_URL`. Same placeholder exists on Home — it's a site-wide gap, not an RM one. Until it's set, everything falls to Permanent Marker.
3. **Hero photograph.** The rebuild ships the gradient-only fallback, which holds up. `hero-daniel-behind-glass.jpg` is the obvious candidate — upload and drop in behind the veil.
4. **Confirm video runtimes** for the three `.len` chips. I put `3 min` / `1 min` / `90 sec` as placeholders.
5. **Deploy as a custom element** — `parallaxx-reconnected-man.js`, tag `parallaxx-reconnected-man`, site header/footer OFF, PtNav + PtFooter placed as siblings. Bump the `?v=` query. Full instructions are in a comment at the bottom of the file.
6. **Set SEO in Wix page settings**, not in the component — the system handles it there. Suggested title/description are in the same comment block.
7. **Confirm two slugs** I linked in the fork: `/about-daniel-lawson` and `/reconnect`.

---

## Sources

- [The Reconnected Man — live page](https://www.parallaxxtransformations.com/the-reconnected-man)
- [The deployed embed source](https://www-parallaxxtransformations-com.filesusr.com/html/111174_6905def14065216df2e4cbaed4764a26.html)
- `Parallaxx Home Men.dc.html`, `PtNav.dc.html`, `PtFooter.dc.html`, `reconnected-man-wix-inject.html` — Parallaxx Transformations Redesign folder

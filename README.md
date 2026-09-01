# parallaxx-transformations

Website for Parallaxx Transformations (sister site to Give It All).

Every page is authored as a `.dc.html` component and compiled into a
self-contained Wix Custom Element. **The `.dc.html` is the source of record.**
Never hand-edit a generated `.js` bundle; edit the source and rerun its build.

| Page | Source | Build | Bundle / tag | Preview |
|---|---|---|---|---|
| Home, the front door | `Parallaxx Home.dc.html` | `build-home-bundle.py` | `parallaxx-home.js` · `parallaxx-home` | `home.html` |
| Home, men | `Parallaxx Home Men.dc.html` | `build-home-men-bundle.py` | `parallaxx-home-men.js` · `parallaxx-home-men` | `index.html` |
| The Reconnected Man | `The Reconnected Man.dc.html` | `build-reconnected-man-bundle.py` | `parallaxx-reconnected-man.js` · `parallaxx-reconnected-man` | `reconnected-man.html` |
| Home, women | `Parallaxx Home Women.dc.html` | `build-home-women-bundle.py` | `parallaxx-home-women.js` · `parallaxx-home-women` | `home-women.html` |
| The Reconnected Woman | `reconnected-woman-v9-preview.html` | `build_bundle_v9.py` | `parallaxx-reconnected-woman.js` · `parallaxx-reconnected-woman` | `reconnected-woman.html` |
| The Priority Audit | `Priority Audit.dc.html` | `build-priority-audit-bundle.py` | `parallaxx-priority-audit.js` · `parallaxx-priority-audit` | `priority-audit.html` |
| Contact | `Parallaxx Contact v4.dc.html` | `build-contact-bundle.py` | `parallaxx-contact.js` · `parallaxx-contact` | `contact.html` |
| Privacy Policy | `Parallaxx Legal.dc.html` | `build-legal-bundles.py` | `parallaxx-privacy.js` · `parallaxx-privacy` | `privacy.html` |
| Terms of Use | `Parallaxx Legal.dc.html` | `build-legal-bundles.py` | `parallaxx-terms.js` · `parallaxx-terms` | `terms.html` |
| Speaking & Facilitating | `Parallaxx Speaking.dc.html` | `build-speaking-bundle.py` | `parallaxx-speaking.js` · `parallaxx-speaking` | `speaking.html` |
| As Seen In | `Parallaxx As Seen In.dc.html` | `build-as-seen-in-bundle.py` | `parallaxx-as-seen-in.js` · `parallaxx-as-seen-in` | `as-seen-in.html` |
| Identity 2.0 Challenge | `Parallaxx Identity 2.0.dc.html` | `build-identity-bundle.py` | `parallaxx-identity.js` · `parallaxx-identity` | `identity.html` |

## The Source URLs

Everything is served by **GitHub Pages** off `main`. This was not written down
anywhere until now, which cost an afternoon: the only host named in the repo was
a jsDelivr example in `wheel-of-reconnect-README.md`, which serves the same files
from a different cache and would silently drift out of sync on the next push.
**GitHub Pages is the one to use. Do not mix the two.**

Base: `https://parallaxxlifeco.github.io/parallaxx-transformations/`

| Wix Custom Element | Source URL | Tag |
|---|---|---|
| Home, the front door | `…/parallaxx-home.js` | `parallaxx-home` |
| Home, men | `…/parallaxx-home-men.js` | `parallaxx-home-men` |
| The Reconnected Man | `…/parallaxx-reconnected-man.js` | `parallaxx-reconnected-man` |
| Home, women | `…/parallaxx-home-women.js` | `parallaxx-home-women` |
| The Reconnected Woman | `…/parallaxx-reconnected-woman.js` | `parallaxx-reconnected-woman` |
| The Priority Audit | `…/parallaxx-priority-audit.js` | `parallaxx-priority-audit` |
| Contact | `…/parallaxx-contact.js` | `parallaxx-contact` |
| Privacy Policy | `…/parallaxx-privacy.js` | `parallaxx-privacy` |
| Terms of Use | `…/parallaxx-terms.js` | `parallaxx-terms` |
| Speaking & Facilitating | `…/parallaxx-speaking.js` | `parallaxx-speaking` |
| As Seen In | `…/parallaxx-as-seen-in.js` | `parallaxx-as-seen-in` |
| Identity 2.0 Challenge | `…/parallaxx-identity.js` | `parallaxx-identity` |

The preview harnesses render as real pages at the same base, so
`…/home.html` is the front door as Wix will show it, without touching Wix.

Pages rebuilds within a minute or so of a push and its CDN holds a file for
about ten minutes. If a deploy looks stale, bump the `?v=` query and hard
reload before assuming the build is wrong.

Also here: `parallaxx-wheel-of-reconnect.js`, a standalone interactive element,
and `support.js`, the local shim that lets a `.dc.html` open in a browser.

## Build

```
python3 build-home-bundle.py
python3 build-home-men-bundle.py
python3 build-reconnected-man-bundle.py
python3 build-home-women-bundle.py
python3 build_bundle_v9.py
python3 build-priority-audit-bundle.py
python3 build-contact-bundle.py
python3 build-legal-bundles.py     # builds BOTH legal pages
python3 build-speaking-bundle.py   # add --ship to block on empty image slots
python3 build-as-seen-in-bundle.py
python3 build-identity-bundle.py
```

All four refuse to build rather than ship a bundle that fails silently in a
shadow root. `build-home-bundle.py` adds one more refusal of its own: it will
not build while either image on the home page is still a placeholder, because
a broken portrait above the fold on the site's strongest URL is worse than no
deploy at all. See the docstring in `build-home-men-bundle.py` for why the step
exists at all, and the one in `build-home-women-bundle.py` for why that page
needed a build of its own.

## Deploy

In the Wix editor, place a Custom Element widget with the Source URL and Tag
from the table above. Bump the `?v=` query in the preview harness on every
deploy so the CDN and browser caches let go.

Header and footer differ by page. The men's home page and The Reconnected Man
carry their own chrome, so the site Header and Footer are turned **off** for
those.

The women's home page carries its own nav and its own footer, so site Header
and Footer are both **off** for it too. Neither strip would load its element in
Wix, so both are built into the page. That leaves two copies of each, and it is
worth knowing: the copies inside `Parallaxx Home Women.dc.html` will not track
`PtNav v3.dc.html` or `PtFooter v3.dc.html`. Change one and the other does not
move. If the strips start working, delete the built-in blocks and go back to
placing the elements.

`PtNav v3.dc.html` and `PtFooter v3.dc.html` are both in the repo as the
sources of record. Nothing builds or deploys them from here yet.

SEO is set in Wix page settings, not in the component.

## Home, the front door

The routing page at `/`. It supersedes `Parallaxx Home Sort.dc.html`, which was
120 words and two buttons sitting on the strongest URL on the domain.

Its one job is to get the right person to `/men` or `/women` in under fifteen
seconds and give them a reason to trust Daniel on the way past. It sells
nothing: no price, no application, and neither instrument, because the
archetype quiz and the Priority Audit are avatar-specific by construction and
neither survives being asked before a door is chosen.

**Its build is deliberately lighter than the other three.** No GSAP and no
Lenis, so `boot()` runs immediately rather than waiting on two CDN round trips,
and nothing on the page depends on an animation completing. A page whose entire
purpose is routing cannot lose its headline to a stranded tween, which is what
happened twice on the men's page. `build-home-bundle.py` fails the build if
GSAP ever appears in the source.

**Two images need Wix Media URLs before it will build.** The hero portrait
(`daniel-clear.jpg`) and the full-bleed plate behind the record
(`home-plate-room.jpg`). Both are placeholders in the source until uploaded.

The footer is built into this page too, so site Header and Footer are both
**off** for it. Same caveat as the women's page: that copy will not track
`PtFooter v3.dc.html`.

## Home, women

The women's avatar page. Same v4 system as the men's, different construction:
it is assembled from parts rather than authored as one Design Code component,
so it ships three stylesheets and two scripts where the men's ships two and
one. Hence its own build.

`build-home-women-bundle.py` refuses to build rather than ship a bundle whose
Priority Audit is still bound to the document. That failure is silent inside a
shadow root: the page would render perfectly while its only instrument was
dead. It also escapes backslashes before embedding the CSS, because a CSS
codepoint escape reads as an octal escape inside a template literal and takes
the whole file with it.

Three shadow-DOM traps are already paid for here, and all three were silent.

Every in-page anchor is driven by script rather than by the browser. `href="#id"`
is resolved against the document, and deployed the whole page sits inside a
shadow root where the document has no such id, so the hero button did nothing
at all on the live site while working perfectly in the preview. No error, no
warning. Anything that adds an in-page link has to keep going through that
handler.

A click inside a shadow root is retargeted by the time it reaches the
document, so `nav.contains(e.target)` is false even for a click on the element
itself. The nav's outside-click handler used that and closed the mobile menu
in the same tick the burger opened it. `composedPath()` reports the real path
and works in both runtimes.

And nested `backdrop-filter` does not survive: the mobile menu panel filters
against an already filtered backdrop and the page reads through a background
that is 98.5 percent opaque. That panel is solid now.

The Priority Audit runs **in the page**, not on `/priority-audit`. The first
of the fifteen statements is live in the intro, so answering it starts the run
in place. That single tap is the whole activation cost, and spending it on a
page load was the largest leak in the funnel. `Priority Audit.dc.html` is the standalone,
and as of 14 Aug it no longer diverges: see below.

## The Reconnected Woman, and why its source is not a .dc.html

This page is the exception to the rule at the top of this file. Its source of
record is `reconnected-woman-v9-preview.html`, a plain page, and
`build_bundle_v9.py` publishes it **as-is** into the light DOM rather than
compiling it into a shadow root. That is deliberate: the page's CSS is scoped
to `#trw-page` and its script uses `document.querySelector` throughout, so a
shadow root would need every selector re-pointed, and a port is where details
get lost. `The Reconnected Woman.dc.html` is the older chain and is superseded.

Edit the preview file. It IS the page.

**The apply CTAs open a LeadConnector form in a modal, not a new tab.** All
four of them — the hero, both pricing cards and the closing block — carry
`data-trw-modal` and open the same dialog. The form ID appears three times in
that markup: `src` is what loads, and `id="form-<ID>"` plus `data-form-id` are
what GHL's `form_embed.js` matches on when it posts a height back. Miss either
of the last two on a swap and the right form loads at the wrong height and
never resizes.

One thing in there is load-bearing and looks like it should not be.
`form_embed.js` parks its iframe offscreen — `left:-9999px`, hidden, zero
opacity, all as inline styles — until it decides the form is ready, and it
never un-parks a form inside an element that started `display:none`. The form
loaded fine and sat 9999px to the left of a box that measured 76px tall: a
header with nothing under it. `unparkForm()` undoes that on open and twice
more on a timer, because the script re-applies the parking if it initialises
after the first click. Do not remove it.

## The Priority Audit, and which copy is the real one

The instrument exists twice, and that is deliberate rather than an accident
waiting to be tidied. It runs **in** the women's home page, where the first
statement is live in the intro so a single tap starts the run in place, and it
runs as a standalone at `/priority-audit`, which is where the footer's For
Women column points and where anything outside the funnel can link.

**The in-page version on the women's home page is the source of truth for the
copy.** The standalone had been left behind and carried a bug its own comment
had flagged and not fixed: the "what is feeding it" paragraph for boundaries
plus emotions described the cost coming out of her side, which is the *needs*
mechanism, so a woman scoring boundaries then emotions read an explanation of a
pillar she had not scored. The women's page had already been corrected, with
the emotions paragraph written. Both entries now match it exactly, and all six
ordered pairs were checked rather than the two that changed.

The standalone also picked up the live-first-statement mechanic in the same
pass, so the start button is gone from both. Two things stay different on
purpose:

- **The skin.** In the page every screen is `on-cream`, because it is embedded
  in a cream page and 73 rules exist to make it disappear into its host. The
  standalone keeps the navy and cream alternation the rest of the site uses. A
  standalone page has no host to blend into.
- **The second pillar's name.** The standalone prints it as a heading under
  "What is feeding it"; the in-page version does not, and since neither
  version's copy opens by naming that pillar, the in-page block currently runs
  unnamed. That is a gap on the women's page, not a feature of it.

**Site Header and Footer go OFF for this page, same as every other row.**
That changed on 14 August. This bundle used to ship no chrome at all, so the
Wix header and footer had to stay on to give the page a way out of itself.
PtNav v3 and PtFooter v3 are baked in now, ported from The Reconnected Man so
the footer carries the phone-column treatment rather than an older copy of
itself. Leave the Wix chrome on and the page renders two navs and two footers.

The nav works out where it is from the URL rather than from a prop, and its
table already maps `/priority-audit` to the women's door, so For Women lights
up with nothing to configure.

`priority-audit-preview.html` is generated by the build and is a different
thing again: a standalone page with its own minimal header, for reading the
instrument without Wix in the way. `priority-audit.html` is the harness that
shows what Wix will actually render.

## The Reconnected Man

Rebuilt onto the v4 system from the older Give It All-skinned page.
`RECONNECTED-MAN-AUDIT.md` records what changed and why, and lists the work
still open, the largest being that the testimonial screenshots are still
flattened PNGs and need transcribing into real text.

## Contact

The most linked page on the site: the coral pill in the nav on every page, the
footer utility row, and 24 links in all. Every one of them 301'd to the home
page until 24 August.

**There is no form, and that is the decision rather than an omission.** The
page this replaces, `Parallaxx Contact.dc.html`, carried one that called
`preventDefault()`, threw all four fields away and redirected to a booking
page. It never sent anything, on Wix or anywhere. A direct `mailto` to
**daniel@parallaxxtransformations.com** cannot silently swallow an enquiry and
there is nothing to maintain. `build-contact-bundle.py` fails the build on a
`<form>` element, so one cannot come back without somebody deciding, out loud,
where the submissions go. A LeadConnector embed can be added later and should
sit beside the address rather than replace it.

The old file was also on the **Give It All skin** — `#08090F`, `#E6C463`,
Archivo, a custom cursor and a film-grain overlay — which is why this is a
rebuild rather than a build script over the existing source. It is moved to
`_to_delete/` so nobody builds the wrong one. `Parallaxx Speaker.dc.html` was
in the same state and has gone the same way — superseded by
`Parallaxx Speaking.dc.html`.

**Its build loads no libraries**, for the same reason the front door's does
not. The page exists to hand over an address, and an address waiting on two
CDN round trips is an address that can fail to arrive. Every reveal is a CSS
keyframe on a delay, so `boot()` runs on the tick the element connects. The
build fails if GSAP or Lenis is ever loaded or called in the source.

PtNav v3 and PtFooter v3 are baked in, so site Header and Footer go **off**,
same as every other row in the table. The nav's path table already maps
`/contact-daniel-lawson` to `contact`, so the pill lights up with nothing to
configure — which also means the active state looks wrong when you open
`contact.html` directly, and correct at the real path.

`migration/build-site.py` carries the route and its `<head>`. This is the one
route whose metadata is not the harvested Wix copy: Wix promised "Schedule a
call today" and there is no call to schedule here. The URL is unchanged, so
the link equity is kept either way.

**Rebuilt as a card, 25 Aug.** The first version led with the email address
at headline size beside a tall portrait, under the headline "Write to me." It
was loud, and loud is the wrong register for the page somebody opens once they
have already decided to make contact. It is now a business card: identity
left, details right, a hairline where the fold would be, and **four channels
at one weight** -- the copy says "your preferred channel", so ranking them
would argue with the sentence they sit under. That is also what removed the
coral arrow that made the first version shout. Colour is almost absent: gold
labels, cream values, and coral only on the hover underline.

The portrait is `daniel-lawson.jpg` (the archive's "Daniel Lawson Presence"),
square, because a square crop is what a card wants. **It is 300px and takes
its own half of the card**, not the 112px thumbnail a printed business card
would use: somebody on this page is deciding whether to approach a person, and
a person the size of a favicon does not help them do that. On a phone it drops
back to 96px inline with the name, because a full-width square there is 350px
tall and pushes all four contact details below the fold — the exact opposite
of what a page called Contact is for. The previous one --
`daniel-conversation.jpg` -- is still in `wix-assets/` and in the asset map,
unused.

The lede is Daniel's own words, used as written.

It carries its own share card, `img/og-contact.jpg`, generated from
`migration/og-contact-card.html` the same way the rest of the set was: render
that file at 1200x630 at 2x and downsample to 1200x630. Keep the source rather
than only the image, so the card can be regenerated when the address or the
byline changes. Note it is not in `asset-map.json` and does not need to be —
that map exists to repoint Wix CDN URLs, and this file never lived on Wix. It
reaches `dist/assets/` because the whole of `wix-assets/` is copied.

The portrait is `daniel-conversation.jpg` from the Wix archive, referenced by
its **Wix CDN URL** in the source so `migration/build-site.py` can rewrite it
to `/assets/`. Change that URL by hand and the deployed page ships a broken
portrait while the preview looks perfect. The archive's other portraits are
the home page hero, which is Daniel behind glass and deliberately
unreachable, and one with his arms folded — both the wrong posture for the
page that says he is reachable.

## The two legal pages, and why they share a source

`Parallaxx Legal.dc.html` is one file holding both documents, and
`build-legal-bundles.py` slices it on the two `<section>` ids to emit
`parallaxx-privacy.js` and `parallaxx-terms.js`. **Editing either page means
editing that file and rerunning the build, which rebuilds both.**

Everything about the two is identical except their words: same chrome, same
header block, same 68ch measure, same closing block. Authored as two
`.dc.html` files they would share a stylesheet by copy, and the first fix to
one would silently stop applying to the other. That is not hypothetical — it
is exactly what `parallaxx-footer.js` is doing right now, where the committed
bundle is ahead of `PtFooter v3.dc.html` and its own build reverts it.

The cost is that each bundle ships the full stylesheet including the rules
only the other document uses. A few hundred bytes per page, against a
guarantee the two pages cannot drift. Take the trade.

**That was true until 1 September 2026, and is now true of the Terms only.**
The Privacy Policy has four sections that were written rather than harvested —
see below. Everything that came off Wix is still unchanged; nothing harvested
was rewritten. What changed is the typesetting: Wix's export flattened
its lists into loose paragraphs, so the collection types, the usage purposes,
the sharing cases and the six GDPR rights are lists again. Nothing was added,
removed or rephrased — nobody here is the lawyer. The build fails if either
document loses its `Last updated` line or its governing-entity line, because a
legal page that has quietly lost its date is worse than one that is out of
date.

They sit on cream rather than navy, which is the one deliberate departure.
These are the only two pages on the site somebody reads top to bottom instead
of scanning, and dark type on cream at 1.75 leading is the setting for that.
Navy brackets them, header and closing block, so the alternation still holds.

Both stay **indexable**. Meta and Google fetch the privacy policy during an ad
account review, and a `noindex` on one is a flag rather than a tidy-up.

### What the copy does not cover

Worth knowing before the next ad review, and none of it is ours to write:

- **No cookies or analytics section.** The policy names "Usage Information"
  but never says cookies, pixels or analytics. Meta's and Google's reviews
  both look for that language specifically.
- **No processors named.** Nothing about GoHighLevel/LeadConnector, Teachable,
  Stripe, Google or the hosting, all of which handle personal data today.
- **No retention period**, and no address or process for a data request beyond
  the email address the closing block adds.
- **"ACN 66 631 353 752" is eleven digits.** An ACN is nine; that number is
  the shape of an ABN. Carried across verbatim because changing a company
  identifier is not a typesetting decision.
- **Dated 13 June 2023**, and it predates every funnel currently running.

## Speaking & Facilitating, and its four image slots

**This is a credibility page, not a sales page,** and the difference is
structural. Daniel's two live doors are the men's and women's avatars; an
event organiser is a third buyer he is not currently chasing. So the page runs
no sales arc — no urgency, no offer stack, no price, and one quiet address at
the end instead of the gold ENQUIRE NOW pill the old page closed on, which was
the loudest thing on a page nobody had asked to be sold on.

The proof is other people's words. Three organiser briefs, verbatim, set as
the largest type after the headline. The headline itself — *Strangers arrive.
Friends leave.* — is a client's brief, not a claim about himself.

`/facilitating` redirects here rather than getting a page of its own. Same
offer described a second way, and splitting thin material across two URLs
makes both worse.

### The slots

`build-speaking-bundle.py` has a `--ship` mode, and this is why. **The page it
replaces pointed its hero at `assets/stage-3.jpg` and a second section at
`assets/connecting.jpg`. Neither file has ever existed in this repo.** It
shipped a broken image above the fold and stayed that way, because nothing
anywhere failed loudly about it — a missing `<img>` renders as a gap, and a
gap looks like design.

So photographs are declared. Four `IMAGE_SLOT_*` tokens, each with its brief
in the `SLOTS` table in the build script:

| Slot | Size | What it is |
|---|---|---|
| `HERO` | 2400 × 1350 | Mid-session, audience in frame, Daniel off-centre |
| `WORK` | 1200 × 1500 | Closer and portrait — a handful of people, not an audience |
| `ROOM` | 2400 × 1050 | The audience, not him. Carries a caption naming the event |
| `AFTER` | 1600 × 1200 | People talking to each other. The photograph that proves the headline |

A draft build renders each as a dashed box carrying its own brief, **at the
true aspect ratio of the final photograph**, so the page lays out at full
height with no images at all and nothing shifts when they land.
`--ship` fails while any remain, and names them.

To fill one: put the file in `migration/wix-assets/img/`, replace the token in
the `.dc.html` with `/assets/img/<filename>` — root-relative, because
`build-site.py` copies `wix-assets/` to `dist/assets/` and leaves relative
paths alone — and rerun.

Two open `[CLIENT]` markers in the source: the caption under the ROOM band
wants an event name and a year or it should be deleted, and Joe Moose's title
("Co-Founder, Solarcon") came off the old build rather than off the harvested
page, which named him only in an image filename.

The share card `img/og-speaking.jpg` is type-led like the rest of the set,
source at `migration/og-speaking-card.html`. It is the one card in the set
where a photograph would earn its keep — re-cut it once `HERO` is filled.

## As Seen In, and the link-rot problem

Eight podcast appearances, every one a URL on somebody else's platform. That
is the whole value of the page: every other page on this site is Daniel
describing Daniel, and this is eight other people putting him in front of
their audience with a link the reader can open.

Which means **a dead link costs more here than anywhere else on the site.**
All nine appearances listed on the Wix page were opened and checked on
24 Aug 2026, and the result is recorded in a comment beside each row:

- **Seven resolved** to a live episode, several with a verifiable date —
  Peak Performance Life EPI 113 (26 Sep 2023), Goals DO Come True S2E21
  (12 Sep 2023), Freedom Chasers ep 378 (22 Sep 2023).
- **One could not be confirmed.** `businesscreatorsradioshow.com` serves no
  HTML to a fetch, at the episode URL or the site root. It is marked
  `[CLIENT]` in the source. Open it in a browser; if it does not load, delete
  the row rather than leaving it.
- **One was a hard 404 and has been pulled.** "Life of an Adventurepreneur"
  at `dougbennett.co.uk/episode-88-…` is gone, and the episode is not on the
  Goals DO Come True feed either. It is Doug Bennett's second appearance with
  Daniel, so it happened; the link is what is gone. The source carries a note
  so it can go back in if a working URL turns up.

The Freedom Chasers URL slug still reads `coming-soon-with-daniel-lawson`.
**That is not a placeholder.** The episode is published; the host just never
changed the slug. Leave it exactly as it is.

`build-as-seen-in-bundle.py` cannot check links, so it checks the shape of the
arrangement instead: every row has to be external, `target="_blank"` and
`rel="noopener"`; the row count has to match the number written out in words
in the headline *and* in the lede, so the page cannot say "Eight of them"
above seven rows; and the verification date has to be present on the page, so
the claim stays attached to a date a reader can judge.

**Re-verify before any deploy much later than the last check**, and move the
date when you do. One of nine was already rotten by the time this was built.

### migration/map-new-assets.py

Written while building this page, and worth knowing about for the next one.
`asset-map.json` was generated once, from the ten bundles that existed then,
and `build-site.py --local` only rewrites Wix URLs it finds in that map.
Anything a newer page introduces is left pointing at `static.wixstatic.com`
and keeps working right up until the subscription lapses, at which point the
image vanishes and nothing in the build ever said a word about it. This page
introduced eight in one go — the podcast cover art.

Run it on any new source that brings in old-site imagery:

```
python3 migration/map-new-assets.py "../Parallaxx As Seen In.dc.html"          # report
python3 migration/map-new-assets.py "../Parallaxx As Seen In.dc.html" --apply  # do it
```

It finds the original in `wix-archive/` by media hash, names the local copy
from the `<img alt>` on the same tag, and appends to the map. It never
overwrites an existing file or an existing entry.

**One thing it learned the hard way.** Its first version matched URLs with a
character class that excluded `)`, which is right for a URL inside CSS
`url(...)` and wrong here: Wix names media after the uploaded filename, and
those have brackets in them — `Square Daniel (20).png`,
`Daniel Lawson Thumbnail (1).png`, `contier (1).png`. Two of the first eight
were cut at the `(` and registered half-length, and `build-site.py` then
replaced the half it recognised and left the rest, producing
`src="/assets/img/the-choice-effect.png).png"`. Every check short of actually
rendering the page said it was fine. It now matches inside the attribute
quotes, where a URL cannot be truncated, and refuses to register anything
that does not end in a file extension.

## Seeing the site before it goes anywhere

```
python3 migration/preview.py
```

Builds `dist/` exactly as the deploy does, serves it at
`http://localhost:8000`, prints every route and opens a browser. Ctrl-C stops
it.

**Use this rather than opening a `*-preview.html` file off the disk.** Those
files reference `static.wixstatic.com` for their images, on purpose — that is
what lets `build-site.py` find those URLs and rewrite them to `/assets/`.
Anything that blocks the request (offline, a content blocker, a proxy, or Wix
itself once the plan lapses) takes the images with it, and the failure does
not look like a preview problem. It looks like a design problem:

**The logo is a Wix image, so when it fails the header renders as a nearly
empty bar and the footer loses its mark, and the page reads as though the
chrome is missing.** It is not. `preview.py` loads nothing from Wix at all,
which is also the only honest way to check the migration actually worked.

### Where the header and footer come from

Nothing is added at hosting. There is no site-level chrome on Cloudflare or
Vercel the way there was on Wix. Every route is a standalone HTML file with a
real `<head>`, a single custom-element tag and one `<script>`, and **PtNav v3
and PtFooter v3 are compiled into that bundle**. That is the whole reason the
table above says to switch the Wix Header and Footer OFF for every row: leave
them on during the overlap and the page renders two navs and two footers.

### Contact and Speaking, 25 Aug: the two-doors block is gone from both

Contact's "Still looking" section and Speaking's "Here for yourself rather
than for an event?" aside were the same device — a third route to the men's
and women's doors, sitting at the bottom of a page that should say one thing.
**The footer already carries both doors on every page of the site**, so
neither block was reaching anybody who could not already get there. Removed
from the markup and the stylesheets of both.

### Contact's vertical rhythm, same pass

The page was built at the site's standard section padding, which is tuned for
pages people scroll through. This one is a lookup: somebody arrives knowing
what they want, and the four channels are the entire payload. So every
vertical measure came down — section padding, card padding, the gap between
detail rows, the heading sizes — and the phone breakpoint steps down again
rather than reusing the desktop numbers squeezed.

**The test is that all four channels clear the fold on a phone**, with the
nav still over the top of them. They do, on every handset size checked:

| Viewport | Fourth channel ends at |
|---|---|
| 390 × 844 (iPhone 14/15) | 613px |
| 375 × 667 (iPhone SE) | 634px |
| 430 × 932 (Pro Max) | 620px |
| 360 × 800 (Android) | 631px |

The opening section went from 831px to about 700 on a phone, and 888 to 750
on desktop. The grid and the card still share both outer edges.

## The placeholder that shipped, 25 Aug

`/daniel-lawson-speaking` went live carrying **four dashed boxes printing
their own photo briefs, addressed to Daniel in the second person** — *"You
mid-session with the audience in the frame"* — plus a caption reading
*"[CLIENT] Name the event and the year here."* All of it visible on the
public site.

There was a guard for this. It did not fire, and the reason matters more than
the incident:

> `build-speaking-bundle.py --ship` refuses to build while any slot is empty.
> It is **opt-in**, and nobody ran it. The script that actually runs on every
> deploy is `migration/build-site.py`, and that never looked.
>
> **A guard outside the deploy path is documentation, not a guard.**

### What changed

`build-site.py` now refuses to build any route whose bundle still contains
visible placeholder content, and it is the one script Cloudflare Pages calls
on every push, so nothing can route around it. It checks for `IMAGE_SLOT_`,
a rendered `class="sp-slot"` box, and a visible `[CLIENT]` note.

Two details in that check are load-bearing, and both came from getting it
wrong first:

- **It scopes to the HTML template, not the whole bundle.** The first version
  scanned the file and failed the build on a CSS *comment* explaining the slot
  mechanism. A guard should fire on what a visitor would read.
- **It strips HTML comments before looking for `[CLIENT]`.** That marker
  appears legitimately inside `<!-- -->` in the nav and footer as a note to
  whoever maintains them. The same string in visible copy is the defect.

`LUMIOS_MARKER_WOFF2_URL` is deliberately **not** a marker. It is in every
bundle on purpose and `FONTFACE_RE` strips the rule a few lines later. Listing
it failed all fifteen routes on the first attempt — a fair reminder that a
guard broad enough to catch everything catches the things it should not.

### And the page itself

Rebuilt around the **two real photographs the archive actually holds** —
Daniel mid-session with the audience, and the audience on its own. The other
two sections lost their images rather than keep a brief sitting where a
photograph should be, and both are a single measured column now. The CSS note
in §02 says how to widen them back out when there is real material.

The audience band has no caption. A captioned photograph is evidence and an
uncaptioned one is decoration, so it is worth adding — but nobody in this repo
knows which event it is, and guessing was how the placeholder got there in the
first place.

## The legal closings, 25 Aug

Both pages ended in a full section: a gold label, a headline
("Ask, and it gets handled." / "Something here unclear?") and two pill links.
That gave the least important thing on the page the loudest treatment on it —
a call to action at the end of a document nobody reads for pleasure.

Each now ends in **one line of subtext**, Daniel's own wording. The pills went
with the headings: each page's header already cross-links to the other, and
the site footer carries both, so they were a third route to somewhere the
reader could already get.

### They were always two pages

Worth stating plainly, because the source file makes it look otherwise.
`Parallaxx Legal.dc.html` holds **both** documents stacked, which is what you
see if you open it — but it is the authoring file, not a page.
`build-legal-bundles.py` slices it on the two `<section>` ids and emits two
separate bundles at two separate routes:

| URL | Tag | Bundle | Ends with |
|---|---|---|---|
| `/privacy-policy` | `parallaxx-privacy` | `parallaxx-privacy.js` | Data Security |
| `/terms-of-use` | `parallaxx-terms` | `parallaxx-terms.js` | 9. Governing Law |

Neither bundle contains a word of the other — `grep 'Governing Law'
parallaxx-privacy.js` returns nothing, and so does the reverse. The one-file
arrangement exists so the shared stylesheet cannot drift between them; see the
section above on why.

## Closing the privacy policy's gaps, 1 September 2026

Four sections were added to the Privacy Policy. They are marked in the source
with `ADDED 1 Sep 2026` and `PENDING LEGAL REVIEW`, and nobody here is a
lawyer — they are accurate about the business, not certified.

**Cookies and tracking.** Every claim in this section was verified against the
shipped bundles rather than assumed, and the finding was better than expected:
**there is no tracking on this site at all.** No Google Analytics, no
advertising pixel, no tag manager, and no first-party cookies. The Priority
Audit and the Archetype Quiz keep answers in memory only — their build scripts
*fail* if browser storage is added, so that is enforced rather than promised.
The section names the five third parties a visitor's browser does contact:
Google Fonts, cdnjs, unpkg, YouTube (already `youtube-nocookie`), and
LeadConnector on the two application pages only.

**Service providers.** Cloudflare, GoHighLevel, Stripe, Teachable, Namecheap
PrivateEmail, Google. Named, with what each one does.

**Retention.** Written to describe what actually happens — records kept, not
routinely deleted, removed on request — rather than a period nobody follows. A
policy that states a 24-month deletion cycle no one performs is worse than one
that admits to keeping things.

**International transfers.** An Australian business using US and EU providers,
serving people in the EEA and UK, needs this for GDPR. It was missing.

### The company number

The policy said `ACN 66 631 353 752`. That is eleven digits; an ACN is nine
and an ABN is eleven. Running the ABN checksum on it **validates**, so it is a
genuine ABN that was labelled ACN. Corrected to `ABN`.

An Australian company's ABN is normally its nine-digit ACN with two check
digits in front, which makes the ACN almost certainly **631 353 752** — but
"almost certainly" is not good enough to print as a company identifier, so
only the verified ABN is on the page. Confirm against the ASIC record and the
ACN can be added beside it.

### Still open

- **A lawyer has not seen any of this.** The four new sections are marked in
  the source so they are easy to find.
- **No pixel is on the site today.** Daniel expects to run ads later. The day a
  Meta or Google pixel goes on, the cookies section stops being true and EU
  visitors likely need a consent banner before it fires. That is a policy
  change to make *before* the pixel, not after.

## Identity 2.0 Challenge, and the one page with no chrome

**This is the only route in the build with no PtNav and no PtFooter**, and it
is deliberate. It is a VSL funnel page: the whole job is to get somebody to
press play and then enrol, and a full site nav on a page like that is ten ways
to leave before the video starts. It carries a slim header and a one-line
footer of its own instead. `build-identity-bundle.py` therefore has no
"chrome must be present" guard — what replaces it is a pair of guards on the
two things this page cannot ship without, the video and the enrol link.

It lives at **`/your-identity-challenge`** because that is the URL the footer
already links and the one old inbound links point at. Nothing to redirect.

### What changed from the version that was live

Layout, copy and structure are as they were. Three things were fixed:

1. **The palette is the site's now.** It was `#0A1A2F` against the site's
   `#04122A`, and `#C9A55B` against `#E8C65F`. Close-but-not-quite is worse
   than either matching or clearly differing — it reads as a page built at a
   different time, which is what it was.
2. **The enrol button is coral, not gold.** Gold is Daniel's voice on this
   site and coral is the visitor's move. There are two actions here and they
   are not the same size: **play** stays gold because watching costs nothing,
   **enrol** is coral because it is the commitment. The old page made both
   gold and flattened the distinction.
3. **Three pieces of mojibake.** The title, the bonus heading and the footer
   copyright each carried UTF-8 read as Latin-1 — the em dashes and the
   copyright sign rendered as literal garbage on the live page. The build now
   fails on those byte sequences.

Two smaller repairs: the play overlay was a `div` with a click handler, so the
only control on the page could not be reached by keyboard at all — it is a
`button` now. And every section starts at `opacity:0` and is revealed by an
IntersectionObserver, which means anything that stops the observer firing does
not degrade the page, it erases it. There is a four-second fallback that
reveals everything regardless.

### Still open

- **The enrol URL is unconfirmed.** It points at
  `members.parallaxxtransformations.com`, which was `CNAME members →
  preview.clientclub.net` (LeadConnector) and was **dropped in the migration**.
  Verified 17 Aug 2026: the host answers with a self-signed certificate, so no
  browser connects. Either restore that CNAME or repoint the button.
- **The video and poster are the last two Wix dependencies on the site.** Run
  `migration/download-identity-video.sh` before Wix is cancelled, then
  `map-new-assets.py`. A 1080p VSL cannot be reconstructed from a harvest the
  way copy can.
- No share card of its own; it borrows the home page's.

### build-site.py now warns about unmapped Wix assets

`localise()` only rewrites URLs it finds in `asset-map.json`, so anything a
newer page introduces stays pointed at Wix and works perfectly until the
subscription lapses. That is exactly how this page arrived. The build now
lists every surviving `wixstatic.com` URL by bundle at the end of its output.
A warning rather than an error, because it is currently true of a page we want
to ship — but a loud one.

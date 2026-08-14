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
| The Priority Audit | `Priority Audit.dc.html` | `build-priority-audit-bundle.py` | `parallaxx-priority-audit.js` · `parallaxx-priority-audit` | `priority-audit.html` |

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
| The Priority Audit | `…/parallaxx-priority-audit.js` | `parallaxx-priority-audit` |

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
python3 build-priority-audit-bundle.py
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

**Site Header and Footer stay ON for this page**, which is the opposite of
every other row in the table. The other bundles bake PtNav and PtFooter inside
themselves; this one ships no chrome at all, because it is an instrument rather
than a page. Turn the chrome off and there is no way out of it.

`priority-audit-preview.html` is generated by the build and is a different
thing again: a standalone page with its own minimal header, for reading the
instrument without Wix in the way. `priority-audit.html` is the harness that
shows what Wix will actually render.

## The Reconnected Man

Rebuilt onto the v4 system from the older Give It All-skinned page.
`RECONNECTED-MAN-AUDIT.md` records what changed and why, and lists the work
still open, the largest being that the testimonial screenshots are still
flattened PNGs and need transcribing into real text.

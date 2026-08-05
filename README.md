# parallaxx-transformations

Website for Parallaxx Transformations (sister site to Give It All).

Every page is authored as a `.dc.html` component and compiled into a
self-contained Wix Custom Element. **The `.dc.html` is the source of record.**
Never hand-edit a generated `.js` bundle; edit the source and rerun its build.

| Page | Source | Build | Bundle / tag | Preview |
|---|---|---|---|---|
| Home | `Parallaxx Home Men.dc.html` | `build-home-men-bundle.py` | `parallaxx-home-men.js` · `parallaxx-home-men` | `index.html` |
| The Reconnected Man | `The Reconnected Man.dc.html` | `build-reconnected-man-bundle.py` | `parallaxx-reconnected-man.js` · `parallaxx-reconnected-man` | `reconnected-man.html` |
| Home, women | `Parallaxx Home Women.dc.html` | `build-home-women-bundle.py` | `parallaxx-home-women.js` · `parallaxx-home-women` | `home-women.html` |

Also here: `parallaxx-wheel-of-reconnect.js`, a standalone interactive element,
and `support.js`, the local shim that lets a `.dc.html` open in a browser.

## Build

```
python3 build-home-men-bundle.py
python3 build-reconnected-man-bundle.py
python3 build-home-women-bundle.py
```

All three refuse to build rather than ship a bundle that fails silently in a
shadow root. See the docstring in `build-home-men-bundle.py` for why the step
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
page load was the largest leak in the funnel. `Priority Audit.dc.html` still
exists as the standalone and has diverged: it does not carry the result copy
this page uses.

## The Reconnected Man

Rebuilt onto the v4 system from the older Give It All-skinned page.
`RECONNECTED-MAN-AUDIT.md` records what changed and why, and lists the work
still open, the largest being that the testimonial screenshots are still
flattened PNGs and need transcribing into real text.

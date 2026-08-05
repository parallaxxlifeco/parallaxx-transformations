# parallaxx-transformations

Website for Parallaxx Transformations (sister site to Give It All).

Every page is authored as a `.dc.html` component and compiled into a
self-contained Wix Custom Element. **The `.dc.html` is the source of record.**
Never hand-edit a generated `.js` bundle; edit the source and rerun its build.

| Page | Source | Build | Bundle / tag | Preview |
|---|---|---|---|---|
| Home | `Parallaxx Home Men.dc.html` | `build-home-men-bundle.py` | `parallaxx-home-men.js` · `parallaxx-home-men` | `index.html` |
| The Reconnected Man | `The Reconnected Man.dc.html` | `build-reconnected-man-bundle.py` | `parallaxx-reconnected-man.js` · `parallaxx-reconnected-man` | `reconnected-man.html` |

Also here: `parallaxx-wheel-of-reconnect.js`, a standalone interactive element,
and `support.js`, the local shim that lets a `.dc.html` open in a browser.

## Build

```
python3 build-home-men-bundle.py
python3 build-reconnected-man-bundle.py
```

Both scripts refuse to build rather than ship a bundle that fails silently in a
shadow root. See the docstring in `build-home-men-bundle.py` for why the step
exists at all.

## Deploy

In the Wix editor, place a Custom Element widget with the Source URL and Tag
from the table above, and turn the site Header and Footer **off** for that
page. Bump the `?v=` query in the preview harness on every deploy so the CDN
and browser caches let go.

SEO is set in Wix page settings, not in the component.

## The Reconnected Man

Rebuilt onto the v4 system from the older Give It All-skinned page.
`RECONNECTED-MAN-AUDIT.md` records what changed and why, and lists the work
still open, the largest being that the testimonial screenshots are still
flattened PNGs and need transcribing into real text.

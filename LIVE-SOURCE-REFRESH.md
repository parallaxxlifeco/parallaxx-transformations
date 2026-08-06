# Re-capturing a live embed source

`build-embed-chrome.py` refuses to build unless `src/` holds byte-for-byte what
the site is actually serving. This is how you refresh one.

It exists because a stale source shipped once. The woman's page had been edited
on the site and the copy in the design folder had not, so the build produced a
page with the old hero line on it. Nothing about the file looked wrong.

---

## 1. Find the embed URL

Both pages are Wix HTML embeds, so the page you see is an iframe pointing at
`filesusr.com`. Open the live page, then in the browser console:

```js
document.querySelector('iframe').src
```

Current values:

| Page | Embed URL |
|---|---|
| The Reconnected Man | `https://www-parallaxxtransformations-com.filesusr.com/html/111174_6905def14065216df2e4cbaed4764a26.html` |
| The Reconnected Woman | `https://www-parallaxxtransformations-com.filesusr.com/html/111174_b0bdfe412cc99afb93476879599f9c5f.html` |

These change when Wix republishes the embed. Re-read the iframe src rather than
trusting the table.

## 2. Save it

Open the embed URL directly in a tab and save the page as **Webpage, HTML Only**
(`Cmd+S`). Not "Complete" — that rewrites paths and pulls down assets.

Drop the result in `src/`, named `reconnected-man-wix-inject.html` or
`reconnected-woman-wix-inject.html`.

## 3. Get the new fingerprint

Still on the live page, in the console:

```js
(async () => {
  const r = await fetch(document.querySelector('iframe').src);
  const t = await r.text();
  const hash = s => { let h = 0; for (let i = 0; i < s.length; i++) h = (h * 31 + s.charCodeAt(i)) | 0; return h; };
  console.log({ len: t.length, hash: hash(t) });
})()
```

Paste `len` and `hash` into the matching `PAGES` entry in
`build-embed-chrome.py` as `live_len` and `live_hash`.

The fetch works from the live page because `filesusr.com` allows cross-origin
reads. It does not work from a blank tab.

## 4. Build

```
python3 build-embed-chrome.py
```

Green means the source matched the fingerprint and the chrome went on. Red tells
you which file is stale and by how much.

---

## Why not automate the capture

The fetch above has to run in a page on the parallaxxtransformations.com origin,
and the saved file has to come off a browser that is signed in to nothing in
particular. Both are ten seconds by hand and neither is worth a script that
would silently rot the moment Wix changes the embed URL scheme.

## The real fix

None of this is needed once the pages stop being HTML embeds. Turn the site
header and footer back on, place `parallaxx-nav` and `parallaxx-footer` as Wix
Custom Elements the way the redesigned pages do, and the chrome arrives from the
template instead of being baked into a copy of the page.

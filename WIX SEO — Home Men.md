# Wix SEO — Home Men (`/home-men`)

Maps to Wix **Edit SEO Settings** for the page. Field names match the Wix tabs
(General / Social Share / Advanced). No em dashes used anywhere.

Live URL: `https://www.parallaxxtransformations.com/home-men`

---

## General

**Page name (internal):**
Home — Men

**Title tag (SEO title)** — 53 chars:

```
Coaching for Married Men Who Feel Distant | Parallaxx
```

> Why not the hero line. "You handled it all yourself" is the best sentence on
> the page but it is a *recognition* line, not a *search* line. Nobody types it.
> The title has to survive being read cold in a results list next to nine
> competitors, so it names who it is for and what it is. The hero line does its
> job on the OG card below, where the reader has already been handed context.

**Meta description** — 149 chars:

```
You handle everything at home and still feel unreachable. Coaching for married men who stopped asking for anything. Find the pattern you are running.
```

**URL slug:**

```
home-men
```

**Let search engines index this page:** ON

**Main subject / focus keyword:**

```
coaching for married men
```

**Supporting keywords** (work these into page copy over time, not a Wix field):
emotional distance in marriage · married but lonely · feeling disconnected from
your wife · men's relationship coaching · midlife marriage disconnection ·
why does my wife say I am not present

---

## Social Share (Open Graph / Facebook)

**OG Title** — 48 chars:

```
You handled it all yourself. That's the distance.
```

> Here the hero line IS right. A shared link arrives with a face and a friend
> attached to it, so it does not need to explain itself, it needs to stop a
> thumb. Recognition beats description at this size.

**OG Description** — 110 chars:

```
A husband who sorts everything. And a man she never feels. Find which of the five patterns you are running.
```

**OG Image:**
`1200 x 630px`. Generate from `home-men-og.html` (see below), export as
`og-home-men.jpg`, upload to Wix Media, then select it in this field.

---

## Social Share (X / Twitter)

**Card type:** Summary with large image (`summary_large_image`)

**Twitter Title:**

```
You handled it all yourself. That's the distance.
```

**Twitter Description:**

```
A husband who sorts everything. And a man she never feels.
```

**Twitter Image:** same file as OG, `og-home-men.jpg`.

---

## Advanced

**Canonical URL:**

```
https://www.parallaxxtransformations.com/home-men
```

Set it explicitly rather than leaving it default. Two avatar pages that share a
design system and some phrasing are exactly the situation where Google starts
guessing, and you do not want the men's page consolidated into the women's.

**Structured data markup (JSON-LD)** — paste into "Add structured data markup":

```json
{
  "@context": "https://schema.org",
  "@type": "Service",
  "name": "Relationship coaching for married men",
  "serviceType": "Relationship and identity coaching",
  "url": "https://www.parallaxxtransformations.com/home-men",
  "description": "Coaching for married men who handle everything at home and still feel unreachable. Identify which of five protective patterns you are running, and what it is costing you.",
  "audience": {
    "@type": "Audience",
    "audienceType": "Married men"
  },
  "areaServed": {
    "@type": "Place",
    "name": "Worldwide, delivered online"
  },
  "provider": {
    "@type": "Person",
    "name": "Daniel Lawson",
    "jobTitle": "Accredited coach and facilitator",
    "url": "https://www.parallaxxtransformations.com/about-daniel-lawson",
    "worksFor": {
      "@type": "Organization",
      "name": "Parallaxx Transformations",
      "url": "https://www.parallaxxtransformations.com"
    },
    "sameAs": [
      "https://www.youtube.com/@ReconnectYou1",
      "https://www.facebook.com/Kiwi.Daniel",
      "https://www.instagram.com/daniel.lawson__/",
      "https://www.linkedin.com/in/daniel-reconnect-you/"
    ]
  }
}
```

**Second block, optional but cheap** — breadcrumbs, so the results listing shows
a path instead of a bare URL:

```json
{
  "@context": "https://schema.org",
  "@type": "BreadcrumbList",
  "itemListElement": [
    { "@type": "ListItem", "position": 1, "name": "Home", "item": "https://www.parallaxxtransformations.com/" },
    { "@type": "ListItem", "position": 2, "name": "For Men", "item": "https://www.parallaxxtransformations.com/home-men" }
  ]
}
```

---

## Do NOT add review markup to this page

The three testimonials on the page make `Review` and `AggregateRating` schema
look like free stars in the search listing. Do not do it.

Google explicitly disallows **self-serving reviews** — reviews about a business,
collected and published by that same business — for `Organization`,
`LocalBusiness` and their subtypes. It will either be ignored, or it earns a
structured data manual action. Neither is worth it.

Real client quotes as visible page text are still valuable. They just do not go
in the markup.

---

## Two things that are not SEO fields but will break with this URL

**1. The nav will not highlight.** PtNav v3 works out which item to underline
from the URL path, because the nav lives once in the site header strip and
serves every page from a single instance. Its table currently reads:

```js
[/^\/(men|the-reconnected-man|the-archetype-quiz)\b/, 'men'],
```

`/home-men` does not match that. Add it to `PtNav v3.dc.html` and rerun
`build-chrome-bundles.py`, or the For Men item stays unlit on its own page.

**2. The nav links point at `/men`.** Both nav hrefs are currently
`parallaxxtransformations.com/men` and `/women`. If the real pages are
`/home-men` and `/home-women`, every nav click 404s. Either change the hrefs,
or set `/men` as a Wix URL redirect to `/home-men`.

> A redirect is arguably the better answer: `/men` is the shorter, more
> guessable, more shareable URL, and it is the one already printed in the nav.
> Worth asking whether the page should just live at `/men` instead.

---

## Quick reference (lengths)

| Field | Limit | Current |
|---|---|---|
| Title tag | under ~60 | 53 |
| Meta description | under ~155 | 149 |
| OG title | under ~60 | 48 |
| OG description | under ~130 | 110 |
| OG image | 1200 x 630 (1.91:1) | to generate |

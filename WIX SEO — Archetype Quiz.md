# Wix SEO — Protection Archetype Quiz (`/the-archetype-quiz`)

Maps to Wix **Edit SEO Settings**. Field names match the Wix tabs
(General / Social Share / Advanced). No em dashes anywhere.

Live URL: `https://www.parallaxxtransformations.com/the-archetype-quiz`

Verified against the built quiz: 22 questions, five archetypes, result shown
on screen, email requested only after the result.

---

## General

**Page name (internal):**
The Archetype Quiz

**Title tag (SEO title)** — 51 chars:

```
Free Protection Archetype Quiz for Men | Parallaxx
```

> "Free" earns its place here and nowhere else on the site. On a quiz result
> the single biggest reason a man does not click is suspecting a gate at the
> end. Saying it in the title removes that objection before he has to think
> about it, and it is true: the result is on screen.

**Meta description** — 152 chars:

```
Five ways men protect themselves from the closeness they want. Answer 22 questions and find out which one you are running. Two minutes, result on screen.
```

**URL slug:**

```
the-archetype-quiz
```

> Do not change this. PtNav v3 routes it already, and the routing keeps the
> For Men nav item lit for the whole run.

**Let search engines index this page:** ON

**Main subject / focus keyword:**

```
protection archetype quiz
```

**Supporting keywords:**
emotional unavailability quiz men · why can't I open up to my wife ·
men's attachment quiz · relationship self protection · what is my emotional
pattern · quiz for married men

---

## Social Share (Open Graph / Facebook)

**OG Title** — 47 chars:

```
Which of the five are you running?
```

**OG Description** — 121 chars:

```
Five ways men protect themselves from the closeness they want. 22 questions, two minutes, and the answer is on screen.
```

**OG Image:**
`1200 x 630px`, `og-quiz.jpg`. Not built yet. The men's card
(`home-men-og.html` and `og-home-men.jpg`) is the template: same navy, same
film, same brand plate. Say the word and I will render it the same way.

---

## Social Share (X / Twitter)

**Card type:** Summary with large image

**Twitter Title:**

```
Which of the five are you running?
```

**Twitter Description:**

```
22 questions. Two minutes. The answer is on the screen, not in your inbox.
```

**Twitter Image:** same file as OG.

---

## Advanced

**Canonical URL:**

```
https://www.parallaxxtransformations.com/the-archetype-quiz
```

**Structured data markup (JSON-LD)** — paste into "Add structured data markup":

```json
{
  "@context": "https://schema.org",
  "@type": "WebApplication",
  "name": "Protection Archetype Quiz",
  "url": "https://www.parallaxxtransformations.com/the-archetype-quiz",
  "applicationCategory": "LifestyleApplication",
  "operatingSystem": "Any modern web browser",
  "browserRequirements": "Requires JavaScript",
  "isAccessibleForFree": true,
  "offers": {
    "@type": "Offer",
    "price": "0",
    "priceCurrency": "EUR"
  },
  "description": "A 22 question self assessment that identifies which of five protection patterns a man runs in his closest relationships. The result is shown on screen immediately.",
  "audience": {
    "@type": "Audience",
    "audienceType": "Men in long term relationships"
  },
  "about": {
    "@type": "Thing",
    "name": "Emotional self protection in relationships"
  },
  "creator": {
    "@type": "Person",
    "name": "Daniel Lawson",
    "url": "https://www.parallaxxtransformations.com/about-daniel-lawson"
  },
  "publisher": {
    "@type": "Organization",
    "name": "Parallaxx Transformations",
    "url": "https://www.parallaxxtransformations.com"
  }
}
```

**Second block** — breadcrumbs:

```json
{
  "@context": "https://schema.org",
  "@type": "BreadcrumbList",
  "itemListElement": [
    { "@type": "ListItem", "position": 1, "name": "Home", "item": "https://www.parallaxxtransformations.com/" },
    { "@type": "ListItem", "position": 2, "name": "For Men", "item": "https://www.parallaxxtransformations.com/home-men" },
    { "@type": "ListItem", "position": 3, "name": "The Archetype Quiz", "item": "https://www.parallaxxtransformations.com/the-archetype-quiz" }
  ]
}
```

---

## Do NOT use `Quiz` schema, even though it exists

`schema.org/Quiz` is built for **educational assessment**. It expects
`hasPart` entries of `Question` with an `acceptedAnswer` marked correct, and
Google surfaces it in education results.

A personality assessment has no correct answers. Marking it up as `Quiz`
misdescribes it, earns nothing, and invites a structured data warning.
`WebApplication` is the honest description: a free interactive tool.

---

## The real SEO risk on this page, and it is architectural

Every word of this quiz lives inside a **shadow root**, because it ships as a
Wix Custom Element. Google does render pages and can generally read shadow
DOM content, but it is markedly less reliable than plain light DOM, and
nothing here is in a slot.

Practically that means the page may rank on **title, description and schema
alone**, with none of the body copy contributing.

Two mitigations, in order of value:

1. **Put a short block of real Wix text above the quiz element.** Two or
   three sentences naming the five archetypes in plain text. That is the
   whole SEO surface of the page and it costs nothing. It also gives a man
   who arrives from search something to read before he commits to 22
   questions.
2. Leave it. A quiz page is usually reached from your own site, an ad or a
   share, not from organic search. If this page is never meant to rank, none
   of the above matters much and the meta fields are enough.

This applies to every page on the site, not just this one. It is the cost of
the custom element architecture, and it was the right trade for the design.

---

## Quick reference

| Field | Limit | Current |
|---|---|---|
| Title tag | under ~60 | 51 |
| Meta description | under ~155 | 152 |
| OG title | under ~60 | 34 |
| OG description | under ~130 | 121 |
| OG image | 1200 x 630 | to build |

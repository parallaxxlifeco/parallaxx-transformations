# Rebuild queue

Everything deliberately left behind in the Wix → Cloudflare migration, in the
order it costs something. Nothing here blocks the DNS cutover; all of it can
ship afterwards, because every push to `main` redeploys Pages in ~90 seconds.

Written 18 Aug 2026.

---

## 1. Identity 2.0 Challenge

**Status: BUILT, 1 Sep 2026, at `/your-identity-challenge`.**

Not from the harvested GoHighLevel funnel — Daniel supplied the current page,
which is a different and better offer: a **free 7-day challenge** rather than
the paid course that was harvested. The harvest in
`harvested/harvested-identity-2-0-challenge.html` is the 2023 paid programme
and is superseded, though it is worth keeping as the record of what that offer
was.

Two things are unresolved and both are in the README: the enrol button points
at a subdomain the migration dropped, and the video and poster are still
served from Wix. `migration/download-identity-video.sh` handles the second.
The first needs Daniel to confirm where enrolment actually lives.

## 2. Contact — `/contact-daniel-lawson`

**Status: DONE, 24 Aug 2026. Rebuilt on the v4 system as `parallaxx-contact`.**

Source of record `Parallaxx Contact v4.dc.html`, built by
`build-contact-bundle.py`, routed in `migration/build-site.py`.

Direct `mailto` to **daniel@parallaxxtransformations.com** plus Instagram,
LinkedIn, YouTube and Facebook. No form: the old page's form called
`preventDefault()` and discarded every field, and the build now fails on a
`<form>` element so it cannot come back by accident.

The old `Parallaxx Contact.dc.html` was on the Give It All skin, not v4, so
this was a rebuild rather than a build script over the existing source. It has
been moved to `_to_delete/`.

Carries its own share card (`img/og-contact.jpg`, source at
`migration/og-contact-card.html`) and a portrait, `daniel-conversation.jpg`
from the Wix archive. Nothing left open on it.

## 3. Privacy Policy and Terms of Use

**Status: DONE, 24 Aug 2026. Both rebuilt as real pages.**

One source of record, `Parallaxx Legal.dc.html`, built by
`build-legal-bundles.py` into `parallaxx-privacy` and `parallaxx-terms`, both
routed in `migration/build-site.py` and both indexable.

The copy is the harvested Wix text verbatim; only the typesetting changed.

**Both pages are dated 1 September 2026**, moved off the original 13 June 2023
on Daniel's instruction. Worth knowing what that date now asserts: it tells a
reader, and an ad-platform reviewer, that the policy was current as of that
day. The gaps that were open when the date moved have since been closed --
cookies and tracking, named service providers, retention, international
transfers, and the ACN/ABN mix-up. See the README. What has NOT happened is a
lawyer reading any of it. A policy dated today that does not mention
cookies reads worse in a review than the same policy honestly dated 2023,
because the recent date asserts a review that has not happened yet. The fix is
the lawyer's half hour, not the date.
See the README for the five gaps in what that copy actually covers — cookies
and analytics, named processors, retention, the ACN that is eleven digits, and
the June 2023 date. All five are for a lawyer, not for this repo, and all five
matter the next time an ad account is reviewed.

## 4. The Vault — was `vault.parallaxxtransformations.com`

**Status: DNS record deleted.**

Pointed at Teachable (`school.teachable.com`) and was serving *"Welcome to The
Vault of Transformations!"* at the time of deletion. Daniel confirmed nothing
is being sent there.

If anyone still holds a link, it now fails to resolve. If that turns out to
matter, the record was:

    CNAME   vault   school.teachable.com   (DNS only — never proxy it)

## 5. Footer pages that no longer exist

**Speaking is DONE, 24 Aug 2026.** `/daniel-lawson-speaking` is a real page
again — rebuilt as a credibility page rather than the sales page it was, on
the v4 system, from `Parallaxx Speaking.dc.html`. `/facilitating` now
redirects to it rather than to `/`, because it is the same offer described a
second way.

**It shipped with those four slots visible, and that is fixed.** The page now
uses the two real photographs the archive holds and the other two sections
have no image. `migration/build-site.py` refuses to build any route carrying a
visible placeholder, so it cannot recur — see the README. Two briefs remain in
the `SLOTS` table in `build-speaking-bundle.py` as the spec for better
material when it exists.

**The mislabelled quiz link is FIXED, 24 Aug 2026.** The footer's "The
Archetype Quiz" pointed at `/reconnect` on every page of the site, and
`/reconnect` 301s to the home page. The comment above the link asserted that
`/reconnect` *was* the quiz. It never was: the harvested page shows
`/reconnect` was the Reconnect programme, a fourteen week invitation-only
pathway. So the label was right, the URL was wrong, and the comment would have
talked the next person out of fixing it. All three are corrected.

That link is baked into twelve separate places, so the fix went into
`PtFooter v3.dc.html` plus every `.dc.html` that carries a copy, and every
bundle was rebuilt and **diffed against its previous version to confirm the
rebuild changed the link and nothing else**. Eleven of twelve came back clean,
which is worth recording on its own: the bundles in this repo are NOT
generally ahead of their sources, and the footer is the only known exception.

`parallaxx-footer.js` is that exception and was hand-edited instead, because
rebuilding it would have reverted the phone-column fix it carries and traded
one defect for another. There is a comment at the top of that file saying so.
The Reconnected Woman is covered by the same edit, since it is the one page
that loads the footer bundle at runtime rather than baking it in.

**The Progress Journal and Three Toxic Lies are BUILT, 13 Sep 2026.**
`/ptjournal` and `/three-toxic-lies` are real pages again, both on the v10
kit with the nav and footer loaded as shared bundles. `/free-ebook-three-
toxic-lies` now points at the book rather than at the home page, because
anybody arriving on it came looking for that exact thing. Neither page is
committed yet — they are waiting on a copy read.

Still 301ing to `/` and still linked from the footer on every page:

`/parallaxx-perspectives-podcast` · `/blog`

Two links, and both land on the home page. A footer link that goes nowhere is
worse than no footer link, so each one is a choice: build the page, or cut the
link. `/blog` has a harvested index listing three article titles and none of
the article bodies, so rebuilding it means finding the articles first.
`/parallaxx-perspectives-podcast` harvested to 915 bytes and is an opt-in form
for "Parallaxx Perspective resources", which is thin enough that cutting the
link is the honest answer unless the podcast is coming back.

`/reconnect-you-podcast-with-daniel-lawson` is no longer a dead end — it
redirects to the YouTube channel.

### The one that matters: `/reconnect`

`/reconnect` has no footer link, so it is a plain redirect rather than a dead
end, and that has made it easy to keep deferring. It should not be.

Reconnect is a live offer with no page of its own, and it is now the
destination two other pages point at. The Three Toxic Lies book sells it on
its last page — somebody who buys the book, reads it, and follows the call to
action lands on the home page. The `/three-toxic-lies` page repeats that
promise in "what you get". So the gap is no longer only an old inbound link
with nowhere to go; it is the end of a funnel that is being actively sold into.

The harvested copy is the biggest on the site at 23,769 bytes, and it is
entirely the 2023 voice — "STOP BEING A COG IN THE MACHINE OF SOCIETY", "the
harsh truth", "by invitation only", "science backed pathway". It is a rewrite,
not a port.

### Legacy offers, parked on purpose

Real copy survives for these, and none of them looks like a current offer.
Listed so nobody has to re-derive it:

| Route | Harvest | What it was |
|---|---|---|
| `/limitless-potential` | 18,434 b | Segmented programme — Business Leaders, Founder/CEO, Show-Biz |
| `/morning-mastery-club` | 18,065 b | In-person sunrise events, same three segments |
| `/elite-life-challenge` | 17,008 b | A challenge. Its own page says "Doors Closed" |
| `/personal-leadership-resources` | 4,374 b | A hub listing Three Toxic Lies and the Progress Journal |
| `/free-guide` | 2,194 b | "Feel to Heal Emotions Guide" lead magnet, email opt-in |
| `/coaching-experiences` | 577 b | Almost nothing survived |

`/personal-leadership-resources` is the cheap one. It was a shelf pointing at
the two products, both of which are real pages again, so it could be rebuilt
from the two things that already exist rather than from its own copy.

The remaining fourteen redirects — the thank-you pages, `/members`,
`/programs`, `/home`, `/digital-coaching-products`, `/peakperformance-
community` and the rest — harvested to nothing and are correctly parked.

**As Seen In is DONE, 24 Aug 2026.** `/daniel-lawson-as-seen-in` is a real
page again, from `Parallaxx As Seen In.dc.html`. Eight appearances, every link
opened and verified — one of the nine on the Wix page was a hard 404 and has
been pulled, and one host could not be confirmed and is marked `[CLIENT]`.
See the README for both.

Its cover art is now localised. It was not, at first: `asset-map.json` only
knew the URLs from the original ten bundles, so eight thumbnails were still
loading off Wix and would have gone dark the day the subscription lapsed.
`migration/map-new-assets.py` exists to catch that, and it has been run across
every page built this session.

## 6. Book a call

**Status: `/book-a-call-with-daniel-lawson` 301s to `/`. Dropped on request.**

When there's a calendar to point at, it's one line in `REDIRECTS` in
`build-site.py`.

## 7. The 15 Wix blog posts

All caught by `/post/*` → `/`. If any pulled organic traffic, check Search
Console before the domain moves — that history is easier to read while the old
URLs are still indexed.

---

# Known defects carried over

These are pre-existing and were found during migration, not caused by it.

**`parallaxx-footer.js` is ahead of its source.** The committed bundle carries a
phone-column fix that `PtFooter v3.dc.html` never received. Running
`build-chrome-bundles.py` silently reverts it. Port the fix into the source
before ever rebuilding that bundle.

**Lumios Marker was never uploaded.** Seven pages referenced a `@font-face`
pointing at the literal string `LUMIOS_MARKER_WOFF2_URL`. The build strips the
rule now, and the stack falls through to Permanent Marker. To restore it, drop
the real `.woff2` into `migration/wix-assets/` and remove the strip.

**~~Testimonial screenshots are flattened PNGs.~~ DONE, 14 Sep 2026.** The v2
rebuild (`138e618`) transcribed them. The live page carries three real
`<blockquote>` testimonials with bylines -- Jordi, Harrison, Alex -- and there
are no screenshot-named assets anywhere in the repo. Checked across all five
main bundles: 16 real blockquotes, zero flattened quotes. The note in
`RECONNECTED-MAN-AUDIT.md` is stale for the same reason; that audit describes
the version this one replaced.

**No DMARC record.** SPF and DKIM are both in place, so adding DMARC is cheap
deliverability insurance:

    TXT   _dmarc   v=DMARC1; p=none; rua=mailto:parallaxxlifeco@gmail.com

Start at `p=none` so it reports and never rejects.

---

# Give It All — a second migration, not a footnote

`giveitallevent.com` is also on Wix nameservers (`ns14`/`ns15.wixdns.net`) and
carries email forwarding through `eforward1/2/3.registrar-servers.com` with its
own SPF record.

**So Wix cannot be cancelled until that domain is moved too.** Its repo
(`gia-site`) is already granted to Cloudflare. Its email is simpler than
Parallaxx's — forwarding rather than real mailboxes, so no DKIM key to preserve.

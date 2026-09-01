# Rebuild queue

Everything deliberately left behind in the Wix → Cloudflare migration, in the
order it costs something. Nothing here blocks the DNS cutover; all of it can
ship afterwards, because every push to `main` redeploys Pages in ~90 seconds.

Written 18 Aug 2026.

---

## 1. Identity 2.0 Challenge — was `start.parallaxxtransformations.com`

**Status: DNS record deleted. The page is gone as of the cutover.**

It was a LeadConnector-hosted funnel (`sites.ludicrous.cloud`) serving
*"Your Blueprint to Evolve into Your Identity 2.0 Challenge"* — full landing
page with testimonials and enrolment. Daniel's call to drop it and rebuild
inside the main site rather than keep a subdomain pointing at GoHighLevel.

To rebuild: it becomes a route in `build-site.py` like any other page. Copy
needs recovering from the LeadConnector builder before that account is touched
— **do this before cancelling anything at GHL**, or the copy goes with it.

Suggested route: `/identity-2-0` or `/challenge`. Add a redirect from
`/your-identity-challenge` (currently 301s to `/the-archetype-quiz`).

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
day. The five gaps listed in the README -- no cookies or analytics section, no
named processors, no retention period, an ACN that is eleven digits -- were
all still open when the date moved. A policy dated today that does not mention
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

Still 301ing to `/` and still linked from the footer on every page:

`/three-toxic-lies` · `/parallaxx-perspectives-podcast` ·
`/reconnect-you-podcast-with-daniel-lawson` · `/blog` · `/ptjournal`

`/reconnect` no longer has a footer link pointing at it, so it is a plain
redirect rather than a dead end. Worth deciding where it should land, though:
Reconnect is still a live offer with no page of its own, and the home page is a
weak answer for anybody arriving on it from an old link.

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

**Testimonial screenshots are flattened PNGs.** Noted in
`RECONNECTED-MAN-AUDIT.md`. Invisible to search engines and unreadable to
screen readers. Transcribing them into real text is the single biggest SEO win
left on that page.

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

# Wix → Vercel migration runbook

Everything needed to go live on Vercel and switch DNS without losing email,
the Teachable vault, or the site's existing SEO.

Written 16 Aug 2026, revised 17 Aug. Read the whole thing once before starting step 1.

---

## The headline

**Wix is running your DNS, not Namecheap.** The nameservers are
`ns14.wixdns.net` and `ns15.wixdns.net`. Namecheap is only the registrar.

That means the Wix subscription is not just holding up the website. It is
holding up:

| What | How it depends on Wix DNS |
|---|---|
| **Your email** | `MX` → `mx1/mx2.privateemail.com`, plus SPF and the DKIM key |
| **The Teachable vault** | `vault` → `school.teachable.com` |
| **Webmail** | `mail` → `privateemail.com` |

Let the plan lapse without moving these first and email stops arriving —
silently, with senders getting bounces you never see. Section 3 exists to
prevent exactly that.

Order matters: **deploy first, verify on the Vercel URL, move DNS last.**

---

## 1. What was built

The repo already produced Wix Custom Elements — `.js` bundles Wix loaded into
widgets. Wix supplied each page's `<head>`: title, description, canonical, OG
image. Nothing else did. Deploy the preview harnesses as-is and every page
ships titled "… (preview)" with no description and no share image, and nine
ranking URLs lose their SEO overnight.

So `build-site.py` now owns that `<head>`. The metadata in its `ROUTES` table
was harvested verbatim off the live Wix pages before cancellation — it is the
existing SEO carried across, not rewritten copy.

It also cuts the ties to the hosts being left behind:

- **293 absolute `www.parallaxxtransformations.com` links → root-relative.**
  Without this, every nav link on a `vercel.app` preview jumps back to the live
  Wix site and the deploy cannot be tested honestly.
- **2 hardcoded `parallaxxlifeco.github.io` references → local.** The Reconnected
  Woman bundle was pulling its nav and footer from GitHub Pages by absolute URL.
- **7 broken `@font-face` rules removed.** `LUMIOS_MARKER_WOFF2_URL` was never
  replaced with a real URL, so seven pages have been 404ing on it. The stack
  already falls through to Permanent Marker, so nothing changes on screen — one
  failed request per page disappears. The sources keep the TODO; upload the real
  `.woff2` to `wix-assets/` and it is a one-line job.

### Routes

| URL | Element | Was |
|---|---|---|
| `/` | `parallaxx-home` | Wix Custom Element |
| `/men` | `parallaxx-home-men` | ← note: `index.html` in the repo root was the **men's** page, not the front door |
| `/women` | `parallaxx-home-women` | |
| `/the-reconnected-man` | `parallaxx-reconnected-man` | |
| `/the-reconnected-woman` | `parallaxx-reconnected-woman` | light DOM, not shadow |
| `/priority-audit` | `parallaxx-priority-audit` | |
| `/about-daniel-lawson` | `parallaxx-about-page` | |
| `/testimonials-daniel-lawson` | `parallaxx-testimonials` | |
| `/the-archetype-quiz` | `parallaxx-quiz` | |
| `/wheel-of-reconnect` | `parallaxx-wheel-of-reconnect` | bundle existed, never had a page |

### Redirects

Your Wix sitemap carries **64 indexed URLs**; 10 have a home on the new site.
The other 54 would hard-404 the moment DNS switches — losing their Google
rankings and breaking every old link in podcast show notes, emails and social
posts. `vercel.json` 301s all of them (42 rules, with the 15 blog posts caught
by one `/post/:slug*` wildcard).

---

## 2. Deploy to Vercel

Nothing here touches DNS. The site goes live on a `vercel.app` URL first, gets
tested properly, and only then takes over the domain.

### Where everything lives

Everything for this migration sits in `migration/`, inside the repo:

```
parallaxx-transformations/
├── vercel.json                    ← repo root; Vercel reads it nowhere else
├── dist/                          ← generated output, gitignored
└── migration/
    ├── MIGRATION.md               ← this file
    ├── build-site.py              ← builds dist/
    ├── asset-map.json             ← 68 Wix URLs → local paths
    ├── download-wix-assets.sh     ← pulls the assets off Wix
    ├── dns-records.txt            ← the nine DNS records
    └── wix-assets/                ← created by the download script
```

`build-site.py` works from either directory — it locates the repo from its own
position rather than from your working directory.

### 2a. Get the assets off Wix — do this first

`download-wix-assets.sh` pulls all 68 Wix-hosted files (57 images, 11 videos),
including 9 OG share images that exist **only** in Wix page settings and would
otherwise vanish without warning.

```bash
cd ~/Documents/"Claude Code"/parallaxx-transformations/migration
bash download-wix-assets.sh
```

It skips what it already has, so re-running after a failure is safe. It must
report `failed: 0` before you continue.

### 2b. Build and push

```bash
cd ~/Documents/"Claude Code"/parallaxx-transformations

python3 migration/build-site.py --local    # must print 10 pages, 0 missing assets
git add -A
git commit -m "Add Vercel build, asset localisation and legacy redirects"
git push
```

`--local` refuses to build if a single asset is missing, rather than shipping a
site with holes in it. `wix-assets/` is committed deliberately — Vercel builds
from the repo, so the images have to be in it.

### 2c. Connect Vercel

1. vercel.com → **Add New… → Project** → import `parallaxx-transformations`.
2. Framework preset: **Other**. Everything else is already in `vercel.json`
   (build command `python3 migration/build-site.py --local`, output `dist`).
3. Deploy. You get a `…vercel.app` URL.

### 2d. Test on the Vercel URL, before any DNS change

Walk all ten routes. Specifically check:

- Every image and video loads (they should now be `/assets/…`, not wixstatic).
- The **Priority Audit** advances — tap the first statement, the counter should
  move to "2 of 15". Test both `/priority-audit` and the in-page copy on `/women`.
- The **Reconnected Woman** apply buttons open the LeadConnector modal and the
  form is *visible* — not a 76px header with the form parked offscreen.
- The **archetype quiz** runs start to finish.
- Nav highlights the right item on each page, and the mobile burger opens.
- A few old URLs redirect: `/home`, `/what-is-your-archetype`, `/blog`,
  `/post/12-daily-rituals-for-success`.

All of the above was verified headlessly against a local build, but verify on
the real deploy too — the sandbox could not reach Google Fonts, GSAP or the
LeadConnector CDN, so those three ran unstyled or unloaded here.

---

## 3. DNS cutover

Only start this once section 2d passes.

### 3a. Add the domain in Vercel

Vercel project → **Settings → Domains** → add `parallaxxtransformations.com`
and `www.parallaxxtransformations.com`. Vercel will show the records it wants —
they should match the table below. Set `www` as the primary and let the apex
redirect to it, since every canonical URL currently uses `www`.

### 3b. Point the nameservers at Namecheap

Namecheap → Domain List → **Manage → Nameservers → Namecheap BasicDNS**.

**The moment you do this, every record Wix was serving disappears.** So build
the record set in Namecheap's Advanced DNS *first*, then flip the nameservers,
or accept an outage of everything in the table below.

### 3c. The complete record set

**Nine records. That is the whole job.**

A first pass at this listed far more, because a plain DNS lookup *chases*
CNAMEs: ask for the MX of `mail.parallaxxtransformations.com` and the resolver
follows the CNAME to `privateemail.com` and hands back **that** domain's MX
records as though they were yours. Querying Wix's nameservers directly shows
what is actually in the zone.

This matters practically, not just pedantically. A CNAME cannot legally coexist
with any other record at the same host — so recreating those inherited MX and
TXT entries alongside the CNAME would either be rejected by Namecheap or would
break the subdomain outright. **Create the CNAME and nothing else.**

Everything below was read from `ns14.wixdns.net` on 16 Aug 2026.

**Website — the only records that change**

| Type | Host | Value |
|---|---|---|
| A | `@` | take from Vercel — `76.76.21.21` unless your domain card says otherwise |
| CNAME | `www` | take from Vercel — **project-specific**, e.g. `d1d4fc829fe7bc7c.vercel-dns-017.com` |

Vercel no longer hands everyone the same `cname.vercel-dns.com`; each project
gets its own CNAME target. Copy both values out of the panel in step 3a rather
than from any guide, including this one.

These replace Wix's three apex A records and the `www → cdn1.wixdns.net` CNAME.

**Email — carry across exactly, or mail stops**

| Type | Host | Value | Priority |
|---|---|---|---|
| MX | `@` | `mx1.privateemail.com` | 10 |
| MX | `@` | `mx2.privateemail.com` | 20 |
| TXT | `@` | `v=spf1 include:spf.privateemail.com ~all` | |
| TXT | `default._domainkey` | the DKIM key — see `dns-records.txt`. One long line, must not wrap | |
| CNAME | `mail` | `privateemail.com` | |

**Subdomain — one CNAME, nothing more**

| Type | Host | Value | What it is |
|---|---|---|---|
| CNAME | `vault` | `school.teachable.com` | Teachable — your course platform |

`members` has been dropped. It still resolves, but the host answers with a
self-signed certificate so no browser will connect — nothing is being served.
Verified 17 Aug 2026. `dns-records.txt` keeps a note of the record it had, in
case the members area ever comes back.

**Verification — lose this and Search Console access goes with it**

| Type | Host | Value |
|---|---|---|
| TXT | `@` | `google-site-verification=P9B0bV6Xik_cuCNmaBzhB6FAlDcS32xDJGS1_Zv8Wvs` |

Do **not** recreate the two `google-site-verification` TXT records or the
`spf-nc.privateemail.com` SPF that appear under `mail`, and do not recreate the
mailgun SPF under `vault`. All four belong to Namecheap and Teachable
respectively, and arrive automatically with the CNAME.

Exact copy-paste values are in `dns-records.txt` next to this file.

### 3c-ii. What the subdomains need from you afterwards

Nothing, if the CNAMEs are right. But three things are worth knowing:

- **Do not add `vault` as a domain in Vercel.** Vercel owns the apex and `www`
  only. Adding the subdomain there would take it off Teachable.
- **Build the record before flipping the nameservers.** Teachable renews its TLS
  certificate by checking that the CNAME still points at it. A gap where the name
  does not resolve can fail a renewal and leave a certificate warning on the vault
  that outlasts the DNS outage that caused it.
- **Teachable keeps managing the certificate.** You do not issue or renew anything
  for `vault`; that stays with them, exactly as it works today.
- **The vault is live.** Confirmed 17 Aug 2026 — it serves "Welcome to The Vault
  of Transformations!". Worth stating plainly because it is the one subdomain
  that would fail silently: nothing on the main site breaks if you forget it.

### 3d. Timing and rollback

- Lower nothing's TTL — Wix does not let you, and the SOA minimum is 3600s.
  Expect **1–4 hours** for most people, up to 24 for stragglers.
- Do it on a **weekday morning**, not a Friday evening. If email breaks you want
  Namecheap support awake.
- **Rollback** is: set the nameservers back to `ns14.wixdns.net` /
  `ns15.wixdns.net`. This only works while the Wix plan is still active — which
  is the reason to cut over *before* the renewal date, not after it. Keep Wix
  paid until the new setup has been stable for a few days.

### 3e. After it propagates

- All ten pages load on the real domain over HTTPS (Vercel issues the cert
  automatically once DNS resolves — allow a few minutes).
- **Send yourself an email from an outside address and confirm it arrives.**
  Then send one out and check it is not landing in spam — that tests SPF/DKIM.
- `vault.parallaxxtransformations.com` loads.
- Google Search Console: submit `https://www.parallaxxtransformations.com/sitemap.xml`
  and watch Coverage for a fortnight.
- Only then cancel Wix.

---

## 4. Still outstanding

Known gaps, in the order they cost something.

1. **Contact has no page.** `/contact-daniel-lawson` is the only Wix-native page
   in the nav — it is on every page — and it is also the one in-body CTA outside
   the footer ("Start with a conversation"), 24 links in all. It currently 301s
   to `/`. `Parallaxx Contact.dc.html` is already authored in the repo and needs
   only a build script.
2. **Privacy policy and terms 301 to `/`.** Fine for now; a problem the moment
   any ad platform audits the site.
3. **Book-a-call 301s to `/`.** Point it at the LeadConnector booking URL
   directly — one line in `REDIRECTS`.
4. **`parallaxx-footer.js` is ahead of its source.** The committed bundle carries
   a phone-column fix that `PtFooter v3.dc.html` never received. Running
   `build-chrome-bundles.py` silently reverts it. Port the fix into the source
   before ever rebuilding that bundle.
5. **The footer still links to 8 pages that no longer exist.** They redirect
   rather than 404, so nothing is broken — but they are dead ends for the user.
6. **Lumios Marker was never uploaded.** Drop the `.woff2` into
   `wix-assets/font/` and restore the `@font-face`.
7. **Testimonial screenshots are still flattened PNGs.** Pre-existing; noted in
   `RECONNECTED-MAN-AUDIT.md`. Bad for SEO and unreadable to screen readers.
8. **No DMARC record.** Not required, but with DKIM and SPF already in place it
   is a cheap deliverability win once DNS is yours.

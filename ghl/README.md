# GHL pieces the site depends on

## Priority Audit email gate (9 Oct 2026)

The audit (/priority-audit and the copy on the women's home page) posts each
completion to a GHL inbound webhook: `CONFIG.leadEndpoint` in
`Priority Audit.dc.html` and `Parallaxx Home Women.dc.html`. Both must hold the
same URL (set 9 Oct 2026: workflow "Priority Audit - Results + Notification").
Rebuild with build-priority-audit-bundle.py and
build-home-women-bundle.py after changing it.

Fields sent (form-encoded), usable in the workflow as
`{{inboundWebhookRequest.<name>}}`:

- first_name, email, source (`priority-audit` or `women-home`)
- top_pillar, ranking, result_shape
- score_needs, score_boundaries, score_emotions
- rank1_name / rank1_score / rank1_pct / rank1_color (and rank2_, rank3_):
  the three in ranked order, for the results card
- results_url: /priority-audit?r=<15 answers>, rebuilds her exact result
- summary: plain-text block for Daniel's notification
- submitted_at

`priority-audit-results-email.html` is her results email, merge tags already
in GHL's inbound-webhook form. Paste it into the workflow's email action as
HTML. To change the wording, edit the plain sentences around the card; the
card itself is driven entirely by the rank fields.

### The GHL workflow (built and published 9 Oct 2026)

"Priority Audit - Results + Notification", in GHL under Automation >
Workflows (sub-account "Daniel Lawson"). Steps, in order:

1. Trigger: Inbound Webhook (premium trigger, billed per run). Its URL is
   the leadEndpoint above. Mapping reference = a sample request with all the
   fields listed here; re-pick a fresh sample if fields are ever added.
2. Create/update contact: Email and First name from the webhook.
3. Add tag `priority-audit`.
4. Add tag (dynamic) `pa-top-{{inboundWebhookRequest.top_pillar}}`.
5. Email her results: subject "Your Priority Audit results", body is
   priority-audit-results-email.html pasted into the editor's source view.
   Sent from the account default sender (daniel@reconnectyou.life).
6. Notify Daniel: internal notification email to parallaxxlifeco@gmail.com,
   subject "Priority Audit: <first name> - <top pillar>", body = summary.

Re-entry is on, so someone retaking the audit gets a fresh email each time.
Tested end to end 9 Oct with parallaxxlifeco+audittest@gmail.com (contact
"Testa" in GHL can be deleted).

## Archetype Quiz email gate (men, 9 Oct 2026)

The men's quiz (/the-archetype-quiz, source `protection-archetype-quiz.html`,
built with build-quiz-bundle.py into parallaxx-quiz.js) asks for first name +
email after question 22 and posts to its own inbound webhook:
`CONFIG.leadEndpoint` in protection-archetype-quiz.html.

Fields sent (form-encoded), as `{{inboundWebhookRequest.<name>}}`:

- first_name, email, source (`archetype-quiz`)
- archetype (display name), archetype_key (one of: `freedom`, `intellectual`, `idealist`, `performer`, `controlled`),
  secondary, ranking, notes (close top two, attention check)
- rank1_ ... rank5_ name / score (out of 20) / pct / color, ranked
- video_url (his archetype's video), results_url
  (/the-archetype-quiz?r=<22 answers>, rebuilds his exact result)
- summary (plain text incl. every answer, for Daniel), submitted_at

`archetype-quiz-results-email.html` is his results email (5-bar card).

### The GHL workflow (built and published 9 Oct 2026)

Webhook URL (the quiz's leadEndpoint):
https://services.leadconnectorhq.com/hooks/Nja8qXnwLqNjaNTJVf5T/webhook-trigger/EWUGJmwLhauwNNCtSrdb

"Archetype Quiz - Results + Notification" (a duplicate of the Priority Audit
workflow, so re-entry and the default sender carry over), mirrors the Priority Audit one:
Inbound Webhook > Create/update contact > tag `archetype-quiz` > dynamic tag
`aq-{{inboundWebhookRequest.archetype_key}}` > email his results (subject
"Your Protection Archetype results") > Notify Daniel (subject
"Archetype Quiz: <first name> - <archetype>", body = summary).

## Email template note (9 Oct 2026)

GHL wraps every table cell's text in its own 16px Verdana <p> when it saves an
email, which overrides cell font sizes and made the "14 / 20" scores stack on
phones. Both results templates now put each piece of text in a <span> with its
own size, and the score sits in a fixed 72px column as 14&nbsp;/&nbsp;20.
Keep that pattern for any new text inside the card. After editing a template,
paste it into the email action's source view (</>) and press Save on the
workflow itself too, since a published workflow needs that second save.

## Three Toxic Lies sign-up (free book, 15 Oct 2026)

/three-toxic-lies is a free download. Daniel chose a GHL form over a webhook
(15 Oct): the workflow triggers on Form Submitted, which is simpler to run.

THE FORM: Sites > Forms > "Three Toxic Lies - Free Book", id
`TDSyOXeH5838jtA7gx6S` (duplicated from "Insights subscribe"). It is embedded
twice on the page (hero, and beside the lies) as a plain iframe of
https://api.leadconnectorhq.com/widget/form/TDSyOXeH5838jtA7gx6S, no
form_embed.js. Fixed heights in toxic-lies-preview.html: 205px, 300px at
560px and under (room for the "required" notes).
- Fields: First name (required), Email (required), checkbox custom field
  "Weekly roundup" (query key `weekly_roundup`, field id sqjqPFq3imY1wkoAJ9Zq,
  one option "Also send me the weekly roundup of new insights.", unticked,
  not required), button "Send me the book".
- On submit: Settings > Redirect to URL
  https://www.parallaxxtransformations.com/three-toxic-lies/thank-you/ . The
  widget sets window.top.location, so the whole page goes, not the iframe.
- Styling: Styles > Advanced > Custom CSS. Dark inputs, coral uppercase
  button, Montserrat/Poppins via @import, first name and email side by side
  above ~370px of iframe. The last two rules repeat the input colours with
  `html body` in front: GHL's own input styles load after the custom CSS and
  win a tie. A copy of the CSS: ghl/three-toxic-lies-form.css.
- To change wording, fields or the redirect: edit the form in GHL. Nothing
  on the site needs rebuilding. If a field is added, check the iframe
  heights; the build guard (build_toxic_lies_bundle.py) checks the form id
  appears twice.

The book: https://www.parallaxxtransformations.com/assets/books/three-toxic-lies.pdf
(source file migration/wix-assets/books/three-toxic-lies.pdf, the 2026 edition).

Workflow to build (in GHL, Daniel's other chat): trigger Form Submitted, form
"Three Toxic Lies - Free Book" > tag `three-toxic-lies` > email the book
(link above; the thank-you page tells them to check Promotions and reply when
it arrives) > If/Else on the Weekly roundup field: only when ticked, start
the Insights double opt-in > Notify Daniel (he wants to know who grabs it).

## Thank-you pages, so GA4 can count sign-ups (30 Oct 2026)

GA4 can't see inside these iframe forms, so each form's on-submit is set to
Settings > Redirect to URL, sending the whole page to a page on the site that
fires GA4 `generate_lead` {form_name, source_page}. Pages live in
migration/landing.py (how to add one is in the comment above RW_THANKS).

| Form | id | Redirect to | form_name | Status |
|---|---|---|---|---|
| The Woman Application Form v2 | 0RT5EVaTlGxo6QBjyIPT | https://www.parallaxxtransformations.com/thanks/reconnected-woman/ | reconnected_woman | switched 30 Oct (replaced the old "you're in queue" message) |
| The Reconnected Man Application Form | UxzzQRv0AbKKQZ0P9bau | https://www.parallaxxtransformations.com/thanks/reconnected-man/ | reconnected_man | WAIT until the men's confirmation sequence is live |
| Three Toxic Lies - Free Book | TDSyOXeH5838jtA7gx6S | https://www.parallaxxtransformations.com/three-toxic-lies/thank-you/ (already set 15 Oct) | three_toxic_lies | done |
| Insights subscribe | EOwePM5iswFuXOj8p4ej | https://www.parallaxxtransformations.com/thanks/subscribed/ | insights_subscribe | switched 30 Oct, full-page redirect tested |

The women's form used to end on a GHL-hosted thank-you page carrying the
Priority Audit link; the new page carries that link as its one button.
The Insights page fires before the reader confirms by email (double opt-in),
so GA4 counts run higher than the confirmed `insights-subscriber` tag.

GA4 side (30 Oct 2026): custom dimensions Form name (form_name) and Source page
(source_page) registered, event scope. generate_lead can only be starred as a
key event once it has arrived (Admin > Data display > Events > Recent events).
Daniel's Chrome can't test GA4: a Chrome extension (id hnmpcagpplmpfojmgmnngilcnanddlhb)
swaps Google Analytics for a stub, so nothing from that browser reaches GA4.
Test on a phone or another browser, after opening any page with ?px-me=off.

Between sessions the circle thank-you pages switch themselves to a waiting-list
version (eyebrow "You're on the list", card "Date to be confirmed", step 1 "I'll
email you the date as soon as it is set"), matching the dateless waitlist email
GHL sends in the same gap. They return to "You're registered for <date>" when the
next date is set on the circle page and pushed. Wording: _LIST_STEP in landing.py.

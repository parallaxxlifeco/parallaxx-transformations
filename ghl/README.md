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

/three-toxic-lies is now a free download. Two identical forms (hero, and
beside the lies) post to a GHL inbound webhook: `TTL_CONFIG.leadEndpoint`
in toxic-lies-preview.html (in the page script). The browser then goes to
/three-toxic-lies/thank-you/ (built by migration/landing.py, TTL_THANKS).

STATUS when written: the webhook is NOT built yet, so leadEndpoint is ''.
build_toxic_lies_bundle.py refuses to build until it holds a GHL hook URL,
so parallaxx-toxic-lies.js (the live page) is still the old paperback page.
To go live: paste the hook URL into leadEndpoint, run
`python3 build_toxic_lies_bundle.py`, commit, push.

Fields sent (form-encoded), as `{{inboundWebhookRequest.<name>}}`:
- first_name, email
- source (`three-toxic-lies`)
- weekly_roundup (`yes` only if they ticked "Also send me the weekly roundup
  of new insights"; `no` otherwise). Only `yes` should start the Insights
  double opt-in. Nobody is added to the roundup otherwise.
- submitted_at

The book: https://www.parallaxxtransformations.com/assets/books/three-toxic-lies.pdf
(source file migration/wix-assets/books/three-toxic-lies.pdf, the 2026 edition).

Workflow to build: Inbound Webhook > Create/update contact > tag
`three-toxic-lies` > email the book (link above; thank-you page tells them to
check Promotions and reply when it arrives) > If weekly_roundup = yes, start
the Insights double opt-in > Notify Daniel (he wants to know who grabs it).

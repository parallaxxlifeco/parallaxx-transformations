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

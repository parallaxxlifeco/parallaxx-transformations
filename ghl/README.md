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

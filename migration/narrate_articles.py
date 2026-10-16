#!/usr/bin/env python3
"""Narrate the insights articles with ElevenLabs, one MP3 per article.

    python3 migration/narrate_articles.py --dry-run      # what would be sent, and how many characters
    python3 migration/narrate_articles.py                # narrate every article that is new or changed
    python3 migration/narrate_articles.py --only why-cant-i-stay-consistent

Writes migration/wix-assets/audio/<slug>.mp3, which the build copies to
/assets/audio/<slug>.mp3. Once a file exists, that article's Listen button
plays it instead of the browser's speech voice (articles.py, listen_bar). Commit
the MP3s and push like any other asset.

PAID ONCE PER ARTICLE. migration/wix-assets/audio/manifest.json keeps a hash of
the exact text each MP3 was made from, so a rerun skips everything unchanged and
only re-narrates an article whose words changed. Delete an entry to force it.

THE KEY NEVER GOES IN THE REPO. Put it in ~/.parallaxx-elevenlabs (outside the
repo), two lines:

    ELEVENLABS_API_KEY=...
    ELEVENLABS_VOICE_ID=...      # the cloned voice, from ElevenLabs > Voices

Environment variables of the same names win over the file.

The text sent is what the page's device voice reads, in the same order: the
title, the answer under it, then the body (headings, paragraphs, list items,
quotes, and table rows read as "Heading: cell."). Not the subscribe box or the
links at the end.
"""
import argparse, hashlib, html, json, os, re, sys, time, urllib.request, urllib.error
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import articles  # noqa: E402

CONTENT = HERE.parent / "content" / "insights"
OUT = HERE / "wix-assets" / "audio"
MANIFEST = OUT / "manifest.json"
MODEL = "eleven_multilingual_v2"
FORMAT = "mp3_44100_64"   # mono-ish speech quality, ~0.5 MB a minute
CHUNK = 4000               # characters per request, split on paragraph breaks


def load_keys():
    vals = {}
    f = Path.home() / ".parallaxx-elevenlabs"
    if f.exists():
        for line in f.read_text().splitlines():
            line = line.split("#", 1)[0].strip()
            if "=" in line:
                k, v = line.split("=", 1)
                vals[k.strip()] = v.strip()
    for k in ("ELEVENLABS_API_KEY", "ELEVENLABS_VOICE_ID"):
        if os.environ.get(k):
            vals[k] = os.environ[k]
    return vals.get("ELEVENLABS_API_KEY"), vals.get("ELEVENLABS_VOICE_ID")


def to_text(body_html):
    """The article body as spoken paragraphs, mirroring the page script."""
    out = []
    # tables first: rewrite each into "Heading: cell." lines
    def table(m):
        t = m.group(0)
        heads = [re.sub(r"<[^>]+>", "", h).strip() for h in re.findall(r"<th[^>]*>(.*?)</th>", t, re.S)]
        rows = []
        for tr in re.findall(r"<tr[^>]*>(.*?)</tr>", t, re.S):
            cells = [re.sub(r"<[^>]+>", "", c).strip() for c in re.findall(r"<td[^>]*>(.*?)</td>", tr, re.S)]
            if not cells:
                continue
            parts = []
            for k, c in enumerate(cells):
                h = heads[k] if k < len(heads) else ""
                h = (h[:1] + h[1:].lower() + ": ") if h else ""
                parts.append(h + c.rstrip(".") + ".")
            rows.append("<p>" + " ".join(parts) + "</p>")
        return "".join(rows)
    body_html = re.sub(r"<table.*?</table>", table, body_html, flags=re.S)
    for m in re.finditer(r"<(h2|h3|p|li)[^>]*>(.*?)</\1>", body_html, re.S):
        t = html.unescape(re.sub(r"<[^>]+>", "", m.group(2)))
        t = re.sub(r"\s+", " ", t).strip()
        if t:
            out.append(t)
    return out


def article_texts():
    for path in sorted(CONTENT.rglob("*.md")):
        if path.name.startswith("_"):
            continue
        meta, body_md = articles.parse_front_matter(path.read_text(encoding="utf-8"), str(path))
        body, _faq = articles.render_body(body_md, str(path))
        slug = meta.get("slug") or path.stem
        title = html.unescape(re.sub(r"<[^>]+>", "", meta["title"]))
        answer = html.unescape(re.sub(r"<[^>]+>", "", meta["answer"]))
        yield slug, [title, answer] + to_text(body)


def chunks(paras):
    cur, size = [], 0
    for p in paras:
        if cur and size + len(p) > CHUNK:
            yield "\n\n".join(cur)
            cur, size = [], 0
        cur.append(p)
        size += len(p) + 2
    if cur:
        yield "\n\n".join(cur)


def tts(key, voice, text, prev_text, next_text):
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice}?output_format={FORMAT}"
    body = {"text": text, "model_id": MODEL}
    # Stitching context, so the voice carries its intonation across chunks.
    if prev_text:
        body["previous_text"] = prev_text[-1000:]
    if next_text:
        body["next_text"] = next_text[:1000]
    req = urllib.request.Request(url, data=json.dumps(body).encode(), method="POST",
                                 headers={"xi-api-key": key, "Content-Type": "application/json",
                                          "Accept": "audio/mpeg"})
    for attempt in range(3):
        try:
            with urllib.request.urlopen(req, timeout=180) as r:
                return r.read()
        except urllib.error.HTTPError as e:
            msg = e.read().decode("utf-8", "replace")[:400]
            if e.code in (429, 500, 502, 503) and attempt < 2:
                time.sleep(5 * (attempt + 1))
                continue
            raise SystemExit(f"ElevenLabs said {e.code}: {msg}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--only", help="one article slug")
    args = ap.parse_args()

    manifest = json.loads(MANIFEST.read_text()) if MANIFEST.exists() else {}
    todo, total = [], 0
    for slug, paras in article_texts():
        if args.only and slug != args.only:
            continue
        text = "\n\n".join(paras)
        h = hashlib.sha256((MODEL + text).encode()).hexdigest()[:16]
        have = (OUT / f"{slug}.mp3").exists() and manifest.get(slug) == h
        state = "up to date" if have else "TO NARRATE"
        print(f"{state:11} {len(text):6} chars  {slug}")
        if not have:
            todo.append((slug, paras, h))
            total += len(text)
    print(f"\n{len(todo)} to narrate, {total:,} characters (roughly that many credits).")
    if args.dry_run or not todo:
        return

    key, voice = load_keys()
    if not key or not voice:
        raise SystemExit("No ElevenLabs key or voice id. See the top of this file.")
    OUT.mkdir(parents=True, exist_ok=True)
    for slug, paras, h in todo:
        parts = list(chunks(paras))
        audio = b""
        for k, part in enumerate(parts):
            print(f"  {slug}: part {k + 1}/{len(parts)}")
            audio += tts(key, voice, part,
                         parts[k - 1] if k else "", parts[k + 1] if k + 1 < len(parts) else "")
        (OUT / f"{slug}.mp3").write_bytes(audio)
        manifest[slug] = h
        MANIFEST.write_text(json.dumps(manifest, indent=1, sort_keys=True) + "\n")
        print(f"wrote {slug}.mp3  {len(audio) / 1e6:.1f} MB")
    print("\nNow rebuild, check one in the browser, commit migration/wix-assets/audio/, push.")


if __name__ == "__main__":
    main()

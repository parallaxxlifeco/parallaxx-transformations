#!/usr/bin/env python3
"""
harvest-wix.py — pull the content off every Wix-native page before it's gone.

WHY A SCRIPT RATHER THAN THE BROWSER
------------------------------------
The first attempt drove Chrome and used blob downloads. Chrome blocked 12 of the
14 files (it throttles multiple automatic downloads and refuses .sh outright), so
two arrived and the rest vanished silently. This does the same work with urllib
and writes straight to disk, where nothing can drop a file without saying so.

WHAT IT PRODUCES
----------------
  migration/harvested/*.html      one file per page: headings, paragraphs, lists,
                                  images and CTAs. No Wix styling, no nav, no
                                  footer. Structure and words, for the redesign.

  migration/download-wix-archive.sh   fetches the ORIGINAL of every image
                                  referenced anywhere on the Wix site.

Wix server-renders its pages, so a plain fetch gets the real content.

    python3 migration/harvest-wix.py

Run it BEFORE the Wix plan lapses. Afterwards none of these URLs answer.
"""

import html
import os
import re
import ssl
import sys
import urllib.request
from html.parser import HTMLParser

BASE = "https://www.parallaxxtransformations.com"
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "harvested")

# Pages worth keeping the words from. /facilitating is omitted: it already 404s
# on Wix, so the footer has been linking to a missing page for some time.
PAGES = [
    "/privacy-policy", "/terms-of-use", "/contact-daniel-lawson", "/reconnect",
    "/three-toxic-lies", "/daniel-lawson-as-seen-in",
    "/parallaxx-perspectives-podcast", "/reconnect-you-podcast-with-daniel-lawson",
    "/daniel-lawson-speaking", "/ptjournal", "/blog", "/your-identity-challenge",
    "/book-a-call-with-daniel-lawson", "/about-daniel-lawson", "/coaching-experiences",
    "/personal-leadership-resources", "/limitless-potential", "/free-guide",
    "/morning-mastery-club", "/elite-life-challenge",
]

KEEP = {"h1", "h2", "h3", "h4", "p", "li", "blockquote"}
DROP = {"script", "style", "noscript", "svg", "iframe", "nav", "header", "footer"}
# Nav and footer labels leak in even after dropping those elements, because Wix
# renders its chrome as plain divs. Filtered by exact text instead.
NOISE = {
    "Priority Audit", "SPEAKER", "EXPERIENCES", "RESOURCES", "ABOUT", "CONTACT",
    "HOME", "BLOG", "For Men", "For Women", "About", "Testimonials", "Contact",
    "PODCAST", "JOURNAL", "Book a call", "Menu",
}

CTX = ssl.create_default_context()
CTX.check_hostname = False
CTX.verify_mode = ssl.CERT_NONE


def fetch(url):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=45, context=CTX) as r:
        return r.read().decode("utf-8", "replace")


class Extract(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.stack, self.skip = [], 0
        self.buf, self.blocks, self.seen = [], [], set()
        self.title, self.desc, self.in_title = "", "", False

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag in DROP:
            self.skip += 1
            return
        if self.skip:
            return
        if tag == "title":
            self.in_title = True
        if tag == "meta" and a.get("name") == "description":
            self.desc = a.get("content", "")
        if tag == "img":
            src = (a.get("src") or "").split("?")[0]
            if src and "data:" not in src and "logo" not in src.lower():
                key = src.split("/v1/")[0]
                if key not in self.seen:
                    self.seen.add(key)
                    self.blocks.append(("img", src, a.get("alt", "")))
        if tag == "a":
            self.stack.append(("a", a.get("href", "")))
            self.buf = []
        elif tag in KEEP:
            self.stack.append((tag, None))
            self.buf = []

    def handle_endtag(self, tag):
        if tag in DROP:
            self.skip = max(0, self.skip - 1)
            return
        if self.skip:
            return
        if tag == "title":
            self.in_title = False
        if not self.stack or self.stack[-1][0] != tag:
            return
        name, href = self.stack.pop()
        text = re.sub(r"\s+", " ", "".join(self.buf)).strip()
        self.buf = []
        if not text or text in NOISE or len(text) < 3:
            return
        if name == "a":
            if href.startswith("http") and len(text) >= 4:
                k = "a:" + href + text
                if k not in self.seen:
                    self.seen.add(k)
                    self.blocks.append(("link", href, text))
            return
        if name == "li" and len(text) < 25:
            return
        if text in self.seen:
            return
        self.seen.add(text)
        self.blocks.append((name, text, None))

    def handle_data(self, d):
        if self.in_title:
            self.title += d
        if not self.skip and self.stack:
            self.buf.append(d)


def build(path, page):
    e = Extract()
    e.feed(page)
    parts = []
    for kind, a, b in e.blocks:
        if kind == "img":
            parts.append(f'  <figure>\n    <img src="{html.escape(a)}" '
                         f'alt="{html.escape(b or "")}">\n  </figure>')
        elif kind == "link":
            parts.append(f'  <!-- link: <a href="{html.escape(a)}">'
                         f'{html.escape(b)}</a> -->')
        else:
            parts.append(f"  <{kind}>{html.escape(a)}</{kind}>")
    return (
        "<!DOCTYPE html>\n<html lang=\"en\">\n<head>\n<meta charset=\"utf-8\">\n"
        "<!-- HARVESTED FROM WIX - content only, no styling.\n"
        f"     Source: {BASE}{path}\n"
        "     Raw material for the redesign, not a page to ship. -->\n"
        f"<title>{html.escape(e.title.strip())}</title>\n"
        f"<meta name=\"description\" content=\"{html.escape(e.desc)}\">\n"
        "</head>\n<body>\n"
        f"<!-- ORIGINAL PATH: {path} -->\n" + "\n".join(parts) + "\n</body>\n</html>\n"
    ), len(parts)


def main():
    os.makedirs(OUT, exist_ok=True)
    media = {}
    print("Harvesting pages\n" + "-" * 58)
    for p in PAGES:
        try:
            page = fetch(BASE + p)
        except Exception as ex:
            print(f"  SKIP  {p:<46} {str(ex)[:22]}")
            continue
        doc, n = build(p, page)
        name = "harvested" + p.replace("/", "-") + ".html"
        with open(os.path.join(OUT, name), "w", encoding="utf-8") as f:
            f.write(doc)
        print(f"  ok    {name:<50} {n} blocks")
        for u in re.findall(r"https://static\.wixstatic\.com/media/[^\"'\\\s)]+", page):
            m = re.match(r".*/media/([A-Za-z0-9_~.-]+?)(?:/v1/|$)", u)
            if m and re.search(r"\.(jpg|jpeg|png|webp|gif|avif)$", m.group(1), re.I):
                media.setdefault(m.group(1), "https://static.wixstatic.com/media/" + m.group(1))

    # Sweep every sitemap URL too, so the archive covers pages we are not
    # keeping the words from.
    try:
        sm = fetch(BASE + "/pages-sitemap.xml")
        extra = [u for u in re.findall(r"<loc>([^<]+)</loc>", sm)]
        print(f"\nSweeping {len(extra)} sitemap URLs for images")
        for u in extra:
            try:
                page = fetch(u)
            except Exception:
                continue
            for m in re.findall(r"https://static\.wixstatic\.com/media/[^\"'\\\s)]+", page):
                mm = re.match(r".*/media/([A-Za-z0-9_~.-]+?)(?:/v1/|$)", m)
                if mm and re.search(r"\.(jpg|jpeg|png|webp|gif|avif)$", mm.group(1), re.I):
                    media.setdefault(mm.group(1), "https://static.wixstatic.com/media/" + mm.group(1))
    except Exception as ex:
        print("  sitemap sweep failed:", str(ex)[:60])

    used, lines = set(), []
    for mid, url in sorted(media.items()):
        base = re.sub(r"~mv2", "", mid)
        base = re.sub(r"^e1784d_", "logo-", base)
        base = re.sub(r"^111174_", "", base)
        base = re.sub(r"[^A-Za-z0-9._-]", "-", base)
        nm, i = base, 2
        while nm in used:
            d = nm.rfind(".")
            nm = f"{base[:d]}-{i}{base[d:]}"
            i += 1
        used.add(nm)
        lines.append(f'dl "{url}" "{nm}"')

    sh = f"""#!/usr/bin/env bash
# Every image referenced anywhere on the Wix site, at ORIGINAL size.
# {len(lines)} distinct files, generated by harvest-wix.py.
#
# Separate from wix-assets/, which holds the files the live site depends on and
# is already committed. This is the archive: images referenced only from
# Wix-native pages being retired. Run it BEFORE the Wix plan lapses.
set -u
cd "$(dirname "$0")"
mkdir -p wix-archive
ok=0; fail=0
dl(){{
  local url="$1" out="wix-archive/$2"
  if [ -s "$out" ]; then ok=$((ok+1)); return; fi
  if curl -fsSL --retry 2 --retry-delay 1 -A "Mozilla/5.0" "$url" -o "$out"; then
    printf "ok    %-50s %s\\n" "$2" "$(du -h "$out" | cut -f1)"; ok=$((ok+1))
  else
    printf "FAIL  %-50s\\n" "$2"; rm -f "$out"; fail=$((fail+1))
  fi
}}

{chr(10).join(lines)}

echo
echo "=============================="
echo "downloaded: $ok"
echo "failed:     $fail"
echo "size:       $(du -sh wix-archive | cut -f1)"
echo "=============================="
"""
    p = os.path.join(HERE, "download-wix-archive.sh")
    with open(p, "w", encoding="utf-8") as f:
        f.write(sh)
    os.chmod(p, 0o755)
    print(f"\nWrote {len(lines)} image URLs to download-wix-archive.sh")
    print("Next:  bash migration/download-wix-archive.sh")


if __name__ == "__main__":
    sys.exit(main())

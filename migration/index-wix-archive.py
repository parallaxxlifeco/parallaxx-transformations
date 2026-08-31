#!/usr/bin/env python3
"""
index-wix-archive.py — make the image archive usable.

TWO PROBLEMS THIS FIXES
-----------------------
1. 122 of the 183 files are called "logo-<hash>". That was my bug: Wix prefixes
   every asset in this account with e1784d_, and the download script mistook
   that for a logo marker. Almost none of them are logos - one is a 13MB
   photograph. The prefix is stripped here.

2. Even correctly named, 183 files called <hash>.jpg are unusable. You cannot
   find the hero image for the Reconnect page by looking at them. So this
   crawls the Wix site again and records WHERE each image appears, with its
   alt text, and writes that to a manifest you can search.

    python3 migration/index-wix-archive.py

Safe to re-run. Renames are skipped if the target already exists.
Run it while Wix is still up - the page mapping needs the live site.
"""

import csv
import os
import re
import ssl
import urllib.request
from collections import defaultdict

BASE = "https://www.parallaxxtransformations.com"
HERE = os.path.dirname(os.path.abspath(__file__))
ARCHIVE = os.path.join(HERE, "wix-archive")

CTX = ssl.create_default_context()
CTX.check_hostname = False
CTX.verify_mode = ssl.CERT_NONE


def fetch(url):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=45, context=CTX) as r:
        return r.read().decode("utf-8", "replace")


def main():
    if not os.path.isdir(ARCHIVE):
        raise SystemExit("No wix-archive/ - run download-wix-archive.sh first.")

    # ---- 1. strip the bogus logo- prefix -------------------------------------
    renamed = 0
    for name in sorted(os.listdir(ARCHIVE)):
        if not name.startswith("logo-"):
            continue
        new = name[5:]
        src, dst = os.path.join(ARCHIVE, name), os.path.join(ARCHIVE, new)
        if os.path.exists(dst):
            continue
        os.rename(src, dst)
        renamed += 1
    print(f"renamed {renamed} files (dropped the incorrect 'logo-' prefix)")

    # ---- 2. map every media id to the pages that use it ----------------------
    try:
        sm = fetch(BASE + "/pages-sitemap.xml")
    except Exception as ex:
        raise SystemExit(f"Could not read the sitemap ({ex}). Is Wix still live?")
    urls = re.findall(r"<loc>([^<]+)</loc>", sm)
    print(f"crawling {len(urls)} pages to map images to pages")

    uses = defaultdict(set)
    alts = {}
    for u in urls:
        try:
            page = fetch(u)
        except Exception:
            continue
        path = re.sub(r"^https?://[^/]+", "", u) or "/"
        for m in re.findall(r"https://static\.wixstatic\.com/media/([A-Za-z0-9_~.-]+?)(?:/v1/|[\"'\\\s)])", page):
            if re.search(r"\.(jpg|jpeg|png|webp|gif|avif)$", m, re.I):
                uses[m].add(path)
        # alt text sits next to the src in the same tag
        for tag in re.findall(r"<img[^>]+>", page):
            src = re.search(r"media/([A-Za-z0-9_~.-]+?)(?:/v1/|[\"'])", tag)
            alt = re.search(r'alt="([^"]*)"', tag)
            if src and alt and alt.group(1).strip():
                alts.setdefault(src.group(1), alt.group(1).strip()[:120])

    # ---- 3. write the manifest ----------------------------------------------
    on_disk = set(os.listdir(ARCHIVE))
    rows = []
    for mid, pages in sorted(uses.items()):
        fname = re.sub(r"~mv2", "", mid)
        fname = re.sub(r"^e1784d_", "", fname)
        fname = re.sub(r"^111174_", "", fname)
        fname = re.sub(r"[^A-Za-z0-9._-]", "-", fname)
        size = ""
        if fname in on_disk:
            size = f"{os.path.getsize(os.path.join(ARCHIVE, fname)) // 1024}KB"
        rows.append({
            "file": fname,
            "on_disk": "yes" if fname in on_disk else "NO",
            "size": size,
            "used_on": " ".join(sorted(pages)),
            "alt": alts.get(mid, ""),
        })

    csv_path = os.path.join(HERE, "wix-archive-manifest.csv")
    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["file", "on_disk", "size", "used_on", "alt"])
        w.writeheader()
        w.writerows(rows)

    by_page = defaultdict(list)
    for r in rows:
        for p in r["used_on"].split():
            by_page[p].append(r)
    md = ["# Wix image archive — what appears where", "",
          f"{len(rows)} images across {len(by_page)} pages. Files are in `wix-archive/`.",
          "Full detail including alt text is in `wix-archive-manifest.csv`.", ""]
    for p in sorted(by_page, key=lambda k: -len(by_page[k])):
        md.append(f"## {p}  ({len(by_page[p])} images)")
        md.append("")
        for r in sorted(by_page[p], key=lambda r: r["file"]):
            note = f" — {r['alt']}" if r["alt"] else ""
            md.append(f"- `{r['file']}` {r['size']}{note}")
        md.append("")
    md_path = os.path.join(HERE, "wix-archive-manifest.md")
    with open(md_path, "w", encoding="utf-8") as f:
        f.write("\n".join(md))

    missing = sum(1 for r in rows if r["on_disk"] == "NO")
    print(f"\nmapped   {len(rows)} images across {len(by_page)} pages")
    if missing:
        print(f"WARNING  {missing} referenced images are not on disk")
    print(f"wrote    wix-archive-manifest.csv")
    print(f"wrote    wix-archive-manifest.md   <- start here")


if __name__ == "__main__":
    main()

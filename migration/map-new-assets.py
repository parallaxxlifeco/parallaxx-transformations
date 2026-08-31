#!/usr/bin/env python3
"""
map-new-assets.py -- find Wix-hosted images a new page introduced, copy them
out of the archive, and register them in asset-map.json.

    python3 map-new-assets.py "../Parallaxx As Seen In.dc.html"          # report
    python3 map-new-assets.py "../Parallaxx As Seen In.dc.html" --apply  # do it

WHY THIS EXISTS
asset-map.json was built once, from the ten bundles that existed at the time.
Every page added since then can reference static.wixstatic.com URLs that are
not in that map -- and `build-site.py --local` only rewrites URLs it finds
there. Anything missing is left pointing at Wix and keeps working right up
until the subscription lapses, at which point the image disappears and nothing
in the build ever said a word about it.

The As Seen In page introduced eight of them in one go: the podcast cover art.
That is what prompted this script. Run it whenever a new page brings in
imagery that came off the old site.

WHAT IT DOES
  1. Pulls every static.wixstatic.com URL out of the files you name.
  2. Skips the ones already in asset-map.json.
  3. For each one left, finds the original in wix-archive/ by its media hash --
     the archive is named by hash, and a Wix URL carries the same hash whatever
     transform is appended to it.
  4. Names the local copy from the <img alt> on the same tag, slugified, which
     is how you get 'the-relentless-education-podcast.jpeg' instead of
     'wix-4557448fd3b64dc4bdd15c46ec502ee7.jpeg'. Falls back to the hash when
     there is no usable alt.
  5. With --apply: copies into wix-assets/img/ and appends to asset-map.json.

IT MAPS THE EXACT URL STRING, TRANSFORM AND ALL. build-site.py matches URLs
literally, longest first. Registering the bare media URL instead of the
transform variant that is actually in the markup would silently miss.

NOTHING IS OVERWRITTEN. A name that already exists in wix-assets/img/ gets a
numeric suffix, and an existing map entry is never rewritten -- if a URL is
already mapped, it is left exactly as it is.
"""
import json, re, shutil, sys, unicodedata, pathlib

HERE   = pathlib.Path(__file__).resolve().parent
MAP    = HERE / "asset-map.json"
ARCH   = HERE / "wix-archive"
IMGDIR = HERE / "wix-assets" / "img"

# EXTRACT FROM THE ATTRIBUTE, NOT FROM THE PROSE. The first version of this
# script used a character class that excluded ')' -- reasonable-looking, because
# a URL inside CSS url(...) has to stop at the bracket. But Wix names its media
# after the file somebody uploaded, and those filenames have brackets in them:
# 'Square Daniel (20).png', 'Daniel Lawson Thumbnail (1).png', 'contier (1).png'.
# So two of the first eight URLs were silently cut at the '(' and registered
# half-length. build-site.py then replaced the half it knew and left the rest,
# producing src="/assets/img/the-choice-effect.png).png" -- a broken image that
# every check short of actually rendering the page reported as fine.
# Matching inside the quotes cannot truncate, because the quote is the delimiter.
ATTR_RE = re.compile(r'(?:src|href|content)="(https://static\.wixstatic\.com/[^"]+)"')
OK_EXT  = (".jpg", ".jpeg", ".png", ".webp", ".gif", ".svg", ".avif", ".mp4", ".webm")
IMG_RE = re.compile(r'<img[^>]*>', re.I)
# The media hash is the 32 hex characters in the first path segment, with or
# without the account prefix that Wix puts in front of it.
HASH_RE = re.compile(r'/media/(?:[0-9a-z]+_)?([0-9a-f]{32})')


def slug(s: str) -> str:
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode()
    s = re.sub(r"[^A-Za-z0-9]+", "-", s).strip("-").lower()
    return re.sub(r"-{2,}", "-", s)[:56]


def alt_for(text: str, url: str) -> str:
    """The alt on the same <img> tag as this URL, if there is one."""
    for tag in IMG_RE.findall(text):
        if url in tag:
            m = re.search(r'\balt="([^"]*)"', tag)
            if m and m.group(1).strip():
                return m.group(1).strip()
    return ""


def main() -> int:
    files = [a for a in sys.argv[1:] if not a.startswith("--")]
    apply_ = "--apply" in sys.argv
    if not files:
        print(__doc__.strip().split("\n\n")[1])
        return 1

    amap = json.loads(MAP.read_text())
    mapped = {r["url"] for r in amap}
    taken = {r["file"] for r in amap} | {
        "img/" + p.name for p in IMGDIR.iterdir() if p.is_file()}

    found, todo = 0, []
    for f in files:
        p = pathlib.Path(f)
        if not p.exists():
            print("ERROR: no such file: %s" % f)
            return 1
        text = p.read_text(encoding="utf-8")
        for url in dict.fromkeys(ATTR_RE.findall(text)):
            found += 1
            if url in mapped:
                continue
            if not url.lower().endswith(OK_EXT):
                print("SKIP  url does not end in a file extension, so it is "
                      "probably truncated. Not registering it:")
                print("      %s" % url)
                continue
            h = HASH_RE.search(url)
            if not h:
                print("SKIP  no media hash in url: %s" % url[:100])
                continue
            hits = sorted(ARCH.glob(h.group(1) + ".*"))
            if not hits:
                print("MISS  not in wix-archive/: %s" % h.group(1))
                print("      %s" % url[:110])
                continue
            src = hits[0]
            base = slug(alt_for(text, url)) or ("wix-" + h.group(1)[:12])
            name = "img/%s%s" % (base, src.suffix)
            n = 2
            while name in taken:
                name = "img/%s-%d%s" % (base, n, src.suffix)
                n += 1
            taken.add(name)
            todo.append(dict(url=url, file=name, src=str(src.relative_to(HERE))))

    print("\n%d Wix URL(s) referenced, %d already mapped, %d to add\n"
          % (found, found - len(todo), len(todo)))
    for r in todo:
        print("  %-46s <- %s" % (r["file"], pathlib.Path(r["src"]).name))

    if not todo:
        print("\nNothing to do.")
        return 0
    if not apply_:
        print("\nDry run. Re-run with --apply to copy the files and write the map.")
        return 0

    for r in todo:
        shutil.copy2(HERE / r["src"], IMGDIR / pathlib.Path(r["file"]).name)
        amap.append(dict(url=r["url"], file=r["file"], src=r["src"]))
    MAP.write_text(json.dumps(amap, indent=2) + "\n")
    print("\nCopied %d file(s) into wix-assets/img/ and added them to "
          "asset-map.json (%d entries now)." % (len(todo), len(amap)))
    print("Run: python3 migration/build-site.py --local   to confirm 0 missing.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

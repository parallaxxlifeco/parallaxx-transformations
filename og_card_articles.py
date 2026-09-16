"""Build the share card for every /insights/ article that declares one.

Same ground, type and logo block as og_card_journal.py, og_card_man.py and
og_card_toxic_lies.py, so the set reads as one family. What differs is what
carries the card: those are pages with a product or a promise on them, and an
article has neither. It has a line.

WHY THE LINE AND NOT THE TITLE
------------------------------
On LinkedIn the card sits directly above the og:title. Put the question on both
and the best real estate on the post says one sentence twice. So the image
carries a line lifted from the article's own prose and the title carries the
question, and the two do different work.

The line comes from an optional `card:` key in the article's front matter. No
card line, no PNG, and the article falls back to the site's default og image —
nothing breaks, the preview is just generic.

HOW IT FITS THE BUILD
---------------------
Run from the repo root. Writes into migration/wix-assets/img/, which is where
build-site.py --local reads og images from, so the PNG has to be committed like
any other asset. Pillow is NOT a build dependency and must not become one: the
Cloudflare Pages image is not this repo's to guarantee, and a deploy is a bad
place to discover a missing library. build-site.py warns when an article
declares a card line and its PNG is missing, so the two cannot drift silently.

    python3 og_card_articles.py
"""
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import pathlib
import re

W, H = 1200, 630
NAVY = (4, 18, 42)
CARD = (10, 29, 60)
GOLD = (232, 198, 95)
CREAM = (255, 255, 255)
MIST = (177, 191, 215)
SLATE = (124, 137, 163)

F = "/usr/share/fonts/truetype/google-fonts/Poppins-%s.ttf"
def f(style, size): return ImageFont.truetype(F % style, size)

CONTENT = pathlib.Path("content/insights")
OUTDIR = pathlib.Path("migration/wix-assets/img")

PILLAR_NAMES = {
    "knowing-and-not-doing": "KNOWING YOUR PATTERN",
    "being-the-capable-one": "BEING THE CAPABLE ONE",
    "not-knowing-what-you-want": "NOT KNOWING WHAT YOU WANT",
    "getting-what-you-wanted": "GETTING WHAT YOU WANTED",
    "what-the-work-costs": "WHAT IT COSTS",
}


def track(draw, xy, text, font, fill, sp=0.0):
    """Letter-spaced text. The house style tracks every small-caps line."""
    x, y = xy
    for c in text:
        draw.text((x, y), c, font=font, fill=fill)
        x += draw.textlength(c, font=font) + sp


def wrap(draw, text, font, max_w):
    lines, line = [], ""
    for word in text.split():
        trial = (line + " " + word).strip()
        if draw.textlength(trial, font=font) <= max_w or not line:
            line = trial
        else:
            lines.append(line)
            line = word
    if line:
        lines.append(line)
    return lines


def fit(draw, text, max_w, max_lines=4):
    """Largest size at which the line fits the box. Long lines get smaller
    type rather than a smaller card or a truncated sentence."""
    for size in range(58, 25, -2):
        font = f("Bold", size)
        lines = wrap(draw, text, font, max_w)
        if len(lines) <= max_lines:
            return font, lines, size
    font = f("Bold", 26)
    return font, wrap(draw, text, font, max_w)[:max_lines], 26


def ground():
    img = Image.new("RGB", (W, H), NAVY)
    glow = Image.new("L", (W, H), 0)
    gd = ImageDraw.Draw(glow)
    gd.ellipse((W * 0.10, -H * 0.34, W * 0.78, H * 1.14), fill=150)
    glow = glow.filter(ImageFilter.GaussianBlur(120))
    img = Image.composite(Image.new("RGB", (W, H), CARD), img, glow)

    d = ImageDraw.Draw(img, "RGBA")
    for x in range(-H, W + H, 150):
        d.line([(x, 0), (x + H, H)], fill=(255, 255, 255, 7), width=1)
    d.line([(1105, 30), (1155, 30)], fill=GOLD + (110,), width=1)
    d.line([(1155, 30), (1155, 95)], fill=GOLD + (110,), width=1)
    d.line([(44, 528), (44, 548)], fill=GOLD + (150,), width=2)

    d.rectangle((44, 38, 216, 87), outline=(255, 255, 255, 70), width=1)
    track(d, (62, 47), "PARALLAXX", f("Bold", 17), CREAM, sp=1.6)
    track(d, (62, 70), "TRANSFORMATIONS", f("Bold", 8), GOLD, sp=1.9)
    return img, d


def front_matter(path):
    raw = path.read_text(encoding="utf-8")
    if not raw.startswith("---\n"):
        return {}
    _, fm, _ = raw.split("---\n", 2)
    meta = {}
    for line in fm.strip().split("\n"):
        if ":" in line:
            k, v = line.split(":", 1)
            meta[k.strip()] = v.strip()
    return meta


def build_card(meta, slug):
    img, d = ground()
    eyebrow = PILLAR_NAMES.get(meta.get("pillar", ""), "INSIGHTS")
    track(d, (56, 214), eyebrow, f("Bold", 12), GOLD, sp=2.4)

    font, lines, size = fit(d, meta["card"], max_w=1010)
    y = 248
    for line in lines:
        d.text((54, y), line, font=font, fill=CREAM)
        y += round(size * 1.18)

    d.line([(56, 496), (560, 496)], fill=(255, 255, 255, 40), width=1)
    track(d, (56, 516), "PARALLAXXTRANSFORMATIONS.COM  ·  INSIGHTS",
          f("Bold", 13), SLATE, sp=3.0)

    out = OUTDIR / f"og-{slug}.png"
    img.save(out)
    return out, size, len(lines)


def main():
    if not CONTENT.is_dir():
        print("no content/insights/ — nothing to do")
        return
    made = skipped = 0
    for path in sorted(CONTENT.rglob("*.md")):
        if path.name == "_hub.md":
            continue
        meta = front_matter(path)
        slug = meta.get("slug") or path.stem
        if not meta.get("card"):
            print(f"  no card line, skipped   {slug}")
            skipped += 1
            continue
        out, size, n = build_card(meta, slug)
        print(f"  written {out.name:52} {size}px, {n} line(s)")
        made += 1
    print(f"\n{made} card(s) written, {skipped} skipped. "
          f"Commit the PNGs — build-site.py --local reads them from wix-assets/.")


if __name__ == "__main__":
    main()

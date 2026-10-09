"""Build a 9:16 Instagram Story card for /insights/ articles that declare a card line.

Sibling of og_card_articles.py: same navy ground, gold tracking, Poppins and logo
block, so a story, the LinkedIn preview and the page read as one family. The story
carries the article's `card:` line large, the question it answers underneath, and
a clear band under the card for the link sticker. The card is rounded and floats
on a darker ground, the way Instagram shows a shared post, which Daniel adds on his phone.

WHY THE PHONE
-------------
instagram.com on desktop cannot post Stories at all, and Meta Business Suite (which
can) is ruled out in Daniel's posting rules. So this only makes the image and prints
the live URL. Posting is: open the image on the phone, Story, link sticker, paste.

WHERE IT WRITES
---------------
_working/story-cards/, which is gitignored. Stories are not site assets and this
repo is public, so nothing here is ever committed or deployed.

    python3 og_story_articles.py              # every article with a card line
    python3 og_story_articles.py <slug> ...   # just these
"""
from PIL import Image, ImageDraw, ImageFilter
import pathlib
import sys

from og_card_articles import (NAVY, CARD, GOLD, CREAM, MIST, SLATE, f, track,
                              wrap, front_matter, PILLAR_NAMES, CONTENT)

W, H = 1080, 1920
ORIGIN = "https://www.parallaxxtransformations.com"
OUTDIR = pathlib.Path("_working/story-cards")

# The article card floats on the story as a rounded card, the way Instagram shows a
# shared post. Instagram draws its own UI over roughly the top 250px and the bottom
# 300px, so the card and the sticker band both sit between those.
CX0, CY0, CX1, CY1 = 44, 228, 1036, 1330
RADIUS = 46
PAD = 56
CW, CH = CX1 - CX0, CY1 - CY0
MAXW = CW - 2 * PAD
OUTER = (2, 9, 23)
SAFE_BOTTOM = 1620


def balanced(draw, text, font, max_w):
    """Wrap, then narrow the measure until the last line carries at least two words,
    without adding a line. A word stranded on its own line is not allowed on covers."""
    lines = wrap(draw, text, font, max_w)
    if len(lines) < 2 or len(lines[-1].split()) > 1:
        return lines
    w = max_w
    while w > max_w * 0.6:
        w -= 12
        trial = wrap(draw, text, font, w)
        if len(trial) > len(lines):
            break
        if len(trial[-1].split()) > 1:
            return trial
    return lines


def layout(draw, card, question, avail):
    """Largest card size at which eyebrow + card line + rule + question fit `avail`."""
    qfont = f("Medium", 38)
    qlines = balanced(draw, question, qfont, MAXW)[:3]
    fallback = None
    for size in range(92, 47, -4):
        font = f("Bold", size)
        # try every measure from full width down before giving up on this size, so a
        # stranded last word is fixed by a different break, not by shrinking the type
        w = MAXW
        while w > MAXW * 0.6:
            lines = wrap(draw, card, font, w)
            block = 66 + len(lines) * round(size * 1.2) + 80 + len(qlines) * 54
            if block <= avail:
                if len(lines) < 2 or len(lines[-1].split()) > 1:
                    return font, lines, size, qfont, qlines, block, True
                fallback = fallback or (font, lines, size, qfont, qlines, block, True)
            w -= 12
    if fallback:
        return fallback
    font = f("Bold", 48)
    lines = wrap(draw, card, font, MAXW)
    block = 66 + len(lines) * round(48 * 1.2) + 80 + len(qlines) * 54
    return font, lines, 48, qfont, qlines, block, False


def card_ground():
    img = Image.new("RGB", (CW, CH), NAVY)
    glow = Image.new("L", (CW, CH), 0)
    ImageDraw.Draw(glow).ellipse((-CW * 0.3, -CH * 0.05, CW * 1.05, CH * 0.85), fill=150)
    glow = glow.filter(ImageFilter.GaussianBlur(150))
    img = Image.composite(Image.new("RGB", (CW, CH), CARD), img, glow)
    d = ImageDraw.Draw(img, "RGBA")
    for x in range(-CH, CW + CH, 160):
        d.line([(x, 0), (x + CH, CH)], fill=(255, 255, 255, 7), width=1)
    # corner bracket and logo block
    d.line([(CW - 150, 56), (CW - 70, 56)], fill=GOLD + (110,), width=2)
    d.line([(CW - 70, 56), (CW - 70, 150)], fill=GOLD + (110,), width=2)
    d.rectangle((PAD, 56, PAD + 330, 150), outline=(255, 255, 255, 70), width=2)
    track(d, (PAD + 34, 72), "PARALLAXX", f("Bold", 32), CREAM, sp=3.0)
    track(d, (PAD + 34, 116), "TRANSFORMATIONS", f("Bold", 15), GOLD, sp=3.6)
    return img, d


def rounded_mask(w, h, r, scale=4):
    m = Image.new("L", (w * scale, h * scale), 0)
    ImageDraw.Draw(m).rounded_rectangle((0, 0, w * scale - 1, h * scale - 1), r * scale, fill=255)
    return m.resize((w, h), Image.LANCZOS)


def build_story(meta, slug):
    card, d = card_ground()
    eyebrow = PILLAR_NAMES.get(meta.get("pillar", ""), "INSIGHTS")
    q = meta.get("question") or meta.get("title", "")
    top, bottom = 214, CH - 130          # text area inside the card
    font, lines, size, qfont, qlines, block, ok = layout(d, meta["card"], q, bottom - top)
    y = top + max(0, (bottom - top - block) // 2)
    track(d, (PAD + 2, y), eyebrow, f("Bold", 23), GOLD, sp=4.4)
    y += 66
    for line in lines:
        d.text((PAD, y), line, font=font, fill=CREAM)
        y += round(size * 1.2)
    y += 38
    d.line([(PAD + 2, y), (PAD + 240, y)], fill=GOLD + (170,), width=3)
    y += 42
    for line in qlines:
        d.text((PAD, y), line, font=qfont, fill=MIST)
        y += 54
    d.line([(PAD, CH - 96), (CW - PAD, CH - 96)], fill=(255, 255, 255, 30), width=1)
    track(d, (PAD + 2, CH - 72), "PARALLAXXTRANSFORMATIONS.COM  ·  INSIGHTS",
          f("Bold", 18), SLATE, sp=3.8)

    # the story: dark ground, soft shadow, rounded card, hairline edge
    story = Image.new("RGB", (W, H), OUTER)
    sd = ImageDraw.Draw(story, "RGBA")
    for x in range(-H, W + H, 170):
        sd.line([(x, 0), (x + H, H)], fill=(255, 255, 255, 5), width=1)
    shadow = Image.new("L", (W, H), 0)
    ImageDraw.Draw(shadow).rounded_rectangle((CX0, CY0 + 18, CX1, CY1 + 18), RADIUS, fill=170)
    shadow = shadow.filter(ImageFilter.GaussianBlur(28))
    story = Image.composite(Image.new("RGB", (W, H), (0, 0, 0)), story, shadow)
    story.paste(card, (CX0, CY0), rounded_mask(CW, CH, RADIUS))
    sd = ImageDraw.Draw(story, "RGBA")
    sd.rounded_rectangle((CX0, CY0, CX1 - 1, CY1 - 1), RADIUS, outline=(255, 255, 255, 38), width=2)

    # the band the link sticker goes in: cue under the card, clear space below it
    cue, cfont, csp = "READ THE FULL ANSWER", f("Bold", 24), 4.6
    tw = sum(sd.textlength(c, font=cfont) + csp for c in cue)
    cx = (W - (tw + 36)) // 2
    band = CY1 + 78
    track(sd, (cx, band), cue, cfont, GOLD, sp=csp)
    ax = cx + tw + 14
    sd.polygon([(ax, band + 8), (ax + 22, band + 8), (ax + 11, band + 26)], fill=GOLD)

    OUTDIR.mkdir(parents=True, exist_ok=True)
    out = OUTDIR / f"story-{slug}.png"
    story.save(out)
    url = f"{ORIGIN}/insights/{meta.get('pillar')}/{slug}"
    return out, url, size, len(lines), ok


def main():
    want = set(sys.argv[1:])
    made = 0
    for path in sorted(CONTENT.rglob("*.md")):
        if path.name == "_hub.md":
            continue
        meta = front_matter(path)
        slug = meta.get("slug") or path.stem
        if want and slug not in want:
            continue
        if not meta.get("card"):
            print(f"  no card line, skipped   {slug}")
            continue
        out, url, size, n, ok = build_story(meta, slug)
        warn = "" if ok else "  WARNING: text runs into the sticker band (card line too long for the story)"
        print(f"  written {out}  ({size}px, {n} line(s)){warn}\n    link: {url}")
        made += 1
    print(f"\n{made} story card(s) in {OUTDIR}/ (gitignored, never pushed).")


if __name__ == "__main__":
    main()

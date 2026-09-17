"""Build a LinkedIn newsletter cover for an issue of Reconnect You.

Same family as og_card_articles.py -- navy ground, gold accent, logo block,
a line rather than the title -- with two differences that the surface forces.

WHY IT IS NOT JUST A RESIZED SHARE CARD
---------------------------------------
LinkedIn wants 1920x1080, 16:9. The share cards are 1200x630, which is the
Open Graph ratio, wider than 16:9 and half the resolution. Feeding one into an
article header gets it cropped or letterboxed and it renders soft. Different
surface, different asset.

THE SAFE ZONE
-------------
In the feed LinkedIn crops the cover hard on the top and bottom and shows the
middle band. So the eyebrow and the line sit in the central third; the logo
block and the footer live in the outer bands and are allowed to be cropped
away, because they are recognition rather than message. Tested elsewhere, a
headline inside the safe zone took about a third more clicks than one sitting
near the top edge.

THE PHOTO, AND WHY IT IS A SPLIT RATHER THAN A SCRIM
----------------------------------------------------
A newsletter published from a personal profile is building a person, so the
cover carries his face rather than typography alone.

The first attempt laid type over a full-bleed photo behind a left-to-right
navy scrim. It measured wrong: the photo side came out at mean luminance 10
against 71 on the type side, because the subject sat inside the fading scrim
and the only part left clear was a dark doorway. A full-bleed 4:5 portrait
also needs a 1.6x upscale to cover 1920 wide, which is where the softness and
the lost framing both come from.

So the cover is split. Type on a navy panel left, the photo at its own aspect
right, a gold hairline on the seam. A 1200x1500 portrait lands in the 864x1080
right panel at 0.72x with no crop and no upscale at all.

    python3 og_card_newsletter.py "<line>" <photo> <out.png> [eyebrow]
"""
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance
import pathlib, sys

W, H = 1920, 1080
NAVY  = (4, 18, 42)
CARD  = (10, 29, 60)
GOLD  = (232, 198, 95)
CREAM = (255, 255, 255)
SLATE = (124, 137, 163)

F = "/usr/share/fonts/truetype/google-fonts/Poppins-%s.ttf"
def f(style, size): return ImageFont.truetype(F % style, size)


def track(d, xy, text, font, fill, sp=0.0):
    x, y = xy
    for c in text:
        d.text((x, y), c, font=font, fill=fill)
        x += d.textlength(c, font=font) + sp


def wrap(d, text, font, max_w):
    lines, line = [], ""
    for word in text.split():
        trial = (line + " " + word).strip()
        if d.textlength(trial, font=font) <= max_w or not line:
            line = trial
        else:
            lines.append(line); line = word
    if line: lines.append(line)
    return lines


def fit(d, text, max_w, max_lines=4):
    for size in range(92, 39, -2):
        font = f("Bold", size)
        lines = wrap(d, text, font, max_w)
        if len(lines) <= max_lines:
            return font, lines, size
    font = f("Bold", 40)
    return font, wrap(d, text, font, max_w)[:max_lines], 40


def photo_panel(photo_path, pw, ph):
    """Crop to fill the right panel. Darkened and pushed toward the house navy
    so the photograph and the flat cards read as one palette, but nowhere near
    as far as the scrim version went: the face has to survive."""
    im = Image.open(photo_path).convert("RGB")
    scale = max(pw / im.width, ph / im.height)
    im = im.resize((round(im.width * scale), round(im.height * scale)), Image.LANCZOS)
    left = (im.width - pw) // 2
    top = max(0, round((im.height - ph) * 0.34))
    im = im.crop((left, top, left + pw, top + ph))

    # The grade branches on the source, because the two kinds of photograph he
    # has need opposite handling and getting it backwards ruins both.
    #
    # A DARK source (a night interior, a lit-from-one-side scene) needs a
    # shadow LIFT. The after-hours shot measured his face at median luminance
    # 42 of 255, which on a phone in daylight is a black rectangle with a
    # person somewhere in it. A gamma curve raises the face and the lamp and
    # leaves the blacks black; a brightness increase would grey the whole panel.
    #
    # A LIGHT source (a studio headshot on a pale ground) needs almost none of
    # that. Lifting it blows the background to paper white, and a heavy navy
    # blend turns his skin grey. It gets a small settle downward instead, just
    # enough that the panel sits in the same world as the navy beside it.
    sample = sorted(0.2126 * r + 0.7152 * g + 0.0722 * b
                    for r, g, b in im.resize((120, 150)).getdata())
    median = sample[len(sample) // 2]

    if median < 100:                                   # dark source
        im = im.point([round(255 * (i / 255) ** 0.62) for i in range(256)] * 3)
        im = ImageEnhance.Color(im).enhance(0.66)
        im = ImageEnhance.Contrast(im).enhance(1.06)
        tint = 0.16
    else:                                              # light source
        im = ImageEnhance.Brightness(im).enhance(0.94)
        im = ImageEnhance.Color(im).enhance(0.86)
        im = ImageEnhance.Contrast(im).enhance(1.04)
        tint = 0.10
    im = Image.blend(im, Image.new("RGB", (pw, ph), NAVY), tint)

    # Short fade on the inner edge so the seam is a transition, not a cut.
    mask = Image.new("L", (pw, ph), 0)
    md = ImageDraw.Draw(mask)
    for x in range(round(pw * 0.22)):
        md.line([(x, 0), (x, ph)], fill=int(255 * (1 - x / (pw * 0.22)) ** 1.4))
    mask = mask.filter(ImageFilter.GaussianBlur(18))
    return Image.composite(Image.new("RGB", (pw, ph), NAVY), im, mask)


def build(line, photo, out, eyebrow="RECONNECT YOU"):
    PW = 864                      # right panel: a 4:5 portrait at 1:1, no upscale
    img = Image.new("RGB", (W, H), NAVY)

    glow = Image.new("L", (W, H), 0)
    ImageDraw.Draw(glow).ellipse((-W * 0.1, -H * 0.4, W * 0.62, H * 1.3), fill=150)
    glow = glow.filter(ImageFilter.GaussianBlur(190))
    img = Image.composite(Image.new("RGB", (W, H), CARD), img, glow)

    img.paste(photo_panel(photo, PW, H), (W - PW, 0))
    d = ImageDraw.Draw(img, "RGBA")
    for x in range(-H, W - PW + H, 240):
        d.line([(x, 0), (x + H, H)], fill=(255, 255, 255, 6), width=1)
    d.line([(W - PW, 0), (W - PW, H)], fill=GOLD + (90,), width=2)

    # Outer bands: recognition, and croppable in the feed.
    d.rectangle((70, 60, 345, 139), outline=(255, 255, 255, 70), width=1)
    track(d, (99, 75), "PARALLAXX", f("Bold", 27), CREAM, sp=2.6)
    track(d, (99, 112), "TRANSFORMATIONS", f("Bold", 13), GOLD, sp=3.0)
    track(d, (90, 966), "PARALLAXXTRANSFORMATIONS.COM", f("Bold", 19), SLATE, sp=4.0)
    d.line([(70, 960), (74, 1000)], fill=GOLD + (150,), width=3)

    # Safe zone: everything carrying meaning sits in the middle band.
    track(d, (90, 318), eyebrow, f("Bold", 19), GOLD, sp=4.0)
    font, lines, size = fit(d, line, max_w=W - PW - 180)
    y = 372
    for ln in lines:
        d.text((88, y), ln, font=font, fill=CREAM)
        y += round(size * 1.16)
    d.line([(90, min(y + 34, 860)), (560, min(y + 34, 860))],
           fill=(255, 255, 255, 46), width=2)

    img.save(out)
    return out, size, len(lines)


if __name__ == "__main__":
    line, photo, out = sys.argv[1], sys.argv[2], sys.argv[3]
    eyebrow = sys.argv[4] if len(sys.argv) > 4 else "RECONNECT YOU"
    o, size, n = build(line, photo, out, eyebrow)
    print(f"written {o}  {size}px, {n} line(s)")

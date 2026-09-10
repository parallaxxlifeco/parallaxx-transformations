"""Rebuild the Reconnected Man share card on the v10 copy.

The card still carried "A GIVE IT ALL EXPERIENCE" over "For men done living
in disconnection and loneliness" — a badge for a brand being wound down, over
a promise the page replaced. Same layout and type as the other door, so the
two cards read as a pair, with this page's own words.
"""
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import math

W, H = 1200, 630
NAVY   = (4, 18, 42)
CARD   = (10, 29, 60)
GOLD   = (232, 198, 95)
CREAM  = (255, 255, 255)
MIST   = (177, 191, 215)
SLATE  = (124, 137, 163)

F = "/usr/share/fonts/truetype/google-fonts/Poppins-%s.ttf"
def f(style, size): return ImageFont.truetype(F % style, size)

# ── ground: navy with a soft lift behind the type ────────────────────────
img = Image.new("RGB", (W, H), NAVY)
glow = Image.new("L", (W, H), 0)
gd = ImageDraw.Draw(glow)
gd.ellipse((W*0.14, -H*0.30, W*0.86, H*1.16), fill=150)
glow = glow.filter(ImageFilter.GaussianBlur(120))
img = Image.composite(Image.new("RGB", (W, H), CARD), img, glow)

d = ImageDraw.Draw(img, "RGBA")

# faint diagonal streaks, as on the original
for x in range(-H, W + H, 150):
    d.line([(x, 0), (x + H, H)], fill=(255, 255, 255, 7), width=1)

# corner marks
d.line([(1105, 30), (1155, 30)], fill=(GOLD + (110,)), width=1)
d.line([(1155, 30), (1155, 95)], fill=(GOLD + (110,)), width=1)
d.line([(44, 528), (44, 548)], fill=(GOLD + (150,)), width=2)

def track(draw, xy, text, font, fill, sp=0.0, anchor_centre=False):
    """Letter-spaced text. PIL has no tracking, so step glyph by glyph."""
    widths = [draw.textlength(c, font=font) for c in text]
    total = sum(widths) + sp * (len(text) - 1)
    x, y = xy
    if anchor_centre:
        x -= total / 2
    for c, w in zip(text, widths):
        draw.text((x, y), c, font=font, fill=fill)
        x += w + sp
    return total

# ── logo block ───────────────────────────────────────────────────────────
d.rectangle((44, 38, 216, 87), outline=(255, 255, 255, 70), width=1)
track(d, (62, 47), "PARALLAXX", f("Bold", 17), CREAM, sp=1.6)
track(d, (62, 70), "TRANSFORMATIONS", f("Bold", 8), GOLD, sp=1.9)

# The old card carried "A GIVE IT ALL EXPERIENCE" here. The page itself never
# mentions Give It All, so the card was claiming a badge the page does not,
# and it is gone. Everything below shifts up to keep the stack optically
# centred on the 630 without it.

# ── title ────────────────────────────────────────────────────────────────
big = f("Bold", 82)
l1a, l1b = "The ", "Reconnected"
w1 = d.textlength(l1a, font=big) + d.textlength(l1b, font=big)
x = (W - w1) / 2
d.text((x, 168), l1a, font=big, fill=CREAM)
d.text((x + d.textlength(l1a, font=big), 168), l1b, font=big, fill=GOLD)
l2 = "Man"
d.text(((W - d.textlength(l2, font=big)) / 2, 256), l2, font=big, fill=CREAM)

# ── the promise, as the page now states it ───────────────────────────────
sub = f("Light", 25)
sub_t = "Decide what you want. Ask for it. And see what happens."
d.text(((W - d.textlength(sub_t, font=sub)) / 2, 378), sub_t, font=sub, fill=MIST)

# ── rule ─────────────────────────────────────────────────────────────────
d.line([(300, 436), (900, 436)], fill=(255, 255, 255, 40), width=1)

# ── strip ────────────────────────────────────────────────────────────────
track(d, (W/2, 462), "FREE OPEN SESSION  ·  ONLINE  ·  WEEKLY",
      f("Bold", 13), SLATE, sp=3.2, anchor_centre=True)

img.save("og-reconnected-man.png")
print("written", img.size)

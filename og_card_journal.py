"""Build the Progress Journal share card.

The Wix page never had one -- it shared with whatever Wix picked, which was
usually the logo. Same ground, type and logo block as the other cards so the
set reads as one family, but this is a product page, so the product is on it
rather than a promise line. Run from the repo root; writes the PNG straight
into migration/wix-assets/img/, which is where build-site.py --local reads
og images from.
"""
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import pathlib

W, H = 1200, 630
NAVY  = (4, 18, 42)
CARD  = (10, 29, 60)
GOLD  = (232, 198, 95)
CREAM = (255, 255, 255)
MIST  = (177, 191, 215)
SLATE = (124, 137, 163)

F = "/usr/share/fonts/truetype/google-fonts/Poppins-%s.ttf"
def f(style, size): return ImageFont.truetype(F % style, size)

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


def track(draw, xy, text, font, fill, sp=0.0, anchor_centre=False):
    widths = [draw.textlength(c, font=font) for c in text]
    total = sum(widths) + sp * (len(text) - 1)
    x, y = xy
    if anchor_centre:
        x -= total / 2
    for c, w in zip(text, widths):
        draw.text((x, y), c, font=font, fill=fill)
        x += w + sp
    return total


d.rectangle((44, 38, 216, 87), outline=(255, 255, 255, 70), width=1)
track(d, (62, 47), "PARALLAXX", f("Bold", 17), CREAM, sp=1.6)
track(d, (62, 70), "TRANSFORMATIONS", f("Bold", 8), GOLD, sp=1.9)

# ── the product, cropped to its own edges so the transparent padding in the
#    render does not decide the composition ────────────────────────────────
SRC = pathlib.Path("migration/wix-assets/img/journal-cover-and-spread.png")
shot = Image.open(SRC).convert("RGBA")
shot = shot.crop(shot.getchannel("A").getbbox())
target_h = 430
shot = shot.resize((round(shot.width * target_h / shot.height), target_h),
                   Image.LANCZOS)

# a soft drop shadow, matching the filter the page itself puts on this image
sh = Image.new("RGBA", (shot.width + 120, shot.height + 120), (0, 0, 0, 0))
sh.paste((0, 0, 0, 150), (60, 76), shot.getchannel("A"))
sh = sh.filter(ImageFilter.GaussianBlur(28))
sx, sy = 1200 - shot.width - 72, (H - shot.height) // 2 + 8
img.paste(sh, (sx - 60, sy - 60), sh)
img.paste(shot, (sx, sy), shot)

# ── type, left column, clear of the render ───────────────────────────────
d = ImageDraw.Draw(img, "RGBA")
# The claim leads the page, so it leads the card. It is the loudest surface
# either of them has.
track(d, (56, 214), "THE WORLD\u2019S MOST VALUABLE JOURNAL", f("Bold", 12), GOLD, sp=2.4)

big = f("Bold", 62)
d.text((54, 240), "Progress", font=big, fill=CREAM)
d.text((54, 306), "Journal", font=big, fill=GOLD)

sub = f("Light", 27)
d.text((56, 400), "One page a day. Ninety days.", font=sub, fill=MIST)

d.line([(56, 460), (520, 460)], fill=(255, 255, 255, 40), width=1)
track(d, (56, 482), "HARDCOVER  ·  SHIPPED WORLDWIDE  ·  €24.99",
      f("Bold", 13), SLATE, sp=3.0)

OUT = pathlib.Path("migration/wix-assets/img/og-progress-journal.png")
img.save(OUT)
print("written", OUT, img.size)

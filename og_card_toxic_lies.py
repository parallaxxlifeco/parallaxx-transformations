"""Build the Three Toxic Lies share card.

The Wix page never had one either -- it shared with whatever Wix picked. Same ground, type and logo block as the other cards so the
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
SRC = pathlib.Path("migration/wix-assets/img/toxic-lies-cover.png")
shot = Image.open(SRC).convert("RGBA")
shot = shot.crop(shot.getchannel("A").getbbox())
target_h = 450
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
track(d, (56, 196), "A SHORT BOOK ABOUT TIME", f("Bold", 12), GOLD, sp=2.4)

big = f("Bold", 62)
d.text((54, 222), "Three Toxic", font=big, fill=CREAM)
d.text((54, 288), "Lies", font=big, fill=GOLD)

sub = f("Light", 27)
d.text((56, 386), "You probably believe at least one.", font=f("Light", 25), fill=MIST)

d.line([(56, 448), (560, 448)], fill=(255, 255, 255, 40), width=1)
track(d, (56, 470), "PAPERBACK  ·  POSTED WORLDWIDE  ·  €14.97",
      f("Bold", 13), SLATE, sp=3.0)

# --- card guard -------------------------------------------------------
# This script was derived from the journal's by find-and-replace and one
# replacement missed silently: the card rendered "HARDCOVER . SHIPPED
# WORLDWIDE . EUR 24.99" under a paperback costing EUR 14.97. A share card is
# a picture, so nothing downstream can read it and notice. Everything above
# this marker is the drawing code, and it is what gets checked.
_src = pathlib.Path(__file__).read_text().split("# --- card guard")[0]
for _wrong in ("HARDCOVER", "24.99", "Ninety days", "most valuable journal"):
    if _wrong.lower() in _src.lower():
        raise SystemExit(
            "FAIL: %r is still in the drawing code. Check every string that "
            "came across from the journal's card." % _wrong)
for _want in ("Three Toxic", "14.97", "PAPERBACK"):
    if _want.lower() not in _src.lower():
        raise SystemExit("FAIL: %r is missing from the card" % _want)

OUT = pathlib.Path("migration/wix-assets/img/og-toxic-lies.png")
img.save(OUT)
print("written", OUT, img.size)

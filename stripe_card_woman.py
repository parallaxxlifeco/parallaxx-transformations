"""Stripe checkout product image for The Reconnected Woman.

Stripe renders the product image in a squarish slot in the order summary,
so the 1200x630 share card cannot be reused -- a centre crop of it cuts
straight through the title. This is the same ground, lockup and type as
og-reconnected-woman.png so the two read as one brand, laid out 1:1.

The share card's strip says FREE OPEN SESSION. That is true of the page and
false at a checkout, where the person is paying EUR 89, so the strip here
states what the charge is instead.
"""
from PIL import Image, ImageDraw, ImageFont, ImageFilter

S = 1024
NAVY  = (4, 18, 42)
CARD  = (10, 29, 60)
GOLD  = (232, 198, 95)
CREAM = (255, 255, 255)
MIST  = (177, 191, 215)
SLATE = (124, 137, 163)

F = "/usr/share/fonts/truetype/google-fonts/Poppins-%s.ttf"
def f(style, size): return ImageFont.truetype(F % style, size)

img = Image.new("RGB", (S, S), NAVY)
glow = Image.new("L", (S, S), 0)
gd = ImageDraw.Draw(glow)
gd.ellipse((S*0.10, -S*0.18, S*0.90, S*0.98), fill=150)
glow = glow.filter(ImageFilter.GaussianBlur(150))
img = Image.composite(Image.new("RGB", (S, S), CARD), img, glow)

d = ImageDraw.Draw(img, "RGBA")
for x in range(-S, S * 2, 150):
    d.line([(x, 0), (x + S, S)], fill=(255, 255, 255, 7), width=1)

# corner marks, scaled off the share card
d.line([(S-108, 34), (S-34, 34)], fill=GOLD + (110,), width=1)
d.line([(S-34, 34), (S-34, 108)], fill=GOLD + (110,), width=1)
d.line([(46, S-92), (46, S-58)], fill=GOLD + (150,), width=2)

def track(draw, xy, text, font, fill, sp=0.0, centre=False):
    widths = [draw.textlength(c, font=font) for c in text]
    total = sum(widths) + sp * (len(text) - 1)
    x, y = xy
    if centre: x -= total / 2
    for c, w in zip(text, widths):
        draw.text((x, y), c, font=font, fill=fill); x += w + sp
    return total

# lockup
d.rectangle((46, 42, 218, 91), outline=(255, 255, 255, 70), width=1)
track(d, (64, 51), "PARALLAXX", f("Bold", 17), CREAM, sp=1.6)
track(d, (64, 74), "TRANSFORMATIONS", f("Bold", 8), GOLD, sp=1.9)

# title, sized to the square's measure rather than the card's
big = f("Bold", 94)
a, b = "The ", "Reconnected"
w = d.textlength(a, font=big) + d.textlength(b, font=big)
x = (S - w) / 2
d.text((x, 352), a, font=big, fill=CREAM)
d.text((x + d.textlength(a, font=big), 352), b, font=big, fill=GOLD)
l2 = "Woman"
d.text(((S - d.textlength(l2, font=big)) / 2, 452), l2, font=big, fill=CREAM)

# promise, wrapped for the narrower measure
sub = f("Light", 27)
for i, line in enumerate(["Work out what you want,", "and ask for it in four weeks."]):
    d.text(((S - d.textlength(line, font=sub)) / 2, 600 + i * 43), line, font=sub, fill=MIST)

d.line([(276, 734), (S-276, 734)], fill=(255, 255, 255, 40), width=1)
track(d, (S/2, 762), "ONLINE  ·  WEEKLY  ·  MONTHLY MEMBERSHIP",
      f("Bold", 13), SLATE, sp=3.0, centre=True)

img.save("_working/images/stripe-reconnected-woman.png", optimize=True)
print("written", img.size)

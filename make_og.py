"""Generate the 1200x630 OpenGraph share image for Burnside Music Fest."""
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import math
import random

W, H = 1200, 630
out_png = "og-burnside-fest-2026.png"
out_jpg = "og-burnside-fest-2026.jpg"

# Palette (from flyer)
CREAM   = (232, 210, 166)
PAPER   = (243, 228, 195)
INK     = (30, 26, 20)
INK_2   = (46, 38, 28)
TEAL    = (44, 166, 164)
TEAL_DK = (31, 140, 135)
TEAL_DP = (15, 107, 102)
RUST    = (212, 81, 46)
ORANGE  = (232, 123, 62)
YELLOW  = (247, 212, 76)

FONTS = "C:/Windows/Fonts"
f_title   = ImageFont.truetype(f"{FONTS}/impact.ttf", 168)
f_title_s = ImageFont.truetype(f"{FONTS}/impact.ttf", 110)
f_sub     = ImageFont.truetype(f"{FONTS}/arialbd.ttf", 28)
f_badge   = ImageFont.truetype(f"{FONTS}/arialbd.ttf", 22)
f_date    = ImageFont.truetype(f"{FONTS}/impact.ttf", 60)
f_lineup  = ImageFont.truetype(f"{FONTS}/arialbd.ttf", 22)
f_small   = ImageFont.truetype(f"{FONTS}/arialbd.ttf", 18)

img = Image.new("RGB", (W, H), CREAM)
d = ImageDraw.Draw(img, "RGBA")

# ---------- Paper grain ----------
random.seed(3)
grain = Image.new("RGBA", (W, H), (0, 0, 0, 0))
gd = ImageDraw.Draw(grain)
for _ in range(9000):
    x = random.randint(0, W - 1)
    y = random.randint(0, H - 1)
    a = random.randint(4, 18)
    gd.point((x, y), fill=(40, 30, 20, a))
img = Image.alpha_composite(img.convert("RGBA"), grain).convert("RGB")
d = ImageDraw.Draw(img, "RGBA")

# ---------- Teal flame background ----------
def flame_poly(baseline_y, amp_a, amp_b, step, phase, color):
    pts = [(0, H)]
    x = 0
    i = 0
    while x <= W:
        y = baseline_y - (
            amp_a * math.sin((x / 90.0) + phase)
            + amp_b * math.sin((x / 37.0) + phase * 1.7)
            + 0.35 * amp_a * math.sin((x / 17.0) + phase * 2.3)
        )
        pts.append((x, y))
        x += step
        i += 1
    pts.append((W, H))
    d.polygon(pts, fill=color)

# Back flame (darker)
flame_poly(baseline_y=210, amp_a=70, amp_b=28, step=6, phase=0.4, color=TEAL_DP + (255,))
# Mid flame
flame_poly(baseline_y=280, amp_a=90, amp_b=40, step=6, phase=1.2, color=TEAL_DK + (255,))
# Front flame (brightest)
flame_poly(baseline_y=360, amp_a=110, amp_b=50, step=6, phase=2.2, color=TEAL + (255,))

# ---------- Stars over flames ----------
def star(cx, cy, r, color):
    pts = []
    for k in range(10):
        ang = -math.pi / 2 + k * math.pi / 5
        rr = r if k % 2 == 0 else r * 0.42
        pts.append((cx + rr * math.cos(ang), cy + rr * math.sin(ang)))
    d.polygon(pts, fill=color)

random.seed(11)
for _ in range(22):
    sx = random.randint(20, W - 20)
    sy = random.randint(40, 420)
    sr = random.choice([6, 7, 9, 11, 14])
    star(sx, sy, sr, CREAM + (230,))

# Cream dots sprinkled
for _ in range(60):
    cx = random.randint(0, W)
    cy = random.randint(60, 430)
    rr = random.choice([2, 3, 4])
    d.ellipse((cx - rr, cy - rr, cx + rr, cy + rr), fill=CREAM + (180,))

# ---------- Title "BURNSIDE MUSIC FEST" ----------
def text_w(t, f):
    b = d.textbbox((0, 0), t, font=f)
    return b[2] - b[0], b[3] - b[1]

# BURNSIDE — big
t1 = "BURNSIDE"
t1w, t1h = text_w(t1, f_title)
x1 = (W - t1w) / 2
y1 = 60
# chunky shadow
for dx, dy in [(6, 8)]:
    d.text((x1 + dx, y1 + dy), t1, font=f_title, fill=(0, 0, 0, 90))
# fill
d.text((x1, y1), t1, font=f_title, fill=INK)
# teal dot pattern overlay on the title (evokes the flyer's dotted letters)
dot_layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
dl = ImageDraw.Draw(dot_layer)
# Draw masked dots only inside the text bounding box, pattern
tmask = Image.new("L", (W, H), 0)
tm = ImageDraw.Draw(tmask)
tm.text((x1, y1), t1, font=f_title, fill=255)
# generate dot pattern where mask > 0
for yy in range(y1, y1 + t1h + 20, 18):
    for xx in range(int(x1), int(x1 + t1w) + 20, 18):
        if 0 <= xx < W and 0 <= yy < H and tmask.getpixel((xx, yy)) > 120:
            dl.ellipse((xx - 3, yy - 3, xx + 3, yy + 3), fill=TEAL + (255,))
img = Image.alpha_composite(img.convert("RGBA"), dot_layer).convert("RGB")
d = ImageDraw.Draw(img, "RGBA")

# MUSIC FEST — secondary
t2 = "MUSIC FEST"
t2w, t2h = text_w(t2, f_title_s)
x2 = (W - t2w) / 2
y2 = y1 + t1h - 20
d.text((x2 + 4, y2 + 6), t2, font=f_title_s, fill=(0, 0, 0, 110))
d.text((x2, y2), t2, font=f_title_s, fill=RUST)

# ---------- Badge: R.L. 100th ----------
badge_txt = "★  CELEBRATING R.L. BURNSIDE'S 100TH BIRTHDAY  ★"
bw, bh = text_w(badge_txt, f_badge)
bx = (W - bw) / 2 - 24
by = 30
d.rounded_rectangle((bx, by, bx + bw + 48, by + bh + 20), radius=999, fill=INK)
d.text((bx + 24, by + 10), badge_txt, font=f_badge, fill=YELLOW)

# ---------- Date tag (left) & Location tag (right) ----------
# Date box
date1 = "SATURDAY"
date2 = "JUNE 6"
date3 = "2026"
dx = 60
dy = 415
d.rectangle((dx, dy, dx + 250, dy + 150), fill=RUST)
# little notches
d.polygon([(dx, dy), (dx + 16, dy), (dx, dy + 16)], fill=CREAM)
d.polygon([(dx + 250, dy + 150), (dx + 234, dy + 150), (dx + 250, dy + 134)], fill=CREAM)
d.text((dx + 20, dy + 10), date1, font=ImageFont.truetype(f"{FONTS}/arialbd.ttf", 22), fill=YELLOW)
d.text((dx + 20, dy + 38), date2, font=f_date, fill=CREAM)
d.text((dx + 20, dy + 100), date3, font=ImageFont.truetype(f"{FONTS}/impact.ttf", 42), fill=CREAM)

# Location (right)
lx = W - 60 - 360
ly = 415
d.rectangle((lx, ly, lx + 360, ly + 150), fill=INK)
d.text((lx + 22, ly + 16), "HISTORIC DOWNTOWN", font=ImageFont.truetype(f"{FONTS}/arialbd.ttf", 18), fill=YELLOW)
d.text((lx + 22, ly + 40), "RIPLEY, MS", font=ImageFont.truetype(f"{FONTS}/impact.ttf", 54), fill=CREAM)
d.text((lx + 22, ly + 100), "HILL COUNTRY BLUES ALLEY", font=ImageFont.truetype(f"{FONTS}/arialbd.ttf", 18), fill=TEAL)
d.text((lx + 22, ly + 124), "FREE ENTRY  ·  ALL AGES  ·  MUSIC FROM NOON", font=ImageFont.truetype(f"{FONTS}/arialbd.ttf", 14), fill=CREAM)

# ---------- Lineup ribbon (bottom) ----------
rh = 50
d.rectangle((0, H - rh, W, H), fill=INK)
d.rectangle((0, H - rh - 4, W, H - rh), fill=TEAL)
lineup = "CEDRIC BURNSIDE  ·  GARRY BURNSIDE  ·  PISTOL & THE QUEEN  ·  LENA BEACH feat. BOO MITCHELL  ·  MULE MAN MASSEY  ·  PIP PROJECT  ·  TITUS GILLARD"
# auto-fit font size so it never overflows
fs = 22
while fs > 10:
    f_lu = ImageFont.truetype(f"{FONTS}/arialbd.ttf", fs)
    lw, lh = text_w(lineup, f_lu)
    if lw <= W - 40:
        break
    fs -= 1
d.text(((W - lw) / 2, H - rh + (rh - lh) / 2 - 2), lineup, font=f_lu, fill=CREAM)

# ---------- Burnside domain corner ----------
d.text((W - 280, 22), "BURNSIDEMUSICFEST.COM", font=f_small, fill=INK)

# ---------- Subtle vignette ----------
vignette = Image.new("RGBA", (W, H), (0, 0, 0, 0))
vd = ImageDraw.Draw(vignette)
for i in range(40):
    vd.rectangle((i, i, W - i, H - i), outline=(30, 20, 10, 4))
img = Image.alpha_composite(img.convert("RGBA"), vignette).convert("RGB")

# ---------- Save ----------
img.save(out_png, "PNG", optimize=True)
img.save(out_jpg, "JPEG", quality=92, optimize=True, progressive=True)
print("Wrote", out_png, "and", out_jpg)

"""
TCN Outage Manager Background — Light professional design
Clean white/light gray base with subtle TCN red & blue grid accents.
Optimized for dashboard readability.
"""
import math
import random
from PIL import Image, ImageDraw, ImageFont, ImageChops

W, H = 1920, 1080
FONTS_DIR = r"C:\Users\HP\AppData\Roaming\Claude\local-agent-mode-sessions\skills-plugin\f9601166-a6db-4a1f-b060-dfe7db817764\46011d1b-c4e1-4d6b-a4bd-c4e1cbc576e2\skills\canvas-design\canvas-fonts"

# Light palette
BG_WHITE = (245, 247, 251)
BG_GRAY = (235, 239, 245)
GRID_LIGHT = (215, 222, 235)
GRID_MID = (195, 205, 222)
TCN_BLUE = (0, 51, 128)
TCN_BLUE_LIGHT = (30, 80, 160)
TCN_BLUE_FAINT = (180, 195, 220)
TCN_RED = (200, 30, 40)
TCN_RED_LIGHT = (220, 60, 70)
TCN_RED_FAINT = (235, 195, 198)
ACCENT_NAVY = (15, 30, 65)

random.seed(42)
img = Image.new("RGB", (W, H), BG_WHITE)
draw = ImageDraw.Draw(img)

# --- Subtle gradient: white top → light blue-gray bottom ---
for y in range(H):
    t = y / H
    r = int(BG_WHITE[0] + (BG_GRAY[0] - BG_WHITE[0]) * t)
    g = int(BG_WHITE[1] + (BG_GRAY[1] - BG_WHITE[1]) * t)
    b = int(BG_WHITE[2] + (BG_GRAY[2] - BG_WHITE[2]) * t)
    draw.line([(0, y), (W, y)], fill=(r, g, b))

# --- Fine dot grid (engineering paper feel) ---
dot_sp = 24
for dx in range(0, W, dot_sp):
    for dy in range(0, H, dot_sp):
        draw.ellipse([dx, dy, dx + 1, dy + 1], fill=GRID_LIGHT)

# --- Subtle transmission grid lines ---
grid_sp = 96
for i in range(H // grid_sp + 2):
    y = i * grid_sp
    draw.line([(0, y), (W, y)], fill=GRID_LIGHT, width=1)
for i in range(W // grid_sp + 2):
    x = i * grid_sp
    draw.line([(x, 0), (x, H)], fill=GRID_LIGHT, width=1)

# --- Top banner stripe: navy blue ---
banner_h = 6
draw.rectangle([0, 0, W, banner_h], fill=TCN_BLUE)

# --- Bottom accent stripe: red thin line ---
draw.rectangle([0, H - 4, W, H], fill=TCN_RED)

# --- Left edge accent: blue gradient strip ---
strip_w = 4
for y in range(H):
    t = y / H
    r = int(TCN_BLUE[0] + (TCN_RED[0] - TCN_BLUE[0]) * t)
    g = int(TCN_BLUE[1] + (TCN_RED[1] - TCN_BLUE[1]) * t)
    b = int(TCN_BLUE[2] + (TCN_RED[2] - TCN_BLUE[2]) * t)
    draw.line([(0, y), (strip_w, y)], fill=(r, g, b))

# --- Subtle diagonal transmission lines (very faint) ---
for offset in range(-W, W + H, 200):
    draw.line([(offset, 0), (offset + H, H)], fill=GRID_MID, width=1)

# --- Substation node circles (faint blue) at select grid intersections ---
nodes = []
for i in range(1, W // grid_sp, 2):
    for j in range(1, H // grid_sp, 2):
        if random.random() < 0.3:
            x = i * grid_sp
            y = j * grid_sp
            nodes.append((x, y))

for (nx, ny) in nodes:
    for r in [16, 10, 5]:
        alpha = 0.15 * (1 - r / 20)
        c = tuple(int(BG_GRAY[j] + (TCN_BLUE_FAINT[j] - BG_GRAY[j]) * (alpha + 0.1)) for j in range(3))
        draw.ellipse([nx - r, ny - r, nx + r, ny + r], outline=c, width=1)

# --- Red accent nodes (sparse fault indicators) ---
fault_nodes = random.sample(nodes, min(5, len(nodes)))
for (fx, fy) in fault_nodes:
    for r in [12, 7, 3]:
        alpha = 0.2 * (1 - r / 15)
        c = tuple(int(BG_GRAY[j] + (TCN_RED_FAINT[j] - BG_GRAY[j]) * (alpha + 0.15)) for j in range(3))
        draw.ellipse([fx - r, fy - r, fx + r, fy + r], outline=c, width=1)
    draw.ellipse([fx - 2, fy - 2, fx + 2, fy + 2], fill=TCN_RED_FAINT)

# --- Connection lines between nearby nodes ---
for i, (x1, y1) in enumerate(nodes):
    for jj, (x2, y2) in enumerate(nodes):
        if i >= jj:
            continue
        dist = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
        if 80 < dist < 220 and random.random() < 0.1:
            draw.line([(x1, y1), (x2, y2)], fill=GRID_MID, width=1)

# --- Sine wave at very bottom (above the red stripe) ---
wave_y = H - 40
amp = 8
for x_px in range(W):
    t = x_px / W * 16 * 2 * math.pi
    y_val = wave_y + amp * math.sin(t)
    fade = 0.15 + 0.1 * (1 - abs(x_px - W/2) / (W/2))
    c = tuple(int(BG_GRAY[j] + (TCN_RED_FAINT[j] - BG_GRAY[j]) * fade) for j in range(3))
    draw.point((x_px, int(y_val)), fill=c)
    draw.point((x_px, int(y_val) + 1), fill=c)

# --- Corner brackets (blue) ---
mk, ins = 35, 25
mk_blue = tuple(int(BG_GRAY[j] + (TCN_BLUE_FAINT[j] - BG_GRAY[j]) * 0.5) for j in range(3))
mk_red = tuple(int(BG_GRAY[j] + (TCN_RED_FAINT[j] - BG_GRAY[j]) * 0.5) for j in range(3))
draw.line([(ins, ins + banner_h), (ins + mk, ins + banner_h)], fill=mk_blue, width=1)
draw.line([(ins, ins + banner_h), (ins, ins + mk + banner_h)], fill=mk_blue, width=1)
draw.line([(W - ins, ins + banner_h), (W - ins - mk, ins + banner_h)], fill=mk_red, width=1)
draw.line([(W - ins, ins + banner_h), (W - ins, ins + mk + banner_h)], fill=mk_red, width=1)
draw.line([(ins, H - ins - 4), (ins + mk, H - ins - 4)], fill=mk_red, width=1)
draw.line([(ins, H - ins - 4), (ins, H - ins - mk - 4)], fill=mk_red, width=1)
draw.line([(W - ins, H - ins - 4), (W - ins - mk, H - ins - 4)], fill=mk_blue, width=1)
draw.line([(W - ins, H - ins - 4), (W - ins, H - ins - mk - 4)], fill=mk_blue, width=1)

# --- Hexagonal cluster (faint, decorative) bottom-right ---
def draw_hex(draw, cx_h, cy_h, radius, color):
    pts = [(cx_h + radius * math.cos(math.radians(60 * k - 30)),
             cy_h + radius * math.sin(math.radians(60 * k - 30))) for k in range(6)]
    draw.polygon(pts, outline=color)

hcx, hcy = int(W * 0.92), int(H * 0.75)
for ring in range(1, 4):
    for step in range(6):
        angle = math.radians(60 * step + 30 * (ring % 2))
        hx = hcx + ring * 26 * math.cos(angle)
        hy = hcy + ring * 26 * math.sin(angle)
        c = tuple(int(BG_GRAY[j] + (TCN_BLUE_FAINT[j] - BG_GRAY[j]) * (0.2 - ring * 0.04)) for j in range(3))
        draw_hex(draw, hx, hy, 11, c)

# Small red hex cluster top-left
hcx2, hcy2 = int(W * 0.06), int(H * 0.18)
for ring in range(1, 3):
    for step in range(6):
        angle = math.radians(60 * step)
        hx = hcx2 + ring * 22 * math.cos(angle)
        hy = hcy2 + ring * 22 * math.sin(angle)
        c = tuple(int(BG_GRAY[j] + (TCN_RED_FAINT[j] - BG_GRAY[j]) * (0.2 - ring * 0.05)) for j in range(3))
        draw_hex(draw, hx, hy, 9, c)

# --- Save ---
out = r"C:\Users\HP\OneDrive\Desktop\TCN Outage Attributes\tcn_background.png"
img.save(out, "PNG")
print(f"Saved: {out} ({W}x{H})")

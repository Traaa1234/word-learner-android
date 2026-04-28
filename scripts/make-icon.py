"""Generate app icons (1024x1024) for Capacitor: gradient background + fox emoji."""

from PIL import Image, ImageDraw, ImageFont
import os

SIZE = 1024
GRAD_RES = 128  # build a small gradient and upscale for smoothness
FONT_PATH = "C:/Windows/Fonts/seguiemj.ttf"

# Palette pulled from the app's theme
PURPLE = (167, 139, 250)
PINK   = (244, 114, 182)
ORANGE = (251, 146, 60)
SKY    = (147, 197, 253)

def lerp(c1, c2, u):
    return tuple(int(c1[i] * (1 - u) + c2[i] * u) for i in range(3))

def build_gradient():
    img = Image.new("RGB", (GRAD_RES, GRAD_RES))
    pix = img.load()
    for y in range(GRAD_RES):
        for x in range(GRAD_RES):
            t = (x + y) / (2 * (GRAD_RES - 1))
            if t < 0.33:
                c = lerp(PURPLE, PINK, t / 0.33)
            elif t < 0.66:
                c = lerp(PINK, ORANGE, (t - 0.33) / 0.33)
            else:
                c = lerp(ORANGE, SKY, (t - 0.66) / 0.34)
            pix[x, y] = c
    return img.resize((SIZE, SIZE), Image.BICUBIC)

def render_emoji(font_size, canvas_size=SIZE):
    layer = Image.new("RGBA", (canvas_size, canvas_size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(layer)
    font = ImageFont.truetype(FONT_PATH, font_size)
    text = "🦊"
    bbox = draw.textbbox((0, 0), text, font=font, embedded_color=True)
    tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
    x = (canvas_size - tw) // 2 - bbox[0]
    y = (canvas_size - th) // 2 - bbox[1]
    draw.text((x, y), text, font=font, embedded_color=True)
    return layer

def main():
    out_dir = os.path.join(os.path.dirname(__file__), "..", "assets")
    out_dir = os.path.abspath(out_dir)
    os.makedirs(out_dir, exist_ok=True)

    bg = build_gradient()

    # Adaptive icon foreground: fox at ~58% so it stays inside Android's safe zone.
    fox_fg = render_emoji(font_size=600)
    fox_fg.save(os.path.join(out_dir, "icon-foreground.png"), "PNG")

    # Adaptive icon background: pure gradient.
    bg.save(os.path.join(out_dir, "icon-background.png"), "PNG")

    # Legacy/iOS icon: bigger fox composited on the gradient.
    fox_full = render_emoji(font_size=720)
    combined = bg.copy().convert("RGBA")
    combined = Image.alpha_composite(combined, fox_full)
    combined.convert("RGB").save(os.path.join(out_dir, "icon-only.png"), "PNG")

    print("Wrote:")
    for name in ("icon-only.png", "icon-foreground.png", "icon-background.png"):
        p = os.path.join(out_dir, name)
        print(f"  {p} ({os.path.getsize(p)} bytes)")

if __name__ == "__main__":
    main()

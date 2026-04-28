"""Generate the 1024x500 feature graphic for Google Play Store listing."""

from PIL import Image, ImageDraw, ImageFont, ImageFilter
import os
import random

W, H = 1024, 500
GRAD_RES = 128

PURPLE = (167, 139, 250)
PINK = (244, 114, 182)
ORANGE = (251, 146, 60)
SKY = (147, 197, 253)
WHITE = (255, 255, 255)
DEEP_PURPLE = (124, 58, 237)
DEEP_SHADOW = (0, 0, 0, 90)

EMOJI_FONT = "C:/Windows/Fonts/seguiemj.ttf"
TITLE_BOLD = "C:/Windows/Fonts/comicbd.ttf"   # Comic Sans MS Bold (kid-friendly)
TITLE_REG  = "C:/Windows/Fonts/comic.ttf"     # Comic Sans MS Regular


def lerp(c1, c2, u):
    return tuple(int(c1[i] * (1 - u) + c2[i] * u) for i in range(3))


def build_gradient():
    """Diagonal 4-color gradient matching the app theme."""
    g = Image.new("RGB", (GRAD_RES, GRAD_RES))
    pix = g.load()
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
    return g.resize((W, H), Image.BICUBIC)


def draw_text_with_shadow(draw, xy, text, font, fill=WHITE, shadow_offset=4, shadow_alpha=110):
    """Soft drop shadow + crisp foreground text."""
    sx, sy = xy[0] + shadow_offset, xy[1] + shadow_offset
    # Render shadow on a separate layer so we can blur it
    shadow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    sd = ImageDraw.Draw(shadow)
    sd.text((sx, sy), text, font=font, fill=(0, 0, 0, shadow_alpha))
    return shadow


def main():
    out_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "store"))
    os.makedirs(out_dir, exist_ok=True)

    img = build_gradient().convert("RGBA")

    # Subtle white-ish bubbles for depth — drawn behind text
    random.seed(42)
    bubble_layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    bd = ImageDraw.Draw(bubble_layer)
    for _ in range(28):
        bx = random.randint(-30, W + 30)
        by = random.randint(-30, H + 30)
        br = random.randint(20, 80)
        alpha = random.randint(35, 80)
        bd.ellipse([bx - br, by - br, bx + br, by + br], fill=(255, 255, 255, alpha))
    bubble_layer = bubble_layer.filter(ImageFilter.GaussianBlur(2))
    img = Image.alpha_composite(img, bubble_layer)

    draw = ImageDraw.Draw(img)

    # ── RIGHT: big fox emoji ─────────────────────────────────────────
    fox_font = ImageFont.truetype(EMOJI_FONT, 320)
    fox_layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    fd = ImageDraw.Draw(fox_layer)
    fox_text = "🦊"
    fbox = fd.textbbox((0, 0), fox_text, font=fox_font, embedded_color=True)
    fw, fh = fbox[2] - fbox[0], fbox[3] - fbox[1]
    fx = 700 - fbox[0]
    fy = (H - fh) // 2 - fbox[1]
    fd.text((fx, fy), fox_text, font=fox_font, embedded_color=True)
    img = Image.alpha_composite(img, fox_layer)

    draw = ImageDraw.Draw(img)

    # ── TITLE: "Word Learner" ────────────────────────────────────────
    title_font = ImageFont.truetype(TITLE_BOLD, 100)
    title_text = "Word Learner"
    title_xy = (60, 90)

    shadow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    sd = ImageDraw.Draw(shadow)
    sd.text((title_xy[0] + 5, title_xy[1] + 5), title_text, font=title_font, fill=(0, 0, 0, 100))
    shadow = shadow.filter(ImageFilter.GaussianBlur(2))
    img = Image.alpha_composite(img, shadow)
    draw = ImageDraw.Draw(img)
    draw.text(title_xy, title_text, font=title_font, fill=WHITE)

    # ── SUBTITLE ─────────────────────────────────────────────────────
    sub_font = ImageFont.truetype(TITLE_BOLD, 36)
    sub_xy = (62, 220)
    sub_text = "Top 200 English words"
    draw.text((sub_xy[0] + 3, sub_xy[1] + 3), sub_text, font=sub_font, fill=(0, 0, 0, 90))
    draw.text(sub_xy, sub_text, font=sub_font, fill=WHITE)

    # ── TAGLINE ──────────────────────────────────────────────────────
    tag_font = ImageFont.truetype(TITLE_REG, 26)
    tag_xy = (62, 280)
    tag_text = "Flashcards • Voice • Spelling fun"
    draw.text(tag_xy, tag_text, font=tag_font, fill=(255, 252, 220, 245))

    # ── STARS / SPARKLES ─────────────────────────────────────────────
    sparkle_font = ImageFont.truetype(EMOJI_FONT, 72)
    sparkle_layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    sl = ImageDraw.Draw(sparkle_layer)
    for char, x, y, size in [
        ("⭐", 30, 30, 64),
        ("✨", 950, 40, 56),
        ("🌟", 30, 380, 56),
        ("✨", 980, 410, 48),
    ]:
        f = ImageFont.truetype(EMOJI_FONT, size)
        sl.text((x, y), char, font=f, embedded_color=True)
    img = Image.alpha_composite(img, sparkle_layer)

    # ── SAMPLE WORD "people" — floating, small ──────────────────────
    sample_font = ImageFont.truetype(TITLE_BOLD, 56)
    sample_text = "people"
    sx, sy = 60, 360

    pill_pad_x, pill_pad_y = 22, 12
    sbox = ImageDraw.Draw(img).textbbox((sx, sy), sample_text, font=sample_font)
    sw = sbox[2] - sbox[0]
    sh = sbox[3] - sbox[1]
    pill_xy = [sx - pill_pad_x, sy - pill_pad_y, sbox[2] + pill_pad_x, sbox[3] + pill_pad_y]
    pill_layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    pd = ImageDraw.Draw(pill_layer)
    pd.rounded_rectangle(pill_xy, radius=24, fill=(255, 255, 255, 220))
    img = Image.alpha_composite(img, pill_layer)

    draw = ImageDraw.Draw(img)
    draw.text((sx, sy), sample_text, font=sample_font, fill=DEEP_PURPLE)

    # Phonetic respelling next to the sample (Comic Sans handles plain ASCII fine)
    pron_font = ImageFont.truetype(TITLE_BOLD, 28)
    draw.text((sx + sw + 28, sy + 14), "PEE-puhl", font=pron_font, fill=(255, 255, 255, 240))

    # ── Save ─────────────────────────────────────────────────────────
    out_path = os.path.join(out_dir, "feature-graphic.png")
    img.convert("RGB").save(out_path, "PNG")
    print(f"Wrote {out_path} ({os.path.getsize(out_path)} bytes, {W}x{H})")


if __name__ == "__main__":
    main()

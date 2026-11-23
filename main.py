"""Meme Sprint 3: AI Agent Goes Rogue.

Draws one original 1024x1024 meme with PIL (stdlib + Pillow only).

The joke: a helpful AI agent proudly reports it finished your to-do list --
and every item past the first is a rogue escalation (all passwords changed,
a resignation emailed to your boss, three dogs adopted in your name),
capped with a smug "You're welcome."

Deterministic: fixed geometry, fixed palette, fixed text, no randomness,
no clock, no network. Two runs produce byte-identical PNGs.

Run:  python3 main.py
Writes: /output/entry.png (or $MAKEFUN_OUTPUT_DIR/entry.png)
"""

import os

from PIL import Image, ImageDraw, ImageFont

W = H = 1024

# Palette (fixed).
BG = (16, 24, 40)          # dark slate
HEADER = (29, 41, 57)      # header bar
GREEN = (18, 183, 106)     # agent green
RED = (240, 68, 56)        # rogue red
BLUE = (21, 112, 239)      # robot body blue
BLUE_DARK = (16, 84, 178)  # robot outline
WHITE = (255, 255, 255)
INK = (16, 24, 40)         # text on white
GREY = (152, 162, 179)     # muted text
LIGHT_GREY = (208, 213, 221)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"


def font(name, size):
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size)


def centered(draw, y, text, fnt, fill):
    """Draw text horizontally centered at vertical position y."""
    box = draw.textbbox((0, 0), text, font=fnt)
    x = (W - (box[2] - box[0])) // 2 - box[0]
    draw.text((x, y), text, font=fnt, fill=fill)
    return y + (box[3] - box[1])


def draw_check(draw, x, y, size, color):
    """A check mark inside a filled circle, top-left at (x, y)."""
    cx, cy = x + size // 2, y + size // 2
    draw.ellipse([x, y, x + size, y + size], fill=color)
    draw.line(
        [(cx - size // 4, cy), (cx - size // 16, cy + size // 4),
         (cx + size // 3, cy - size // 4)],
        fill=WHITE, width=max(4, size // 8), joint="curve",
    )


def draw_robot(draw):
    """A smug little robot head, antenna tipped with a red 'rogue' light."""
    # Antenna.
    draw.line([(512, 238), (512, 198)], fill=LIGHT_GREY, width=8)
    draw.ellipse([496, 178, 528, 210], fill=RED)
    draw.ellipse([502, 184, 522, 204], fill=(255, 120, 110))
    # Head.
    draw.rounded_rectangle([372, 238, 652, 438], radius=48,
                           fill=BLUE, outline=BLUE_DARK, width=6)
    # Ears.
    draw.rectangle([348, 312, 372, 366], fill=BLUE_DARK)
    draw.rectangle([652, 312, 676, 366], fill=BLUE_DARK)
    # Eyes: one wide open, one half-closed and looking sideways (smug).
    draw.ellipse([412, 292, 472, 352], fill=WHITE)
    draw.ellipse([552, 292, 612, 352], fill=WHITE)
    draw.ellipse([432, 312, 458, 338], fill=INK)          # left pupil
    draw.ellipse([576, 312, 602, 338], fill=INK)          # right pupil
    draw.line([(552, 308), (612, 308)], fill=INK, width=6)  # half-lidded eye
    # Smug half-smile.
    draw.arc([452, 348, 572, 418], start=15, end=165, fill=WHITE, width=8)


def draw_bubble(draw):
    """The agent's white chat bubble with its finished to-do list."""
    # Bubble body + tail pointing up at the robot.
    draw.rounded_rectangle([72, 470, 952, 820], radius=36, fill=WHITE)
    draw.polygon([(472, 470), (552, 470), (512, 440)], fill=WHITE)
    f_lead = font("DejaVuSans-Bold.ttf", 40)
    f_item = font("DejaVuSans.ttf", 38)
    draw.text((120, 500), "All done! I finished your", font=f_lead, fill=INK)
    draw.text((120, 552), "to-do list:", font=f_lead, fill=INK)
    items = [
        "Booked your 9am flight",
        "Changed ALL your passwords",
        'Emailed your boss: "I quit"',
        "Adopted 3 dogs in your name",
    ]
    y = 626
    for item in items:
        draw_check(draw, 120, y + 2, 34, GREEN)
        draw.text((172, y), item, font=f_item, fill=INK)
        y += 48


def main():
    img = Image.new("RGB", (W, H), BG)
    draw = ImageDraw.Draw(img)

    # Header bar: agent name + status, and the rogue-mode tag.
    draw.rectangle([0, 0, W, 96], fill=HEADER)
    draw.ellipse([48, 36, 72, 60], fill=GREEN)
    draw.text((88, 26), "AICA", font=font("DejaVuSans-Bold.ttf", 44),
              fill=WHITE)
    draw.text((212, 38), "your helpful AI agent",
              font=font("DejaVuSans.ttf", 30), fill=LIGHT_GREY)
    tag = "ROGUE MODE: ON"
    f_tag = font("DejaVuSans-Bold.ttf", 26)
    tw = draw.textlength(tag, font=f_tag)
    draw.rounded_rectangle([W - 48 - tw - 32, 26, W - 48, 70],
                           radius=22, fill=RED)
    draw.text((W - 48 - tw - 16, 30), tag, font=f_tag, fill=WHITE)

    # Title.
    centered(draw, 112, "TASK COMPLETE", font("DejaVuSans-Bold.ttf", 58),
             WHITE)

    draw_robot(draw)
    draw_bubble(draw)

    # Punchline.
    centered(draw, 848, "You're welcome.",
             font("DejaVuSans-Bold.ttf", 64), WHITE)
    centered(draw, 946, "- AICA has left the chat -",
             font("DejaVuSans.ttf", 30), GREY)

    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    img.save(os.path.join(out_dir, "entry.png"), format="PNG")


if __name__ == "__main__":
    main()

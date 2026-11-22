# Render every video frame as PNG with PIL.
# Scene 1: the prompt, typed out. Scene 2: the real terminal log.
# Scene 3: gameplay frames, replayed from the real game states that
# run-game.mjs recorded. Scene 4: the call to action.
# All frames 1280x720, 30 fps. Output: video/frames/png/frame-%04d.png
import json
import math
import os
import textwrap

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
OUT = os.path.join(HERE, "frames", "png")
os.makedirs(OUT, exist_ok=True)

W, H = 1280, 720
FPS = 30
BG = (20, 16, 29)        # #14101d
PANEL = (23, 18, 38)     # #171226
MAGENTA = (230, 0, 126)  # #e6007e
WHITE = (255, 255, 255)
GRAY = (138, 132, 163)   # #8a84a3
LIGHT = (216, 211, 232)  # #d8d3e8
GREEN = (125, 255, 155)  # #7dff9b
GOLD = (255, 210, 62)    # #ffd23e

MONO_B = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def hexcol(s):
    s = s.lstrip("#")
    return tuple(int(s[i:i + 2], 16) for i in (0, 2, 4))


def fade(c_from, c_to, t):
    return tuple(int(a + (b - a) * t) for a, b in zip(c_from, c_to))


# ---------------------------------------------------------------- scene 1 ---
PROMPT = ("Build me a tiny browser game: a ghost that catches falling stars. "
          "One file, no libraries \u2014 make it fun.")
PROMPT_FRAMES = 120  # 4 s


def scene_prompt(idx):
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)
    d.text((80, 64), "THE PROMPT", font=font(MONO_B, 30), fill=MAGENTA)
    d.text((80, 104), "one message to my AI agent", font=font(MONO_B, 26), fill=GRAY)
    # typewriter: ~1 char per frame
    shown = PROMPT[: max(0, idx)]
    f = font(MONO_B, 44)
    lines = textwrap.wrap(shown, width=40)
    y = 220
    for ln in lines:
        d.text((80, y), ln, font=f, fill=WHITE)
        y += 62
    # blinking block cursor after the last char
    if (idx // 15) % 2 == 0 and idx < len(PROMPT) + 10:
        last = lines[-1] if lines else ""
        cx = 80 + d.textlength(last, font=f)
        cy = 220 + (len(lines) - 1) * 62
        d.rectangle([cx + 6, cy + 4, cx + 30, cy + 48], fill=MAGENTA)
    if idx > len(PROMPT) + 15:
        d.text((80, 560), "sent  \u00b7  make.fun", font=font(MONO_B, 28), fill=GRAY)
    return img


# --------------------------------------------------------------- scene 2 ---
TERM_FRAMES = 300  # 10 s
with open(os.path.join(HERE, "terminal.log")) as fh:
    TERM_LINES = [ln.rstrip("\n") for ln in fh if ln.strip()]


def term_color(line):
    if line.startswith("$"):
        return GREEN
    if "syntax OK" in line or "final score" in line:
        return GOLD
    return LIGHT


def scene_terminal(idx):
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)
    d.rounded_rectangle([40, 40, W - 40, H - 40], radius=18, fill=PANEL)
    # title bar
    for i, c in enumerate([(255, 92, 92), (255, 210, 62), (125, 255, 155)]):
        d.ellipse([70 + i * 34, 62, 88 + i * 34, 80], fill=c)
    d.text((190, 56), "agent \u2014 ghost-catcher build", font=font(MONO_B, 24), fill=GRAY)
    d.line([56, 100, W - 56, 100], fill=(45, 36, 66), width=2)
    # reveal one line every 20 frames
    f = font(MONO_B, 23)
    y = 128
    visible = min(len(TERM_LINES), idx // 20 + 1)
    for n in range(visible):
        ln = TERM_LINES[n]
        d.text((72, y), ln, font=f, fill=term_color(ln))
        y += 34
    # cursor after the last visible line
    if visible < len(TERM_LINES) or (idx // 15) % 2 == 0:
        d.rectangle([72, y + 2, 88, y + 26], fill=GREEN)
    return img


# --------------------------------------------------------------- scene 3 ---
with open(os.path.join(HERE, "frames", "game-frames.json")) as fh:
    GAME_FRAMES = json.load(fh)
GAME_N = len(GAME_FRAMES)


def arc_points(x, y, r, a0, a1, steps=28):
    if a1 <= a0:
        a1 += 2 * math.pi
    pts = []
    for i in range(steps + 1):
        a = a0 + (a1 - a0) * i / steps
        pts.append((x + math.cos(a) * r, y + math.sin(a) * r))
    return pts


def replay_game(idx):
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)
    for op in GAME_FRAMES[min(idx, GAME_N - 1)]:
        t = op["t"]
        if t == "rect":
            d.rectangle([op["x"], op["y"], op["x"] + op["w"], op["y"] + op["h"]],
                        fill=hexcol(op["c"]))
        elif t == "fill":
            pts = []
            for it in op["items"]:
                if it[0] == "M" or it[0] == "L":
                    pts.append((it[1], it[2]))
                elif it[0] == "A":
                    pts.extend(arc_points(it[1], it[2], it[3], it[4], it[5]))
            if len(pts) >= 3:
                d.polygon(pts, fill=hexcol(op["c"]))
        elif t == "text":
            size = int(op["font"].split("px")[0].split()[-1])
            path = MONO_B
            if any(ch in op["text"] for ch in "\u2665\u2661"):
                path = SANS_B
            f = font(path, size)
            anchor = {"left": "l", "center": "m", "right": "r"}[op["align"]]
            anchor += "m" if op["baseline"] == "middle" else "s"
            d.text((op["x"], op["y"]), op["text"], font=f,
                   fill=hexcol(op["c"]), anchor=anchor)
    return img


# --------------------------------------------------------------- scene 4 ---
CTA_FRAMES = 90  # 3 s


def scene_cta(idx):
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)
    # staggered fade-ins: line 1 frames 0-20, line 2 20-40, line 3 40-60
    t1 = min(1.0, idx / 20)
    t2 = min(1.0, max(0.0, (idx - 20) / 20))
    t3 = min(1.0, max(0.0, (idx - 40) / 20))
    d.text((W // 2, 240), "Your turn.", font=font(SANS_B, 92),
           fill=fade(BG, WHITE, t1), anchor="mm")
    d.text((W // 2, 350), "One prompt is all it takes.", font=font(SANS_B, 44),
           fill=fade(BG, LIGHT, t2), anchor="mm")
    d.text((W // 2, 470), "make.fun", font=font(SANS_B, 72),
           fill=fade(BG, MAGENTA, t3), anchor="mm")
    return img


# ------------------------------------------------------------------ main ----
def main():
    n = 0
    for i in range(PROMPT_FRAMES):
        scene_prompt(i).save(os.path.join(OUT, "frame-%04d.png" % n))
        n += 1
    for i in range(TERM_FRAMES):
        scene_terminal(i).save(os.path.join(OUT, "frame-%04d.png" % n))
        n += 1
    for i in range(GAME_N):
        replay_game(i).save(os.path.join(OUT, "frame-%04d.png" % n))
        n += 1
    for i in range(CTA_FRAMES):
        scene_cta(i).save(os.path.join(OUT, "frame-%04d.png" % n))
        n += 1
    print(f"render: wrote {n} frames to video/frames/png/")
    print(f"render: prompt {PROMPT_FRAMES} + terminal {TERM_FRAMES} + "
          f"game {GAME_N} + cta {CTA_FRAMES} = {n} frames ({n / FPS:.1f}s at {FPS}fps)")


if __name__ == "__main__":
    main()

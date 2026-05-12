import math
import re
from pathlib import Path
from collections import defaultdict
from PIL import Image, ImageSequence


# ----------------------------
# Setup
# ----------------------------
input_folder = ".\\inputs\\"
output_folder = "characters/" + input("Output folder: ").strip() or "output"

INPUT_DIR = Path(input_folder)
OUTPUT_DIR = Path(output_folder)
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


# ----------------------------
# Naming: (a)idle -> idle_a
# ----------------------------
def split_name(stem: str):
    m = re.match(r"^\((a|b)\)(.*)$", stem, re.IGNORECASE)

    if m:
        tag = m.group(1).lower()
        base = m.group(2)
    else:
        tag = "pre"
        base = stem

    return clean(base), tag


def clean(name: str):
    name = re.sub(r"[^\w]+", "_", name)
    return re.sub(r"_+", "_", name).strip("_") or "anim"


# ----------------------------
# WebP extraction (preserve timing)
# ----------------------------
def extract_frames(path: Path):
    img = Image.open(path)

    frames = []
    durations = []

    for frame in ImageSequence.Iterator(img):
        frames.append(frame.copy().convert("RGBA"))
        durations.append(frame.info.get("duration", img.info.get("duration", 100)) / 1000.0)

    return frames, durations


# ----------------------------
# Sprite sheet layout
# ----------------------------
def auto_grid(n):
    cols = math.ceil(math.sqrt(n))
    rows = math.ceil(n / cols)
    return cols, rows


def build_sheet(frames):
    cols, rows = auto_grid(len(frames))
    w, h = frames[0].size

    sheet = Image.new("RGBA", (cols * w, rows * h))

    for i, f in enumerate(frames):
        sheet.paste(f, ((i % cols) * w, (i // cols) * h))

    return sheet, cols, rows


# ----------------------------
# Animation .tres (Sprite2D only)
# ----------------------------
def write_animation(name, texture_path, cols, rows, durations):
    times = []
    values = []

    t = 0.0
    for i, d in enumerate(durations):
        times.append(round(t, 6))
        values.append(i)
        t += d

    content = f'''[gd_resource type="Animation" format=3]

[ext_resource type="Texture2D" path="res://{texture_path.as_posix()}" id="1"]

[resource]
resource_name = "{name}"
length = {round(sum(durations), 6)}
loop_mode = 1

tracks/0/type = "value"
tracks/0/path = NodePath("Sprite2D:texture")
tracks/0/keys = {{"times":[0.0],"values":[ExtResource("1")]}}

tracks/1/type = "value"
tracks/1/path = NodePath("Sprite2D:hframes")
tracks/1/keys = {{"times":[0.0],"values":[{cols}]}}

tracks/2/type = "value"
tracks/2/path = NodePath("Sprite2D:vframes")
tracks/2/keys = {{"times":[0.0],"values":[{rows}]}}

tracks/3/type = "value"
tracks/3/path = NodePath("Sprite2D:frame")
tracks/3/keys = {{
"times": {times},
"values": {values},
"update": 1
}}
'''

    out = OUTPUT_DIR / f"{name}.tres"
    out.write_text(content, encoding="utf-8")


# ----------------------------
# Main
# ----------------------------
groups = defaultdict(list)

for f in INPUT_DIR.iterdir():
    if f.suffix.lower() != ".webp":
        continue

    base, tag = split_name(f.stem)
    groups[clean(base)].append((tag, f))


for base, items in groups.items():
    print(f"\nProcessing: {base}")

    for tag, file in items:
        name = f"{base}_{tag}"

        frames, durations = extract_frames(file)
        if not frames:
            continue

        sheet, cols, rows = build_sheet(frames)

        png_path = OUTPUT_DIR / f"{name}.png"
        sheet.save(png_path)

        write_animation(name, png_path, cols, rows, durations)

        print(f"  {name}: {len(frames)} frames ({cols}x{rows})")
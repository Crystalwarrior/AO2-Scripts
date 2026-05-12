import json
import os
import shutil
from pathlib import Path

SPRITE_EXTENSIONS = [".webp", ".apng", ".gif", ".png"]


def parse_char_ini(char_ini_path):
    config = {}
    emotions = {}

    section = None
    with open(char_ini_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            if line.startswith("[") and line.endswith("]"):
                section = line[1:-1]
                continue
            if "=" in line:
                key, _, value = line.partition("=")
                key = key.strip()
                value = value.strip()
                if section == "Emotions":
                    if key.isdigit():
                        emotions[int(key)] = value
                elif section == "Options":
                    config[key.lower()] = value

    sprite_names = []
    for i in sorted(emotions.keys()):
        parts = emotions[i].split("#")
        sprite_name = parts[1].split("#")[0].strip()
        sprite_names.append(sprite_name)

    return config, sprite_names


def find_sprite_file(base_dir, name):
    for ext in SPRITE_EXTENSIONS:
        path = base_dir / f"{name}{ext}"
        if path.exists():
            return path
    return None


def main():
    base_dir = Path.cwd()
    char_ini_path = base_dir / "char.ini"

    if not char_ini_path.exists():
        print("char.ini not found in current directory.")
        return

    print(f"Parsing {char_ini_path}...")
    config, sprite_names = parse_char_ini(char_ini_path)

    showname = config.get("showname", "")
    side = config.get("side", "wit")
    gender = config.get("gender", "plmale")

    print(f"  Showname: {showname}")
    print(f"  Side: {side}")
    print(f"  Gender: {gender}")
    print(f"  Sprites ({len(sprite_names)}): {', '.join(sprite_names)}")

    # Create directory structure
    outfit_dir = base_dir / "outfits" / "Default"
    emotions_dir = outfit_dir / "emotions"
    outfit_dir.mkdir(parents=True, exist_ok=True)
    emotions_dir.mkdir(parents=True, exist_ok=True)
    print("  Created directories: outfits/Default/emotions/")

    # Write char.json
    char_json = {
        "showname": showname,
        "side": side,
        "gender": gender,
        "outfit_order": ["Default"],
    }
    with open(base_dir / "char.json", "w", encoding="utf-8") as f:
        json.dump(char_json, f, indent=4)
    print("  Created char.json")

    # Write outfit.json
    emotes = []
    for name in sprite_names:
        emotes.append({"name": name, "image": name})

    outfit_json = {
        "outfit_name": "Default",
        "default_rules": {
            "show_desk": True,
            "ignore_offsets": False,
        },
        "layers": [],
        "emotes": emotes,
    }
    with open(outfit_dir / "outfit.json", "w", encoding="utf-8") as f:
        json.dump(outfit_json, f, indent=4)
    print("  Created outfits/Default/outfit.json")

    # Move sprite files from root to outfits/Default/
    moved = 0
    for name in sprite_names:
        src = find_sprite_file(base_dir, name)
        if src:
            ext = src.suffix
            shutil.move(str(src), str(outfit_dir / f"{name}{ext}"))
            moved += 1
        else:
            print(f"  Warning: No sprite file found for '{name}'")
    print(f"  Moved {moved} sprite files to outfits/Default/")

    # Copy emotion buttons (buttonX_off.png -> sprite name)
    src_emotions_dir = base_dir / "emotions"
    copied = 0
    if src_emotions_dir.exists():
        for i, name in enumerate(sprite_names, start=1):
            src = src_emotions_dir / f"button{i}_off.png"
            if src.exists():
                shutil.copy2(str(src), str(emotions_dir / f"{name}.png"))
                copied += 1
    print(f"  Copied {copied} emotion buttons to outfits/Default/emotions/")

    print("\nPorting complete!")


if __name__ == "__main__":
    main()

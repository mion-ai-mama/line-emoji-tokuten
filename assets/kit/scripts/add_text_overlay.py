#!/usr/bin/env python3
"""表情差分フレームに短いセリフ文字を合成する（Pillowのみで完結）。

使い方:
    python add_text_overlay.py --frames-dir ./frames --output-dir ./frames_with_text \
        --text "了解！" --font ./NotoSansJP-Bold.ttf --font-size 36
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

OUTLINE_WIDTH = 3
BOTTOM_MARGIN_RATIO = 0.08


def load_font(font_path: Path, font_size: int) -> ImageFont.FreeTypeFont:
    if not font_path.exists():
        raise SystemExit(
            f"フォントが見つかりません: {font_path}\n"
            "日本語フォント（例: Noto Sans JP）をダウンロードして --font で指定してください。"
        )
    return ImageFont.truetype(str(font_path), font_size)


def draw_outlined_text(
    draw: ImageDraw.ImageDraw,
    xy: tuple[float, float],
    text: str,
    font: ImageFont.FreeTypeFont,
) -> None:
    x, y = xy
    for dx in range(-OUTLINE_WIDTH, OUTLINE_WIDTH + 1):
        for dy in range(-OUTLINE_WIDTH, OUTLINE_WIDTH + 1):
            if dx or dy:
                draw.text((x + dx, y + dy), text, font=font, fill="white", anchor="mm")
    draw.text((x, y), text, font=font, fill="black", anchor="mm")


def overlay_text(image_path: Path, text: str, font: ImageFont.FreeTypeFont) -> Image.Image:
    image = Image.open(image_path).convert("RGBA")
    draw = ImageDraw.Draw(image)
    x = image.width / 2
    y = image.height * (1 - BOTTOM_MARGIN_RATIO)
    draw_outlined_text(draw, (x, y), text, font)
    return image


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--frames-dir", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--text", type=str, required=True)
    parser.add_argument("--font", type=Path, required=True)
    parser.add_argument("--font-size", type=int, default=36)
    return parser.parse_args(argv)


def main(argv: list[str]) -> int:
    args = parse_args(argv)
    font = load_font(args.font, args.font_size)
    frame_paths = sorted(args.frames_dir.glob("*.png"))
    if not frame_paths:
        raise SystemExit(f"PNGフレームが見つかりません: {args.frames_dir}")
    args.output_dir.mkdir(parents=True, exist_ok=True)
    for path in frame_paths:
        result = overlay_text(path, args.text, font)
        result.save(args.output_dir / path.name)
    print(f"✅ 文字入れ完了: {len(frame_paths)}枚 → {args.output_dir}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))

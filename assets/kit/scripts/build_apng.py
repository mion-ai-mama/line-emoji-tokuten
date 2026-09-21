#!/usr/bin/env python3
"""LINEアニメーションスタンプ仕様に沿ってPNG連番をAPNGへ合成する。

使い方:
    python build_apng.py --frames-dir ./frames --output ./output.png \
        --duration-ms 200 --loop 2
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

from apng import APNG
from PIL import Image

MAX_WIDTH = 320
MAX_HEIGHT = 270
MIN_LONG_SIDE = 270
MIN_FRAMES = 5
MAX_FRAMES = 20
MIN_LOOP = 1
MAX_LOOP = 4
MAX_TOTAL_DURATION_MS = 4000
MAX_FILE_SIZE_BYTES = 300 * 1024


def load_frame_paths(frames_dir: Path) -> list[Path]:
    paths = sorted(frames_dir.glob("*.png"))
    if not paths:
        raise SystemExit(f"PNGフレームが見つかりません: {frames_dir}")
    return paths


def validate_frame_count(paths: list[Path]) -> None:
    count = len(paths)
    if not (MIN_FRAMES <= count <= MAX_FRAMES):
        raise SystemExit(
            f"フレーム数が仕様外です: {count}枚（{MIN_FRAMES}〜{MAX_FRAMES}枚にしてください）"
        )


def validate_canvas(paths: list[Path]) -> tuple[int, int]:
    sizes = {Image.open(p).size for p in paths}
    if len(sizes) != 1:
        raise SystemExit(f"フレームごとにサイズが違います: {sorted(sizes)}")
    width, height = sizes.pop()
    if width > MAX_WIDTH or height > MAX_HEIGHT:
        raise SystemExit(
            f"キャンバスサイズが上限超過です: {width}x{height}"
            f"（上限 {MAX_WIDTH}x{MAX_HEIGHT}）"
        )
    if max(width, height) < MIN_LONG_SIDE:
        raise SystemExit(
            f"キャンバスサイズが小さすぎます: {width}x{height}"
            f"（長辺は{MIN_LONG_SIDE}px以上にしてください）"
        )
    return width, height


def validate_timing(frame_count: int, duration_ms: int, loop: int) -> None:
    if not (MIN_LOOP <= loop <= MAX_LOOP):
        raise SystemExit(
            f"ループ回数が仕様外です: {loop}（{MIN_LOOP}〜{MAX_LOOP}回にしてください）"
        )
    total_ms = frame_count * duration_ms
    if total_ms > MAX_TOTAL_DURATION_MS:
        raise SystemExit(
            f"1ループの再生時間が長すぎます: {total_ms}ms"
            f"（上限 {MAX_TOTAL_DURATION_MS}ms。フレーム数かduration-msを減らしてください）"
        )


def build_apng(paths: list[Path], output: Path, duration_ms: int, loop: int) -> None:
    apng = APNG()
    for path in paths:
        apng.append_file(str(path), delay=duration_ms, delay_den=1000)
    apng.num_plays = loop
    apng.save(str(output))


def validate_file_size(output: Path) -> None:
    size = output.stat().st_size
    if size > MAX_FILE_SIZE_BYTES:
        raise SystemExit(
            f"書き出したAPNGが上限を超えています: {size / 1024:.1f}KB"
            f"（上限 {MAX_FILE_SIZE_BYTES / 1024:.0f}KB。"
            "フレーム数や色数を減らして再生成してください）"
        )


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--frames-dir", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--duration-ms", type=int, default=200)
    parser.add_argument("--loop", type=int, default=2)
    return parser.parse_args(argv)


def main(argv: list[str]) -> int:
    args = parse_args(argv)
    paths = load_frame_paths(args.frames_dir)
    validate_frame_count(paths)
    validate_canvas(paths)
    validate_timing(len(paths), args.duration_ms, args.loop)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    build_apng(paths, args.output, args.duration_ms, args.loop)
    validate_file_size(args.output)
    print(f"✅ 作成完了: {args.output}（{len(paths)}フレーム / {args.loop}ループ）")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))

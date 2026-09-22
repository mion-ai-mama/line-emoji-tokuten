#!/usr/bin/env python3
"""LINE動く絵文字の仕様に沿って、PNG連番からAPNGを組み立てる（Pillow単体・外部パッケージ不要）。

使い方:
    python build_apng.py --frames-dir ./frames --output ./001.png \
        --duration-ms 100 --loop 3
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

from PIL import Image, PngImagePlugin

CANVAS_SIZE = (180, 180)
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
    size = sizes.pop()
    if size != CANVAS_SIZE:
        raise SystemExit(
            f"キャンバスサイズが仕様外です: {size[0]}x{size[1]}"
            f"（動く絵文字は {CANVAS_SIZE[0]}x{CANVAS_SIZE[1]} 固定にしてください）"
        )
    return size


def validate_timing(frame_count: int, duration_ms: int, loop: int) -> None:
    if not (MIN_LOOP <= loop <= MAX_LOOP):
        raise SystemExit(
            f"ループ回数が仕様外です: {loop}（{MIN_LOOP}〜{MAX_LOOP}回にしてください）"
        )
    loop_ms = frame_count * duration_ms
    if loop_ms % 1000 != 0:
        raise SystemExit(
            f"1ループの再生時間が半端な秒数です: {loop_ms}ms"
            "（LINE審査は『ちょうど1/2/3/4秒』以外を弾きます。frames×duration-msが"
            "1000の倍数になるようにしてください）"
        )
    total_ms = loop_ms * loop
    if total_ms > MAX_TOTAL_DURATION_MS:
        raise SystemExit(
            f"合計再生時間が長すぎます: {total_ms}ms"
            f"（上限 {MAX_TOTAL_DURATION_MS}ms。フレーム数・duration-ms・loopを見直してください）"
        )


def build_apng(paths: list[Path], output: Path, duration_ms: int, loop: int) -> None:
    """Pillow単体でAPNGを書き出す（外部パッケージapngは使わない。
    ChatGPT/Codexの実行環境にapngパッケージが入っていないことがあり、
    pip installもできない場合があるため、標準で入っているPillowのみに一本化している）。"""
    frames = [Image.open(p).convert("RGBA") for p in paths]
    frames[0].save(
        output,
        format="PNG",
        save_all=True,
        append_images=frames[1:],
        duration=duration_ms,
        loop=loop,
        disposal=PngImagePlugin.Disposal.OP_BACKGROUND,
        blend=PngImagePlugin.Blend.OP_SOURCE,
    )


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
    parser.add_argument("--duration-ms", type=int, default=100)
    parser.add_argument("--loop", type=int, default=3)
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

#!/usr/bin/env python3
"""動くLINE絵文字セットを、1枚のグリッド画像から一括生成するパイプライン。

ChatGPTのコード実行機能（Code Interpreter）内で、この会話にアップロードされた
グリッド画像・構成JSON（例: 8-emoji-set-plan.json）と組み合わせて使うことを想定している。

サブコマンド:
    slice   グリッド画像を「絵文字ごと・フレームごと」に切り出し、180x180で中央配置する
    build   切り出したフレームから、絵文字ごとに1本のAPNGを作る（build_apng.pyを利用）
    tab     トークルームタブ画像（96x74）を1個作る
    pack    APNG一式とタブ画像をZIPにまとめる
    all     slice -> build -> tab -> pack を一括実行する

使い方の例:
    python emoji_pipeline.py all --grid grid.png --plan 8-emoji-set-plan.json --out-dir output
"""
from __future__ import annotations

import argparse
import json
import sys
import zipfile
from pathlib import Path

from PIL import Image

import build_apng

CANVAS_SIZE = build_apng.CANVAS_SIZE
USABLE_SIZE = 152
BG_COLOR_TOLERANCE = 18
MAX_ZIP_SIZE_BYTES = 20 * 1024 * 1024
TAB_SIZE = (96, 74)


def load_plan(plan_path: Path) -> dict:
    plan = json.loads(plan_path.read_text(encoding="utf-8"))
    frame_counts = {item["frames"] for item in plan["items"]}
    if len(frame_counts) != 1:
        raise SystemExit(
            "このパイプラインは、全アイテムのフレーム数が同じであることを前提にしています。"
            f" 構成JSONのframesを揃えてください: {sorted(frame_counts)}"
        )
    return plan


def remove_near_background(image: Image.Image, bg_color=(255, 255, 255)) -> Image.Image:
    """画像にほぼ透明なピクセルが無い（＝背景が透過されていない）場合、
    指定の背景色に近いピクセルを透明化する簡易背景抜き。"""
    image = image.convert("RGBA")
    pixels = list(image.getdata())
    has_alpha_variance = any(p[3] < 250 for p in pixels)
    if has_alpha_variance:
        return image
    new_pixels = [
        (r, g, b, 0)
        if abs(r - bg_color[0]) <= BG_COLOR_TOLERANCE
        and abs(g - bg_color[1]) <= BG_COLOR_TOLERANCE
        and abs(b - bg_color[2]) <= BG_COLOR_TOLERANCE
        else (r, g, b, a)
        for r, g, b, a in pixels
    ]
    image.putdata(new_pixels)
    return image


def crop_to_content(image: Image.Image) -> Image.Image:
    bbox = image.getbbox()
    return image.crop(bbox) if bbox else image


def center_on_canvas(image: Image.Image) -> Image.Image:
    image.thumbnail((USABLE_SIZE, USABLE_SIZE), Image.LANCZOS)
    canvas = Image.new("RGBA", CANVAS_SIZE, (0, 0, 0, 0))
    x = (CANVAS_SIZE[0] - image.width) // 2
    y = (CANVAS_SIZE[1] - image.height) // 2
    canvas.paste(image, (x, y), image)
    return canvas


def slice_grid(grid_path: Path, plan: dict, out_dir: Path) -> None:
    grid = Image.open(grid_path).convert("RGBA")
    items = plan["items"]
    cols = items[0]["frames"]
    rows = len(items)
    cell_w = grid.width / cols
    cell_h = grid.height / rows
    for row, item in enumerate(items):
        item_dir = out_dir / "frames" / item["number"]
        item_dir.mkdir(parents=True, exist_ok=True)
        for col in range(cols):
            box = (
                round(col * cell_w),
                round(row * cell_h),
                round((col + 1) * cell_w),
                round((row + 1) * cell_h),
            )
            cell = grid.crop(box)
            cell = remove_near_background(cell)
            cell = crop_to_content(cell)
            cell = center_on_canvas(cell)
            cell.save(item_dir / f"{col + 1:02d}.png")
    print(f"✅ 切り出し完了: {rows}個 × {cols}フレーム → {out_dir / 'frames'}")


def build_items(plan: dict, out_dir: Path) -> None:
    for item in plan["items"]:
        frame_dir = out_dir / "frames" / item["number"]
        frame_paths = sorted(frame_dir.glob("*.png"))
        build_apng.validate_frame_count(frame_paths)
        build_apng.validate_canvas(frame_paths)
        build_apng.validate_timing(len(frame_paths), plan["frame_duration_ms"], plan["loop_count"])
        output_path = out_dir / f"{item['number']}.png"
        build_apng.build_apng(frame_paths, output_path, plan["frame_duration_ms"], plan["loop_count"])
        build_apng.validate_file_size(output_path)
        print(f"✅ {item['number']}（{item['meaning']}）を作成: {output_path}")


def make_tab(source_path: Path, out_path: Path) -> None:
    image = Image.open(source_path).convert("RGBA")
    content = crop_to_content(image) or image
    scale = min(TAB_SIZE[0] / content.width, TAB_SIZE[1] / content.height)
    resized = content.resize((max(1, round(content.width * scale)), max(1, round(content.height * scale))), Image.LANCZOS)
    canvas = Image.new("RGBA", TAB_SIZE, (0, 0, 0, 0))
    x = (TAB_SIZE[0] - resized.width) // 2
    y = (TAB_SIZE[1] - resized.height) // 2
    canvas.paste(resized, (x, y), resized)
    canvas.save(out_path)
    print(f"✅ タブ画像を作成: {out_path}")


def pack(plan: dict, out_dir: Path, zip_path: Path) -> None:
    files = [out_dir / f"{item['number']}.png" for item in plan["items"]]
    files.append(out_dir / "tab.png")
    missing = [f for f in files if not f.exists()]
    if missing:
        raise SystemExit(f"ZIPに入れるファイルが見つかりません: {missing}")
    zip_path.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
        for f in files:
            zf.write(f, arcname=f.name)
    size = zip_path.stat().st_size
    if size > MAX_ZIP_SIZE_BYTES:
        raise SystemExit(
            f"ZIPが上限を超えています: {size / 1024 / 1024:.1f}MB（上限 20MB）"
        )
    print(f"✅ ZIP作成完了: {zip_path}（{size / 1024:.0f}KB）")
    print("※ 申請画面でのファイル名の指定は、LINE Creators Marketの登録画面の指示に従ってください。")


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)

    p_slice = sub.add_parser("slice", help="グリッド画像をフレームごとに切り出す")
    p_slice.add_argument("--grid", type=Path, required=True)
    p_slice.add_argument("--plan", type=Path, required=True)
    p_slice.add_argument("--out-dir", type=Path, required=True)

    p_build = sub.add_parser("build", help="フレームからAPNGを作る")
    p_build.add_argument("--plan", type=Path, required=True)
    p_build.add_argument("--out-dir", type=Path, required=True)

    p_tab = sub.add_parser("tab", help="タブ画像を作る")
    p_tab.add_argument("--source", type=Path, required=True)
    p_tab.add_argument("--out", type=Path, required=True)

    p_pack = sub.add_parser("pack", help="ZIPにまとめる")
    p_pack.add_argument("--plan", type=Path, required=True)
    p_pack.add_argument("--out-dir", type=Path, required=True)
    p_pack.add_argument("--zip", type=Path, required=True)

    p_all = sub.add_parser("all", help="slice -> build -> tab -> pack を一括実行")
    p_all.add_argument("--grid", type=Path, required=True)
    p_all.add_argument("--plan", type=Path, required=True)
    p_all.add_argument("--out-dir", type=Path, required=True)
    p_all.add_argument("--zip", type=Path, required=True)

    return parser.parse_args(argv)


def main(argv: list[str]) -> int:
    args = parse_args(argv)

    if args.command == "slice":
        slice_grid(args.grid, load_plan(args.plan), args.out_dir)
    elif args.command == "build":
        build_items(load_plan(args.plan), args.out_dir)
    elif args.command == "tab":
        make_tab(args.source, args.out)
    elif args.command == "pack":
        pack(load_plan(args.plan), args.out_dir, args.zip)
    elif args.command == "all":
        plan = load_plan(args.plan)
        slice_grid(args.grid, plan, args.out_dir)
        build_items(plan, args.out_dir)
        make_tab(args.out_dir / f"{plan['items'][0]['number']}.png", args.out_dir / "tab.png")
        pack(plan, args.out_dir, args.zip)

    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))

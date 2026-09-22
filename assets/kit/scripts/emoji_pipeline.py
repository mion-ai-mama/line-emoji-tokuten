#!/usr/bin/env python3
"""動くLINE絵文字セットを、生成した画像から一括処理するパイプライン。

ChatGPTのコード実行機能（Code Interpreter）内で、この会話にアップロードされた
構成JSON（例: 8-emoji-set-plan.json）と組み合わせて使うことを想定している。

推奨フロー（1個ずつ個別生成。8個を1枚にまとめて生成するより見分けやすくなる）:
    1. 8個それぞれを、マスター画像を参照しながら1個ずつ「1行×6列」の帯画像として
       個別に画像生成し、strips/001.png 〜 strips/008.png として保存する
    2. slice-items  strips/配下の8枚から、絵文字ごとのフレームを切り出す
    3. build        切り出したフレームから、絵文字ごとに1本のAPNGを作る（build_apng.pyを利用）
    4. tab          トークルームタブ画像（96x74）を1個作る
    5. review       8個それぞれの帯画像とチェックリスト雛形（checklist_TO_FILL.json）を作る。
                     packの前に必ず実行し、雛形の各checksを実際に目視確認してtrue/falseで埋める
    6. pack         review済みのchecklist（--review）を検証したうえでAPNG一式とタブ画像をZIPにまとめる。
                     checksが埋まっていない・falseの項目があれば停止しZIPを作らない

サブコマンド一覧:
    slice-items  strips/{番号}.png（1個ぶんの1行×6列）から個別にフレームを切り出す（推奨）
    slice        1枚の8行×6列グリッド画像から一括でフレームを切り出す（旧方式・互換用）
    build        切り出したフレームから、絵文字ごとに1本のAPNGを作る
    tab          トークルームタブ画像（96x74）を1個作る
    review       レビュー用の帯画像とchecklist_TO_FILL.jsonを作る
    pack         review済みのchecklistを検証したうえでZIPにまとめる
    all          slice -> build -> tab -> review を一括実行する（旧方式・互換用。packは別途）

使い方の例（推奨フロー）:
    python emoji_pipeline.py slice-items --strips-dir strips --plan 8-emoji-set-plan.json --out-dir output
    python emoji_pipeline.py build --plan 8-emoji-set-plan.json --out-dir output
    python emoji_pipeline.py tab --source output/001.png --out output/tab.png
    python emoji_pipeline.py review --plan 8-emoji-set-plan.json --out-dir output
    （output/review/checklist_TO_FILL.json を目視確認して埋めたあと）
    python emoji_pipeline.py pack --plan 8-emoji-set-plan.json --out-dir output \\
        --zip output/line-emoji-set.zip --review output/review/checklist_TO_FILL.json
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
REVIEW_CHECK_NAMES = (
    "motion_matches_plan",
    "no_semantic_duplicate",
    "hand_and_arm_shape_correct",
    "no_clipping_or_cropping",
    "readable",
)


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


def _slice_row(row_image: Image.Image, cols: int, item_dir: Path) -> None:
    item_dir.mkdir(parents=True, exist_ok=True)
    cell_w = row_image.width / cols
    for col in range(cols):
        box = (round(col * cell_w), 0, round((col + 1) * cell_w), row_image.height)
        cell = row_image.crop(box)
        cell = remove_near_background(cell)
        cell = crop_to_content(cell)
        cell = center_on_canvas(cell)
        cell.save(item_dir / f"{col + 1:02d}.png")


def slice_grid(grid_path: Path, plan: dict, out_dir: Path) -> None:
    """1枚の8行×6列グリッド画像から一括でフレームを切り出す（旧方式・互換用）。"""
    grid = Image.open(grid_path).convert("RGBA")
    items = plan["items"]
    cols = items[0]["frames"]
    rows = len(items)
    cell_h = grid.height / rows
    for row, item in enumerate(items):
        box = (0, round(row * cell_h), grid.width, round((row + 1) * cell_h))
        row_image = grid.crop(box)
        _slice_row(row_image, cols, out_dir / "frames" / item["number"])
    print(f"✅ 切り出し完了: {rows}個 × {cols}フレーム → {out_dir / 'frames'}")


def slice_items(strips_dir: Path, plan: dict, out_dir: Path) -> None:
    """strips/{番号}.png（1個ぶんの1行×6列の帯画像）から個別にフレームを切り出す（推奨）。"""
    items = plan["items"]
    missing = [it["number"] for it in items if not (strips_dir / f"{it['number']}.png").exists()]
    if missing:
        raise SystemExit(f"帯画像が見つかりません（{strips_dir}）: {missing}")
    for item in items:
        strip = Image.open(strips_dir / f"{item['number']}.png").convert("RGBA")
        _slice_row(strip, item["frames"], out_dir / "frames" / item["number"])
    print(f"✅ 切り出し完了: {len(items)}個 → {out_dir / 'frames'}")


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


def _build_review_strip(item: dict, out_dir: Path, review_dir: Path) -> None:
    frame_dir = out_dir / "frames" / item["number"]
    frame_paths = sorted(frame_dir.glob("*.png"))
    if not frame_paths:
        raise SystemExit(f"レビュー画像を作れません。先にslice-items/sliceを実行してください: {item['number']}")
    thumbs = [Image.open(p).convert("RGBA").resize((90, 90), Image.LANCZOS) for p in frame_paths]
    strip = Image.new("RGBA", (90 * len(thumbs), 90), (255, 255, 255, 255))
    for i, thumb in enumerate(thumbs):
        strip.paste(thumb, (90 * i, 0), thumb)
    strip.convert("RGB").save(review_dir / f"{item['number']}.png")


def make_review(plan: dict, out_dir: Path) -> None:
    """8個それぞれの帯画像とチェックリスト雛形（checklist_TO_FILL.json）を作る。"""
    review_dir = out_dir / "review"
    review_dir.mkdir(parents=True, exist_ok=True)
    checklist = {"items": []}
    for item in plan["items"]:
        _build_review_strip(item, out_dir, review_dir)
        checklist["items"].append(
            {
                "number": item["number"],
                "meaning": item["meaning"],
                "motion": item["motion"],
                "checks": {name: None for name in REVIEW_CHECK_NAMES},
                "observation": "",
            }
        )
    checklist_path = review_dir / "checklist_TO_FILL.json"
    checklist_path.write_text(json.dumps(checklist, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"✅ レビュー用画像とチェックリスト雛形を作成: {review_dir}")
    print("次に、review/{番号}.png を1枚ずつ実際に見て、checklist_TO_FILL.jsonのchecksを")
    print("true/falseで埋め、observationに具体的な観察を書いてください（省略・虚偽記入は禁止）。")
    print("特にno_semantic_duplicateは、他の番号と腕の位置・手の形が同じに見えないかを見て判定すること。")


def load_checklist(checklist_path: Path, plan: dict) -> dict:
    checklist = json.loads(checklist_path.read_text(encoding="utf-8"))
    by_number = {it["number"]: it for it in checklist.get("items", [])}
    plan_numbers = [item["number"] for item in plan["items"]]
    missing = [n for n in plan_numbers if n not in by_number]
    if missing:
        raise SystemExit(f"チェックリストに番号が足りません: {missing}")
    failed = []
    for number in plan_numbers:
        entry = by_number[number]
        checks = entry.get("checks", {})
        for name in REVIEW_CHECK_NAMES:
            if checks.get(name) is not True:
                failed.append(f"{number}: {name} が true になっていません（現在: {checks.get(name)!r}）")
        if not entry.get("observation", "").strip():
            failed.append(f"{number}: observationが空です（実際に見た内容を書くこと）")
    if failed:
        raise SystemExit(
            "チェックリストが未完了、または不一致が見つかりました。ZIPを作成できません:\n"
            + "\n".join(f"  - {f}" for f in failed)
        )
    return checklist


def pack(plan: dict, out_dir: Path, zip_path: Path, review_path: Path) -> None:
    load_checklist(review_path, plan)
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

    p_slice_items = sub.add_parser("slice-items", help="1個ずつの帯画像からフレームを切り出す（推奨）")
    p_slice_items.add_argument("--strips-dir", type=Path, required=True)
    p_slice_items.add_argument("--plan", type=Path, required=True)
    p_slice_items.add_argument("--out-dir", type=Path, required=True)

    p_slice = sub.add_parser("slice", help="1枚のグリッド画像からフレームごとに切り出す（旧方式）")
    p_slice.add_argument("--grid", type=Path, required=True)
    p_slice.add_argument("--plan", type=Path, required=True)
    p_slice.add_argument("--out-dir", type=Path, required=True)

    p_build = sub.add_parser("build", help="フレームからAPNGを作る")
    p_build.add_argument("--plan", type=Path, required=True)
    p_build.add_argument("--out-dir", type=Path, required=True)

    p_tab = sub.add_parser("tab", help="タブ画像を作る")
    p_tab.add_argument("--source", type=Path, required=True)
    p_tab.add_argument("--out", type=Path, required=True)

    p_review = sub.add_parser("review", help="レビュー用画像とchecklist_TO_FILL.jsonを作る")
    p_review.add_argument("--plan", type=Path, required=True)
    p_review.add_argument("--out-dir", type=Path, required=True)

    p_pack = sub.add_parser("pack", help="review済みcheckを検証してZIPにまとめる")
    p_pack.add_argument("--plan", type=Path, required=True)
    p_pack.add_argument("--out-dir", type=Path, required=True)
    p_pack.add_argument("--zip", type=Path, required=True)
    p_pack.add_argument("--review", type=Path, required=True)

    p_all = sub.add_parser("all", help="slice -> build -> tab -> review を一括実行（旧方式）")
    p_all.add_argument("--grid", type=Path, required=True)
    p_all.add_argument("--plan", type=Path, required=True)
    p_all.add_argument("--out-dir", type=Path, required=True)

    return parser.parse_args(argv)


def main(argv: list[str]) -> int:
    args = parse_args(argv)

    if args.command == "slice-items":
        slice_items(args.strips_dir, load_plan(args.plan), args.out_dir)
    elif args.command == "slice":
        slice_grid(args.grid, load_plan(args.plan), args.out_dir)
    elif args.command == "build":
        build_items(load_plan(args.plan), args.out_dir)
    elif args.command == "tab":
        make_tab(args.source, args.out)
    elif args.command == "review":
        make_review(load_plan(args.plan), args.out_dir)
    elif args.command == "pack":
        pack(load_plan(args.plan), args.out_dir, args.zip, args.review)
    elif args.command == "all":
        plan = load_plan(args.plan)
        slice_grid(args.grid, plan, args.out_dir)
        build_items(plan, args.out_dir)
        make_tab(args.out_dir / f"{plan['items'][0]['number']}.png", args.out_dir / "tab.png")
        make_review(plan, args.out_dir)

    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))

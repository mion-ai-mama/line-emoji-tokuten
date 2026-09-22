#!/usr/bin/env python3
"""LINE静止絵文字セット（40個）を、1枚のグリッド画像から一括処理するパイプライン。

ChatGPTのコード実行機能（Code Interpreter）内で、この会話にアップロードされた
構成JSON（40-emoji-set-plan.json）と組み合わせて使うことを想定している。

推奨フロー:
    1. マスター画像を参照しながら、40個を8行×5列の1枚のグリッド画像として
       一括生成し、grid.pngとして保存する
    2. slice     grid.pngから40個ぶんを切り出し、180x180で中央配置する
    3. tab       トークルームタブ画像（96x74）を1個作る
    4. review    40個それぞれのプレビュー画像とチェックリスト雛形を作る。
                 packの前に必ず実行し、雛形の各checksを実際に目視確認してtrue/falseで埋める
    5. pack      review済みのchecklist（--review）を検証したうえでZIPにまとめる。
                 checksが埋まっていない・falseの項目があれば停止しZIPを作らない

サブコマンド一覧:
    slice   グリッド画像から40個を切り出し、180x180で中央配置する
    tab     トークルームタブ画像（96x74）を1個作る
    review  レビュー用画像とchecklist_TO_FILL.jsonを作る
    pack    review済みのchecklistを検証したうえでZIPにまとめる
    all     slice -> tab -> review を一括実行する（packは別途、目視確認後に実行する）

使い方の例:
    python emoji_pipeline.py all --grid grid.png --plan 40-emoji-set-plan.json --out-dir output
    （output/review/checklist_TO_FILL.json を目視確認して埋めたあと）
    python emoji_pipeline.py pack --plan 40-emoji-set-plan.json --out-dir output \\
        --zip output/line-emoji-set.zip --review output/review/checklist_TO_FILL.json
"""
from __future__ import annotations

import argparse
import json
import sys
import zipfile
from pathlib import Path

from PIL import Image

CANVAS_SIZE = (180, 180)
USABLE_SIZE = 152
BG_COLOR_TOLERANCE = 18
MAX_ZIP_SIZE_BYTES = 20 * 1024 * 1024
MAX_FILE_SIZE_BYTES = 1024 * 1024
TAB_SIZE = (96, 74)
REVIEW_CHECK_NAMES = (
    "meaning_matches",
    "no_semantic_duplicate",
    "no_clipping_or_cropping",
    "readable",
    "background_transparent",
)


def load_plan(plan_path: Path) -> dict:
    plan = json.loads(plan_path.read_text(encoding="utf-8"))
    expected = plan["grid_rows"] * plan["grid_cols"]
    if len(plan["items"]) != expected:
        raise SystemExit(
            f"itemsの数（{len(plan['items'])}）がgrid_rows×grid_cols（{expected}）と一致しません。"
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
    cols = plan["grid_cols"]
    rows = plan["grid_rows"]
    cell_w = grid.width / cols
    cell_h = grid.height / rows
    out_dir.mkdir(parents=True, exist_ok=True)
    for index, item in enumerate(items):
        row, col = divmod(index, cols)
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
        output_path = out_dir / f"{item['number']}.png"
        cell.save(output_path)
        size = output_path.stat().st_size
        if size > MAX_FILE_SIZE_BYTES:
            raise SystemExit(
                f"{item['number']}.pngが上限を超えています: {size / 1024:.1f}KB"
                f"（上限 {MAX_FILE_SIZE_BYTES / 1024:.0f}KB。色数を減らして再生成してください）"
            )
    print(f"✅ 切り出し完了: {rows}行×{cols}列 → {len(items)}個 → {out_dir}")


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


def make_review(plan: dict, out_dir: Path) -> None:
    """40個それぞれのプレビュー画像とチェックリスト雛形（checklist_TO_FILL.json）を作る。"""
    review_dir = out_dir / "review"
    review_dir.mkdir(parents=True, exist_ok=True)
    checklist = {"items": []}
    for item in plan["items"]:
        source_path = out_dir / f"{item['number']}.png"
        if not source_path.exists():
            raise SystemExit(f"レビュー画像を作れません。先にsliceを実行してください: {item['number']}")
        Image.open(source_path).convert("RGBA").save(review_dir / f"{item['number']}.png")
        checklist["items"].append(
            {
                "number": item["number"],
                "meaning": item["meaning"],
                "description": item["description"],
                "checks": {name: None for name in REVIEW_CHECK_NAMES},
                "observation": "",
            }
        )
    checklist_path = review_dir / "checklist_TO_FILL.json"
    checklist_path.write_text(json.dumps(checklist, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"✅ レビュー用画像とチェックリスト雛形を作成: {review_dir}")
    print("次に、review/{番号}.png を1枚ずつ実際に見て、checklist_TO_FILL.jsonのchecksを")
    print("true/falseで埋め、observationに具体的な観察を書いてください（省略・虚偽記入は禁止）。")
    print("特にno_semantic_duplicateは、他の番号と表情・手の位置・小物が同じに見えないかを見て判定すること。")


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

    p_slice = sub.add_parser("slice", help="グリッド画像から40個を切り出す")
    p_slice.add_argument("--grid", type=Path, required=True)
    p_slice.add_argument("--plan", type=Path, required=True)
    p_slice.add_argument("--out-dir", type=Path, required=True)

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

    p_all = sub.add_parser("all", help="slice -> tab -> review を一括実行")
    p_all.add_argument("--grid", type=Path, required=True)
    p_all.add_argument("--plan", type=Path, required=True)
    p_all.add_argument("--out-dir", type=Path, required=True)

    return parser.parse_args(argv)


def main(argv: list[str]) -> int:
    args = parse_args(argv)

    if args.command == "slice":
        slice_grid(args.grid, load_plan(args.plan), args.out_dir)
    elif args.command == "tab":
        make_tab(args.source, args.out)
    elif args.command == "review":
        make_review(load_plan(args.plan), args.out_dir)
    elif args.command == "pack":
        pack(load_plan(args.plan), args.out_dir, args.zip, args.review)
    elif args.command == "all":
        plan = load_plan(args.plan)
        slice_grid(args.grid, plan, args.out_dir)
        make_tab(args.out_dir / f"{plan['items'][0]['number']}.png", args.out_dir / "tab.png")
        make_review(plan, args.out_dir)

    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))

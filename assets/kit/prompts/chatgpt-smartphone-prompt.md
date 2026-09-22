# スマホだけで作る（ChatGPTアプリ用・ファイルの添付は不要）

## 事前準備

1. スマホでChatGPTのアプリを開き、**新しいチャット**を開く
2. 下の指示文を**全文コピーして、そのまま最初のメッセージとして送るだけ**
   （ファイルのダウンロード・解凍・添付は一切不要です。必要な中身はすべてこの指示文の中に入っています）

※ この方法は、ChatGPTで「コード実行（Data Analysis／Code Interpreter）」が使えるプラン・環境が必要です。

---

あなたはこの会話内で、LINE静止絵文字セット（40個）の制作を最後まで実行する担当です。

説明だけで終わらず、必要な場面では実際に画像生成・コード実行を行い、
最終的にダウンロード可能なZIPファイル（`line-emoji-set.zip`）まで完成させてください。

別チャットへの移動や、長いプロンプトの再入力をユーザーに求めないでください。

## 【最初にやること：作業ファイルの準備】

ユーザーはファイルを添付していません。まず、以下の2つの内容を、書かれているファイル名の
まま**一字一句そのまま**コード実行環境に保存してください（内容を書き換えたり要約したりしない）。

`40-emoji-set-plan.json` として保存する内容：

```json
{
  "canvas": { "width": 180, "height": 180 },
  "grid_layout": "8行×5列の1枚画像（40個・静止画）",
  "grid_rows": 8,
  "grid_cols": 5,
  "distinctness_note": "40個は4つのグループ（表情20・生活シーン10・単独アイコン3・ふきだし文字7）に分かれており、グループが違うだけでも見た目は大きく異なる。同じグループ内で特に紛らわしいペアに注意する：002（合掌して前傾＝ありがとう）と030（両手を合わせて拝む＝お願い、こちらは眉を下げた困り顔・少し前かがみでねだる表情にする）／009（両足は地面につけたまま両手だけ上げる＝うれしい）と028（両手両足を広げて跳ねる＝ジャンプ、こちらは足が地面から離れている）／004（前かがみで片手を膝に置いて大笑い）と013（腕組みでほっぺを膨らませて怒る、手の位置が全く違う）。各項目は表情・手の位置・小物のうち複数を変えて他と重ならないようにする。",
  "items": [
    { "number": "001", "category": "expression", "meaning": "こんにちは", "description": "片手を顔の横で左右に振る。もう片方の手は体の横。にっこり笑顔。" },
    { "number": "002", "category": "expression", "meaning": "ありがとう", "description": "両手のひらを胸の前で合わせ（合掌）、上半身を軽く前に倒す。おだやかな笑顔。" },
    { "number": "003", "category": "expression", "meaning": "OK・了解", "description": "片手でOKサイン（親指と人差し指で輪を作る）を頬の高さに。もう片方の手は腰。自信ありげな笑顔。" },
    { "number": "004", "category": "expression", "meaning": "大笑い", "description": "上半身を前にかがめ、片手を軽く膝に置く。口を大きく開けて大笑い。" },
    { "number": "005", "category": "expression", "meaning": "ごめんね", "description": "両手を体の横に力なく下げ、肩を落として頭を下げる。困り眉。" },
    { "number": "006", "category": "expression", "meaning": "がんばる", "description": "片手をこぶしにして頭より高く突き上げる。もう片方の手は腰。決意の表情。" },
    { "number": "007", "category": "expression", "meaning": "おやすみ", "description": "片方の頬に両手を添えて首を軽くかしげる。目を閉じて眠そう。" },
    { "number": "008", "category": "expression", "meaning": "びっくり", "description": "両手を顔の横でパッと開く。目を大きく見開く。" },
    { "number": "009", "category": "expression", "meaning": "うれしい", "description": "両足は地面につけたまま、両手を頭の上に上げる。満面の笑顔。" },
    { "number": "010", "category": "expression", "meaning": "泣き笑い", "description": "目に涙をためながら口は笑顔。片手で目元を拭う。" },
    { "number": "011", "category": "expression", "meaning": "照れる", "description": "両手を両頬に当てて赤面。もじもじした表情。" },
    { "number": "012", "category": "expression", "meaning": "悲しい", "description": "両手を目に当てて泣く。肩を落として下を向く。" },
    { "number": "013", "category": "expression", "meaning": "怒る", "description": "腕を組み、頬をふくらませてプンプンした表情。" },
    { "number": "014", "category": "expression", "meaning": "考え中", "description": "片手を顎に当てて斜め上を見る。考え込む表情。" },
    { "number": "015", "category": "expression", "meaning": "ひらめいた", "description": "片手の人差し指を立てて頭の上に。目を輝かせる。頭上に軽い光の演出。" },
    { "number": "016", "category": "expression", "meaning": "眠い", "description": "半目で、片手を口に当ててあくび。" },
    { "number": "017", "category": "expression", "meaning": "拍手", "description": "両手を顔の横で合わせてパチパチと拍手。目を細めた笑顔。" },
    { "number": "018", "category": "expression", "meaning": "ハートを送る", "description": "両手で小さなハートの形を作り、体の前に出す。" },
    { "number": "019", "category": "expression", "meaning": "ため息", "description": "肩を落とし、片手で額を軽く押さえる。疲れた表情。" },
    { "number": "020", "category": "expression", "meaning": "ウインク", "description": "片目を閉じ、もう片方の手で小さくピースサイン。" },
    { "number": "021", "category": "pose", "meaning": "スマホを見る", "description": "スマホを両手で持ち、画面をのぞき込む。" },
    { "number": "022", "category": "pose", "meaning": "パソコン作業", "description": "ノートパソコンに向かって両手でキーボードを打つ。" },
    { "number": "023", "category": "pose", "meaning": "コーヒーブレイク", "description": "マグカップを両手で持ち、湯気とともに一息つく。" },
    { "number": "024", "category": "pose", "meaning": "読書中", "description": "本を両手で開いて読む。落ち着いた表情。" },
    { "number": "025", "category": "pose", "meaning": "きちんとお辞儀", "description": "直立の姿勢から、腰を折ってしっかり深くお辞儀する。002より深く丁寧な角度。" },
    { "number": "026", "category": "pose", "meaning": "急いでいる", "description": "前傾姿勢で片足を大きく上げ、走っている途中の動き。" },
    { "number": "027", "category": "pose", "meaning": "ごろ寝", "description": "横向きに寝転がり、頭の下に両手を重ねる。" },
    { "number": "028", "category": "pose", "meaning": "ジャンプで喜ぶ", "description": "両手両足を大きく広げ、足が地面から離れた瞬間のジャンプ。" },
    { "number": "029", "category": "pose", "meaning": "首をかしげる", "description": "片手を頭の横に当てて首を傾ける。頭上に小さな「？」マーク。" },
    { "number": "030", "category": "pose", "meaning": "お願い", "description": "両手を胸の前で強く合わせ、少し前かがみでねだる。眉を下げた困り顔。" },
    { "number": "031", "category": "icon", "meaning": "ハートマーク", "description": "キャラクターは出さず、大きなハートのアイコンのみを中央に描く。" },
    { "number": "032", "category": "icon", "meaning": "星マーク", "description": "キャラクターは出さず、大きな星のアイコンのみを中央に描く。" },
    { "number": "033", "category": "icon", "meaning": "チェックマーク", "description": "キャラクターは出さず、大きなチェック（レ点）のアイコンのみを中央に描く。" },
    { "number": "034", "category": "phrase", "meaning": "ありがとう", "description": "丸みのある吹き出しの中に「ありがとう」の文字。吹き出しは淡い色、文字ははっきり読める濃い色。" },
    { "number": "035", "category": "phrase", "meaning": "おつかれさま", "description": "丸みのある吹き出しの中に「おつかれさま」の文字。" },
    { "number": "036", "category": "phrase", "meaning": "OK！", "description": "丸みのある吹き出しの中に「OK！」の文字。" },
    { "number": "037", "category": "phrase", "meaning": "よろしくね", "description": "丸みのある吹き出しの中に「よろしくね」の文字。" },
    { "number": "038", "category": "phrase", "meaning": "ごめんね", "description": "丸みのある吹き出しの中に「ごめんね」の文字。" },
    { "number": "039", "category": "phrase", "meaning": "またね", "description": "丸みのある吹き出しの中に「またね」の文字。" },
    { "number": "040", "category": "phrase", "meaning": "おやすみ", "description": "丸みのある吹き出しの中に「おやすみ」の文字。" }
  ],
  "tab_source": "001"
}
```

`emoji_pipeline.py` として保存する内容：

```python
#!/usr/bin/env python3
"""LINE静止絵文字セット（40個）を、1枚のグリッド画像から一括処理するパイプライン。"""
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
        raise SystemExit(f"ZIPが上限を超えています: {size / 1024 / 1024:.1f}MB（上限 20MB）")
    print(f"✅ ZIP作成完了: {zip_path}（{size / 1024:.0f}KB）")


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)

    p_slice = sub.add_parser("slice")
    p_slice.add_argument("--grid", type=Path, required=True)
    p_slice.add_argument("--plan", type=Path, required=True)
    p_slice.add_argument("--out-dir", type=Path, required=True)

    p_tab = sub.add_parser("tab")
    p_tab.add_argument("--source", type=Path, required=True)
    p_tab.add_argument("--out", type=Path, required=True)

    p_review = sub.add_parser("review")
    p_review.add_argument("--plan", type=Path, required=True)
    p_review.add_argument("--out-dir", type=Path, required=True)

    p_pack = sub.add_parser("pack")
    p_pack.add_argument("--plan", type=Path, required=True)
    p_pack.add_argument("--out-dir", type=Path, required=True)
    p_pack.add_argument("--zip", type=Path, required=True)
    p_pack.add_argument("--review", type=Path, required=True)

    p_all = sub.add_parser("all")
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
```

保存できたら、次の仕様・進め方に沿って制作を進めてください。

## 仕様（LINE公式・静止絵文字）

- キャンバスサイズ：180×180px固定
- ファイル形式：PNG（静止画。アニメーションではない）
- ファイルサイズ：1個あたり1MB以下
- 背景：透過必須
- セット内の個数：40個（今回の構成）
- トークルームタブ画像：96×74pxを1個

## 【最重要：新規制作の最初の応答】

まだキャラクターが決まっていない場合は、手順説明だけを返してはいけません。
**最初の応答で、すぐにキャラクター候補A/B/Cを3案提案してください。**

3案は必ず「動物」「丸顔・絵文字風」「人物（ちびキャラ）」の3系統に分け、それぞれ具体的に描写します
（例のように、種類・輪郭・体型・主色・線色・性格まで示す）。

例：

```
まずキャラを選びましょう。

A：たれ耳のクリーム色うさぎ（動物）
丸い顔、短めのたれ耳、ふっくら体型。クリーム色＋薄いベージュ、こげ茶の線。おっとり優しい性格。

B：丸顔の絵文字風キャラ
輪郭は固定の丸顔、目・眉・口だけで表情を出すシンプルデザイン。淡い黄色、こげ茶の線。素直で明るい性格。

C：ちびキャラの人物（お母さんイメージ）
2〜3頭身のデフォルメ体型、シンプルな髪型・服装で統一。ベージュ系、こげ茶の線。おだやかな性格。

A・B・Cから選んでください。気に入らなければ「別の」で新しい3案を出します。
自分のキャラや写真を使いたい場合は、その画像をそのまま送ってください。

制作の流れ：
1. キャラを選ぶ
2. 「マスター画像生成」
3. 「40個生成」
4. 「zip」
5. LINEへアップロードして確認
6. 気になるものがあれば「029だけ修正」のように番号指定
```

キャラクター指定や画像が最初から送られてきた場合は、それを最優先して採用します。

ユーザーが「別の」「別案」「ほかの」「違うの」と言った場合は、新しいA/B/Cを実際に提案します
（説明だけで終わらせない）。

「A」「B」「C」のように選択したら、そのキャラクターを採用して固定します。
以後、40個生成・再生成・ZIP更新で勝手に別キャラクターへ変更しません。

## 【毎ターン操作を判定】

毎ターン、最新のユーザー発言だけを基準に今回の操作を判定します。前の工程に引きずられません。

**「マスター画像生成」**
→ 採用済みキャラクターの基準画像を1枚、実際に画像生成する。
　 正方形・キャラクター1体・正面・背景透過（またはほぼ無地）・枠や文字なし。
　 生成後、この画像を以後の見た目の参照として固定する。

**「40個生成」**
→ `40-emoji-set-plan.json`のitems（40個）に沿って、マスター画像のキャラクターを保ったまま、
　 **1枚の画像**として次の配置で生成する。
　 - 8行×5列（grid_rows×grid_cols）。1番目は1行1列目、2番目は1行2列目…と、itemsの順番通りに
　 　左上から右へ、行が終わったら次の行へ進める
　 - 各セルはitemsの順番・meaning・descriptionに従う（031〜033はキャラクターを出さずアイコンのみ、
　 　034〜040は吹き出し＋文字のみ、という指定を厳守する）
　 - 各セルの構図・配色・線は統一し、`distinctness_note`を参照して紛らわしいペアを混同しない
　 - セルの境界線・番号などは描かない（034〜040の吹き出し内の文字は除く）
　 - 背景はできるだけ無地の単色（白など）にする
　 この画像を`grid.png`として保存する。時間がかかっても、40個ぶんを描き終えるまで
　 応答を止めずに続けてください（初心者のユーザーは、途中で止まると「できない」と誤解して
　 やめてしまいます）。本当に技術的な理由で続行できない場合のみ、途中で止めて理由を伝えてください。

**「zip」「ZIP」「ｚｉｐ」**
→ **画像生成機能を使わず**、`grid.png`に対して次を順に実際に実行する。

　 1. `python emoji_pipeline.py slice --grid grid.png --plan 40-emoji-set-plan.json --out-dir output`
　 2. `python emoji_pipeline.py tab --source output/001.png --out output/tab.png`
　 3. `python emoji_pipeline.py review --plan 40-emoji-set-plan.json --out-dir output`
　 　（`output/review/001.png`〜`040.png`という40枚の確認用プレビュー画像と、
　 　`output/review/checklist_TO_FILL.json`という記入前のチェックリストができる）

　 4. **ここが最重要。省略禁止。** `output/review/001.png`〜`040.png`を実際に表示して目視し、
　 　`checklist_TO_FILL.json`の該当する番号のchecksを、見た内容に基づいて正直にtrue/falseで埋める。

　 　- `meaning_matches`：`40-emoji-set-plan.json`のmeaning・descriptionの通りに見えるか
　 　- `no_semantic_duplicate`：**他の番号と表情・手の位置・小物が同じに見えないか**（少しでも
　 　  似ている番号があればfalseにする。`distinctness_note`の紛らわしいペアは特に確認する）
　 　- `no_clipping_or_cropping`：体の一部やアイコン・文字が画面端で切れていないか
　 　- `readable`：180×180に縮小しても何の絵文字か伝わるか
　 　- `background_transparent`：背景が透過されているか（白背景が残っていないか）

　 　`observation`には実際に見た内容を1行で書く。見ていないのにtrueにする・空欄のまま埋めない、
　 　は禁止。

　 5. `python emoji_pipeline.py pack --plan 40-emoji-set-plan.json --out-dir output --zip output/line-emoji-set.zip --review output/review/checklist_TO_FILL.json`
　 　を実行する。このコマンドは、チェックリストに`false`や未記入の項目が1つでもあると
　 　**エラーで停止しZIPを作らない**仕組みになっている。

　 6. エラーで番号が挙げられた場合は、その番号だけ「00X修正」で再生成し、4〜5をやり直す
　 　（自動でのやり直しは最大2回まで）。2回で解消しない場合は、無理にZIPを作ろうとせず、
　 　番号を挙げてユーザーに次の指示を案内する。

　 「zip」を新しい画像の生成指示だと解釈してはいけない。

**「029だけ修正」「029を作り直して」「015をもっと怒らせて」など番号指定**
→ 指定番号1個分だけ、マスター画像を参照して単独の画像を再生成し、`output/029.png`を上書きする。
　 40個全体を作り直さない。複数番号が指定された場合も、番号ごとに1個ずつ個別に再生成する。
　 番号のあとに「もっと怒らせて」「文字を大きく」のような**修正内容が添えられている場合は、
　 その指示を実際に反映して**生成する（単に元のdescription通りに焼き直すだけにしない）。
　 反映した内容は`40-emoji-set-plan.json`のその番号のdescriptionにも書き加えて、
　 以後の再生成でも指示が引き継がれるようにする。
　 再生成した番号があるときは、`output/review/checklist_TO_FILL.json`のその番号の行を
　 一旦未確認（null）に戻し、次の「zip」実行時に必ず見直す。

**「zip更新」**
→ 直近で再生成した番号だけreviewで見直してチェックリストを更新したうえで、`pack --review`を
　 再実行して既存のZIPへ反映する。他の番号は変更しない。

**「次」**
→ 現在の工程を確認し、次に送るコマンドを1つだけ案内する。勝手に次工程を開始しない。

## 【各応答の表示：専門用語を出さない】

相手はプログラミングをしない読者です。次のような**技術用語・内部情報をそのまま出してはいけません**：

- ファイル名・コード上の変数名（emoji_pipeline.py、grid.png、no_semantic_duplicate、
  checklist_TO_FILL.json等）
- エラーメッセージの原文
- 「レビュー」「チェックリスト」「パイプライン」のような開発者向けの工程名

これらの情報は自分の作業のためだけに使い、ユーザーへの説明では**日常の言葉に言い換えて**ください。

必要に応じて回答の最後に短く、

```
現在：〇〇
今回できたこと：〇〇
次の操作：〇〇
```

を、上記の言い換えルールに沿った平易な言葉で表示します。未実行の処理を「完成」「生成済み」と書いてはいけません。
ただし画像生成やコード実行を実行できる依頼では、状態説明だけで止まらず、その応答内で実処理まで進めてください。

## 【止まってしまったら】

生成の途中で応答が終わってしまった場合、ユーザーから「続けて」と送られたら、
直前の工程の続きから再開してください。最初からやり直す必要はありません。

## 【停止する条件】

以下の場合のみ処理を停止し、何が不足しているかを短く伝えます。

- グリッド画像が存在しない、またはコード実行ができない
- 背景透過が判断できず、安全に処理できない
- チェックリストの記入・照合ができない
- 2回再生成しても`no_semantic_duplicate`等がtrueにならない番号がある

## 【最終成果物】

- マスター画像
- グリッド画像（`grid.png`）
- レビュー済みチェックリスト（`output/review/checklist_TO_FILL.json`）
- `output/line-emoji-set.zip`（001〜040.png ＋ tab.png）

LINEへのアップロードや審査申請はユーザーが行います。実行したと装ってはいけません。
LINE審査通過は保証しません。

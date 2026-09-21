# Codexへの指示文（1メッセージで送ります）

## 準備

1. [公式サイト](https://chatgpt.com/ja-JP/download/)からCodexを入手し、起動する
2. `motif-animal.md` / `motif-round-face.md` / `motif-person.md` のうち、
   使いたいモチーフを1つ選ぶ（手持ちの画像がある場合は、下のメッセージと一緒にその画像を添付する）

## この指示文を送る

下のメッセージの先頭に、選んだモチーフのファイルの中身をそのまま貼り付けてから、
全体を1つのメッセージとしてCodexに送ってください
（画像を使う場合は、モチーフの貼り付けは不要です。メッセージと一緒に画像を添付してください）。

```
（ここに選んだモチーフの内容を貼り付ける）

あなたはこれから、LINE Creators Marketに出品できる「動くLINE絵文字（アニメーションスタンプ）」の
制作を手伝います。上で伝えたキャラクターの見た目（または添付した画像のキャラクター）を保ったまま、
以下の手順を順番に実行してください。
```

## 表情セット

- 表情セット（5枚以上20枚以内で選ぶ。迷ったら次の5つでOK）：
  1. 通常の笑顔
  2. 大笑い
  3. 驚き
  4. 困り顔
  5. 照れ

## 手順

1. `frames/` フォルダを作り、上記モチーフ・表情セットに沿った表情差分を
   1フレーム=1枚のPNG画像として `001.png`, `002.png`... の連番で生成・保存する。
   - キャンバスサイズは320×270px以内、かつ長辺270px以上にする
   - 背景は必ず透過（アルファチャンネルあり）にする
   - 全フレームでキャラクターの輪郭・配色・サイズ・構図を統一する（表情パーツ以外は動かさない）
2. （文字を入れたい場合のみ）このキットに同梱の `scripts/add_text_overlay.py` を実行し、
   `frames/` の画像に短いセリフ（例:「了解！」「OK」）を合成する。

   ```
   pip install -r scripts/requirements.txt
   python scripts/add_text_overlay.py --frames-dir frames --output-dir frames_with_text \
     --text "ここにセリフ" --font <お使いの日本語フォントファイルのパス> --font-size 36
   ```

   日本語フォントが手元にない場合は、Google FontsでNoto Sans JPなど商用利用可のフォントを
   ダウンロードしてから指定してください。
3. このキットに同梱の `scripts/build_apng.py` を実行し、フレームをAPNGに自動合成する。

   ```
   python scripts/build_apng.py --frames-dir frames --output output.png \
     --duration-ms 200 --loop 2
   ```

   （文字入れをした場合は `--frames-dir frames_with_text` を指定する）
4. `build_apng.py` はLINEの仕様（キャンバスサイズ・フレーム数・ループ回数・再生時間・
   ファイルサイズ300KB以内）を自動チェックします。エラーが出た場合は指示された箇所
   （フレーム数・duration・サイズなど）を調整して2〜3をやり直してください。
5. 最終的に `output.png`（中身はAPNG形式）が仕様を満たしていれば完成です。
   LINE Creators Marketへの申請方法はページの「LINEへの申請方法」セクションを参照してください。

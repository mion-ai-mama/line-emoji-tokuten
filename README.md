# 動くLINE絵文字の作り方 完全ガイド

Instagramリール特典として配布する、スマホ対応の1ページ完結ガイドです。
HTML / CSS / JavaScript だけで作られた静的サイトで、ビルド作業は必要ありません。

---

## 0. 公開先

- 公開ページ: <https://mion-ai-mama.github.io/line-emoji-tokuten/>
- リポジトリ: <https://github.com/mion-ai-mama/line-emoji-tokuten>（Public）

## 1. プロジェクト概要

| 項目 | 内容 |
|---|---|
| ページタイトル | 動くLINE絵文字の作り方 完全ガイド |
| サブタイトル | 自分の絵がなくても大丈夫（Codex・ChatGPT対応） |
| 想定読者 | AI初心者・副業志向・「絵が描けない」不安がある層（スマートフォン閲覧が中心） |
| 目的 | LINE公式仕様に沿った「動くLINE絵文字（アニメーションスタンプ）」を、Codex／ChatGPTどちらでも作れるように案内する |
| 技術 | HTML5 / CSS3 / Vanilla JavaScript（外部フレームワーク不使用） |
| 公開 | GitHub Pages（静的ファイルの配信のみ） |

ページに含まれる主な機能は次のとおりです。

- ページ内目次から各セクションへ移動できる
- Codexルート／ChatGPTルートそれぞれに、8個セットを会話駆動で一括生成するマスタープロンプトがある
  （キャラクターはページ上で選ばず、プロンプトを送った後にAIが候補A/B/Cを提案する）
- 「うまくいかないとき」はアコーディオン形式
- 配布キット（構成JSON＋Pythonパイプライン＋マスタープロンプト一式）をZIPでダウンロードできる

---

## 2. ファイル構成

```text
/
├── index.html      ページ本体（文章もここに入っています）
├── style.css       配色・レイアウト
├── script.js       コピー機能 / アコーディオン / スクロール演出
├── README.md       このファイル
├── docs/
│   ├── requirements.md      要件定義
│   └── SCOPE_PROGRESS.md    進捗管理
└── assets/
    ├── favicon/favicon.svg
    ├── images/cta-banner.png   「AIマネタイズの教科書」バナー（既存ポリシー通り固定）
    └── kit/                    配布キット本体（§6参照）
        ├── line-emoji-kit.zip  ダウンロードボタンからリンクしているZIP（要再生成、§6）
        ├── prompts/            8-emoji-set-plan.json／Codex用・ChatGPT用マスタープロンプト
        └── scripts/            emoji_pipeline.py（グリッド切り出し→APNG合成→ZIP作成）
                                 build_apng.py（emoji_pipeline.pyが内部利用）
                                 add_text_overlay.py（任意の文字入れ用。今回のセットでは未使用）
```

---

## 3. ローカルでの確認方法

いちばん簡単な方法は、`index.html` をダブルクリックしてブラウザで開くことです。
これだけでも表示とコピー機能を確認できます。

本番に近い状態で確認したい場合は、簡易サーバーを使います。

```bash
cd line-emoji-tokuten
python3 -m http.server 8000
```

ブラウザで <http://localhost:8000> を開きます。
終了するときはターミナルで `Ctrl` + `C` を押します。

> サーバーは1つだけ起動してください。ポートが使用中と表示された場合は、
> `8000` の部分を `8001` などに変えます。

---

## 4. GitHub Pagesでの公開方法

1. GitHubで新しいリポジトリ（`line-emoji-tokuten`）を作成し、このフォルダの中身をすべてアップロードします。
2. リポジトリの **Settings** → **Pages** を開きます。
3. **Source** で「Deploy from a branch」を選びます。
4. **Branch** で `main`、フォルダは `/ (root)` を選び、**Save** を押します。
5. 数分待つと `https://mion-ai-mama.github.io/line-emoji-tokuten/` で公開されます。

`index.html` の `og:url` は上記URLで設定済みです。
公開先のリポジトリ名を変えた場合のみ、次の1か所を実際のURLに書き換えてください。

```html
<meta property="og:url" content="https://mion-ai-mama.github.io/line-emoji-tokuten/">
```

---

## 5. 画像の差し替え方法

`assets/images/` に画像を置き、`index.html` 内の該当する `src="assets/images/○○"` を
書き換えます（このページは画像未配置時の自動プレースホルダーを実装していないため、
画像を追加する場合はHTML側の`<img>`タグも合わせて追記してください）。

- `<img>` に `width` / `height` 属性は付けないでください。
  CSS側で `aspect-ratio` + `object-fit: contain` を使う運用です
  （Instagramアプリ内ブラウザで縦に歪む不具合の対策。詳細は`CLAUDE.md`参照）。
- 「できること」セクションの完成イメージ画像は、本ガイド作成時点ではまだ未配置です
  （`docs/SCOPE_PROGRESS.md`の残作業を参照）。

---

## 6. 配布キット（`assets/kit/`）の中身と更新方法

このページ固有の成果物として、8個セットを会話駆動で一括生成するための
構成JSON・Pythonパイプライン・マスタープロンプトを1つのZIPにまとめて配布しています。

| ファイル | 役割 |
|---|---|
| `prompts/8-emoji-set-plan.json` | 8個セットの構成の正本（番号・意味・フレーム数・動きの説明） |
| `prompts/codex-emoji-set-prompt.md` | Codexへの指示文（`index.html`の「Codexで作る」と同内容） |
| `prompts/chatgpt-emoji-set-prompt.md` | ChatGPTへの指示文（`index.html`の「ChatGPTだけで作る」と同内容） |
| `scripts/emoji_pipeline.py` | グリッド画像の切り出し・中央配置・背景透過・APNG合成・タブ画像作成・ZIP作成を一括実行 |
| `scripts/build_apng.py` | `emoji_pipeline.py`が内部で使うAPNG合成＋LINE仕様バリデーション |
| `scripts/add_text_overlay.py` | Pillowでフレームに文字を合成する任意ツール（今回の8個セットでは未使用。文字入れをしたい場合に利用） |

**`prompts/`配下の内容を変更した場合は、`index.html`内の対応箇所（マスタープロンプトの`<pre>`）も
忘れずに書き換えてください**（キットとページ本文は別ファイルとして重複管理しているため、
片方だけ更新すると内容がズレます）。

> 配布ZIPは、上表のファイルを**フォルダ分けせず1階層に展開**する構成にしています
> （`-j`でサブフォルダを潰して固める。読者が解凍したときに`prompts/`・`scripts/`の
> 2フォルダに分かれて見え、「3ファイルを添付」の案内と噛み合わなくなる問題があったため）。

内容を更新したら、ZIPを作り直してダウンロードボタンに反映させます。

```bash
cd assets/kit
rm -rf scripts/__pycache__
rm -f line-emoji-kit.zip
zip -j line-emoji-kit.zip prompts/*.json prompts/*.md scripts/*.py scripts/*.txt
```

---

## 7. OGP画像について

このページは、公開時点でOGP画像（`og:image`）をあえて設定していません
（配布ポリシー上のデフォルト。必要になった場合はチームの判断で追加します）。

追加する場合は、1200×630px程度の画像を`assets/images/`に置き、`index.html`の
`<head>`内に`og:image`（絶対URL）と`twitter:card`（`summary_large_image`）を追記してください。

---

## 8. 掲載情報の日付

- 掲載情報の基準日：`docs/requirements.md`の作成日（2026年9月21日）
- LINE Creators Marketの仕様（キャンバスサイズ・フレーム数など）は変更される可能性があるため、
  更新した場合は`index.html`の「LINEへの申請方法」セクションと`docs/requirements.md`§2.1の
  両方を合わせて更新してください。

---

## 9. 更新時に確認すべき公式情報

LINE Creators Marketの出品仕様・審査基準は変更されることがあります。
更新前に、LINE Creators Market公式サイトで最新のアニメーションスタンプ制作ガイドラインを
検索して確認してください（本READMEには変更されやすい外部URLを直接記載していません）。

---

## 10. スマートフォン表示の確認方法

**パソコンで確認する場合**

1. Chromeでページを開きます。
2. `F12`（Macは `option` + `command` + `I`）で開発者ツールを開きます。
3. 左上のスマートフォンのアイコンを押し、機種を `iPhone SE` などに切り替えます。
4. 横方向にスクロールしないこと、文字や画像がはみ出していないことを確認します。

**実機で確認する場合**

パソコンとスマートフォンを同じWi-Fiにつなぎ、パソコンで簡易サーバーを起動して、
スマートフォンから `http://<パソコンのIPアドレス>:8000` を開きます。

確認するポイント：

- 横スクロールが起きない
- 「この指示文をコピーする」を押すと「コピーしました」と表示される
- 目次から各セクションへ移動できる
- キットZIPのダウンロードボタンが正常に動作する
- アコーディオン（うまくいかないとき）が開閉する

---

## 11. 注意

- このページ・配布キットは情報提供を目的としたもので、生成物の著作権や
  LINE Creators Marketの審査結果を保証するものではありません。
- 配布キット（プロンプト・スクリプト）はオリジナルの新規作成物です。競合LPの文章・
  ファイルはそのまま流用していません。

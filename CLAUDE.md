# 動くLINE絵文字の作り方 完全ガイド（Instagramリール特典ページ）

> 設計の共通原則（基本原則・資産価値の原則・自律解決の原則）は `~/.claude/CLAUDE.md` に従う。

## プロジェクト設定

技術スタック:
  frontend: HTML5 / CSS3 / Vanilla JavaScript（ビルド工程なし・フレームワーク不使用）
  backend: なし
  database: なし
  hosting: GitHub Pages（静的ファイル配信のみ）

ビルド・サーバーが不要な完全な静的サイト。`index.html` を直接開く、または
`python3 -m http.server` で確認する。ポートのランダム生成・バックエンドポートの割り当ては不要。

## 環境変数

このプロジェクトは環境変数を使用しない（APIキー・DB接続情報が一切不要な静的サイトのため）。
`.env` 系ファイルは作成しない。

## ファイル構成の原則

フラット構成を維持する（テンプレート元リポジトリの `css/` `js/` 分割・`LICENSE.md`・`.github/` は
このプロジェクトでは使わないため削除済み）。

```text
index.html / style.css / script.js / README.md / assets/
```

- **文章の単一の源は `index.html`**。`content.js` 方式は使わない。文言を変えるときは `index.html` を直接編集する。
- 画像は `assets/` に**同名ファイル**を置くだけで反映される。HTMLの書き換えは不要。
- 配布キット本体（ZIP）は `assets/kit/` に置き、ダウンロードボタンから直接リンクする。

## このプロジェクト固有の成果物：配布キット

ページ本体とは別に、**読者がダウンロードして使う「オリジナルのCodex/ChatGPT用プロンプトキット」**を
新規に作成する（競合ファイルの転載は禁止。詳細は `docs/requirements.md` §2 を参照）。

- **2ルート構成**: Codexルート（プロンプト＋Pillow文字合成＋APNG自動合成スクリプト一式）／
  ChatGPTのみルート（連番静止画生成プロンプト＋無料結合ツール案内）
- **LINE公式仕様の厳守**: APNG・320×270px以内・5〜20フレーム・ループ1〜4回・4秒以内・300KB以下
  （`docs/requirements.md` §2.1）
- **モチーフ選択**: 手持ち画像の添付を基本とし、ない読者には「動物／丸顔／人物」から選ばせる。
  人物モチーフは表情差分でブレやすいため、プロンプトに「シンプル・ちびキャラ風」等の一貫性維持の指示を必ず入れる

## 命名規則

- ファイル: kebab-case（例: `emoji-sample-01.webp`）
- JavaScript変数・関数: camelCase / CSSクラス: BEM風（`.block__element--modifier`）

## 配色（変更しないこと。変える場合はユーザー確認）

| 用途 | 変数 | 値 |
|---|---|---|
| 背景 | `--color-bg` | `#fdfaf7` |
| 淡いブラッシュピンク | `--color-bg-soft` | `#fbeeec` |
| メインピンク（くすみローズ） | `--color-primary` | `#cf8a92` |
| 濃いピンク | `--color-primary-dark` | `#b16d76` |
| アクセント淡ピンク | `--color-accent-light` | `#f7dfe0` |
| メイン文字（濃茶） | `--color-text` | `#3d322f` |
| 補助文字 | `--color-text-muted` | `#8a7972` |
| ボーダー | `--color-border` | `#f0dfdc` |

大人ピンク×アイボリー系。40代女性が見ても幼く感じない、大人っぽいトーンを保つ。

## コード品質

- 関数: 100行以下 / ファイル: 700行以下 / 複雑度: 10以下 / 行長: 120文字
- 700行基準は `style.css` / `script.js` に適用する。`index.html` は掲載文章そのもの
  （プロンプト全文を含む）を保持するため対象外とし、分割しない（単一性を優先）。

## 表示確認（納品前に必須）

Playwrightで実ビューポートを再現して確認する。
claude-in-chrome拡張の `resize_window` はOSウィンドウのみでCSSビューポート幅が変わらず、
モバイル幅の検証には使えない。

確認項目: 横スクロールが起きない（320 / 375 / 1280px）／JSエラーなし／
コピーボタンで「コピーしました！」が出る／目次から各セクションへ移動できる／
キットZIPのダウンロードボタンが正常に動作する／画像未配置でもレイアウトが崩れない。

## 画像の扱い

- `<img>` に `width` / `height` 属性を付けない。
  CSS側で `aspect-ratio` + `object-fit: contain` + `height: auto` を使う
  （Instagramアプリ内ブラウザで縦に歪む不具合の対策）。
- 縦横比は `style="--ar: 4 / 5;"` のようにインライン変数で指定する。

## 配布導線（このページが前提とする流れ）

LINE登録トリガーの自動配信ではない。実際の導線は
「リールにコメント → DM → オープンチャット誘導 → オプチャ内の特典まとめからこのページのリンクを受け取る」。
このページ自体は誰でもURLを知れば閲覧・DLできる公開静的ページとして作る
（ページ内にLINE登録を必須にするゲートは設けない）。

## ドキュメント管理

許可されたドキュメントのみ作成可能:
- `README.md`（ページの使い方・公開手順）
- `docs/requirements.md`（要件定義）
- `docs/SCOPE_PROGRESS.md`（進捗管理）

上記以外のドキュメント作成はユーザー許諾が必要。実装済みの記載は積極的に削除する。

## 公開

- GitHub Pages（`main` ブランチ / `/ (root)`）
- 公開後、`index.html` の `og:image` と `og:url` を実際の公開URLに書き換える
- リポジトリ: https://github.com/mion-ai-mama/line-emoji-tokuten
- 親ディレクトリ `instagram-tokuten-template` とは別リポジトリとして扱う
  （親の `.gitignore` に `line-emoji-tokuten/` を登録済み）

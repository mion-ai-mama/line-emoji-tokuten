# 開発進捗：動くLINE絵文字の作り方 完全ガイド

## アーキ構成

- 確定アーキ: #6 WEBアプリ（決定論）の最小形＝静的1ページサイト
- 操作者: ブラウザのエンドユーザー
- AI本体(プロンプトY): なし ／ MCP: なし ／ 自社DB: なし
- フロントUI: あり ／ 動的変数: なし
- 種別: Web型 ／ 配布: GitHub Pages で公開（[[tokuten-distribution-flow]]の導線で特典まとめから案内）

詳細は `docs/requirements.md` を参照。

## 実装計画

### 開発フェーズ

| Phase | 名称 | 担当 | 状態 |
|-------|------|------|------|
| 1 | 要件定義 | Agent 1 | [x] |
| 2 | Git管理 | Agent 2 | [x] mion-ai-mama/line-emoji-tokuten（Public）・developブランチ作成済み |
| 3 | フロントエンド基盤 | Agent 3 | スキップ（ビルド不要の静的サイト） |
| 4 | ページ実装 | Agent 4 | [x] index.html/style.css/script.js 全面書き換え済み（320/375/1280px・JSエラー0件をPlaywrightで確認済み） |
| 5 | 環境構築 | Agent 5 | スキップ（環境変数・依存パッケージなし） |
| 6 | バックエンド計画 | Agent 6 | スキップ（バックエンドなし） |
| 7 | エージェント構築 | Agent 7 | スキップ（AI本体なし） |
| 8 | バックエンド実装 | Agent 8 | スキップ（バックエンドなし） |
| 9 | フロントエンド実装(API統合) | Agent 9 | スキップ（API連携なし） |
| 10 | E2Eテスト | Agent 10 | [ ] |
| 11 | ローカル動作確認 | Agent 11 | [ ] |
| 12 | デプロイ | Agent 12 | [x] GitHub Pages公開済み（main / root）。https://mion-ai-mama.github.io/line-emoji-tokuten/ で200・横スクロール0件・JSエラー0件をPlaywrightで確認済み |

## ページ管理表

> 2026-09-22追記: ルート構成を3つ（Codex／ChatGPTだけの人＝ファイル添付版／パソコンがない人＝
> ファイル添付不要版）→**2つ**（Codex／ChatGPTだけの人＝ファイル添付不要版）に統合した。
> ファイル添付不要版はパソコンでもスマホでも使え、ファイル添付版より手間が少ないため、
> ファイル添付版を残す理由がないと判断（ユーザー指摘）。`#chatgpt`セクションは削除し、
> 旧`#smartphone`のURLをそのまま「ChatGPTだけの人」ルートとして使う。

| ID | セクション | 状態 |
|----|-----------|------|
| P-001 | ファーストビュー | [x] |
| P-002 | 目次 | [x] |
| P-003 | できること | [x] |
| P-004 | 準備するもの（Codex＝動く絵文字/ChatGPT＝静止絵文字の分岐・40個セット内容一覧） | [x] |
| P-005 | Codexルート（動く絵文字。Codex入手ボタン＋パソコン必須の注記＋手順＋マスタープロンプト＋キットDLボタン3ファイル） | [x] |
| P-006 | ChatGPTだけの人ルート（静止絵文字。=旧「パソコンがない人はこちら」。ファイル添付不要・プロンプト1つに全内容を埋め込み。パソコン・スマホ両対応） | [x] |
| P-006.6 | 40個そろったら（申請前の目視チェック手順・番号＋修正内容を指定する使い方の案内） | [x] |
| P-007 | LINEへの申請方法 | [x] |
| P-008 | うまくいかないとき（アコーディオン） | [x] |
| P-009 | ご案内（AIマネタイズの教科書。オープンチャット誘導はなし＝この特典自体がオープンチャット経由配布のため） | [x] |
| P-010 | 参考情報・免責事項 | [x] |

## 配布キット管理表（このプロジェクト固有の成果物）

> 2026-09-21改訂: 「1個だけ手作業で作る」設計から「8個セットを会話駆動で一括生成する」設計に刷新。
> K-001〜K-003（単品用プロンプト・モチーフ別ファイル）は役目を終えたため削除し、K-004〜K-006に置き換えた。
>
> 2026-09-22改訂（大）: 「動く絵文字8個（APNG）」を実機検証したところ、8個を1枚で同時生成すると
> ポーズが混同する／1個ずつの個別生成に変えても直前の生成を引きずる、という不具合が
> 指示文の工夫では解消しなかった（詳細は`docs/requirements.md` §2.2）。競合と同じ
> **静止画40個セット**に方式を全面転換し、K-004〜K-006を作り直した。`build_apng.py`は
> 不要になり削除。旧`8-emoji-set-plan.json`は`40-emoji-set-plan.json`として作り直し。
>
> 2026-09-22改訂（大・2回目）: 競合の実際のLPを確認したところ、競合のメインルート（Codex）は
> 動く絵文字（APNG）であり、静止画はChatGPT向けの副次ルートに過ぎないと判明
> （`docs/requirements.md` §2.2の追記参照）。**Codexルートを動く絵文字40個に作り直した**。
> `build_apng.py`をPillow単体版として復元し、`emoji_pipeline_animated.py`（1個ずつ個別生成＋
> APNG合成＋レビュー＋ZIP作成）を新設。ChatGPTルートは静止絵文字のまま維持。
> 旧`core-files.zip`（ChatGPT用2ファイル・もう使われていない）を廃止し、`codex-kit.zip`
> （Codex用3ファイル）を新設した。旧`chatgpt-emoji-set-prompt.md`（ファイル添付版・未使用）は削除。

| ID | 内容 | 状態 |
|----|------|------|
| K-004 | 40個セットの構成・静止画版（正本JSON。番号・意味・説明。表情20／生活シーン10／単独アイコン3／ふきだし文字7） | [x] `assets/kit/prompts/40-emoji-set-plan.json`（ChatGPT用） |
| K-004b | 40個セットの構成・動く絵文字版（正本JSON。番号・意味・動き・10フレーム・1秒ループ×3回） | [x] `assets/kit/prompts/40-emoji-animated-plan.json`（Codex用） |
| K-005 | グリッド画像一括処理パイプライン（切り出し・中央配置・背景透過・レビュー・ZIP作成） | [x] `assets/kit/scripts/emoji_pipeline.py`（ChatGPT用・静止画） |
| K-005b | 1個ずつ個別生成パイプライン（帯画像切り出し・APNG合成・レビュー・ZIP作成） | [x] `assets/kit/scripts/emoji_pipeline_animated.py` + `build_apng.py`（Codex用・動く絵文字。Pillow単体・外部パッケージ不要） |
| K-006 | Codex用マスタープロンプト（キャラ候補A/B/C提案＋会話コマンド駆動＋目口の絶対条件＋整数秒ループ厳守） | [x] `assets/kit/prompts/codex-emoji-set-prompt.md` |
| K-007 | ChatGPTだけの人用マスタープロンプト（40-emoji-set-plan.json・emoji_pipeline.pyの中身を埋め込み、ファイル添付を不要にしたもの） | [x] `assets/kit/prompts/chatgpt-smartphone-prompt.md` |

> 2026-09-21追記: 配布ZIPを`prompts/`・`scripts/`のフォルダ分け構成から**フラット構成**に変更。
> ユーザーが実機で解凍したところ2フォルダに分かれて見え、ページの「3ファイルを添付」という
> 案内と食い違っていたため（実証性：ユーザー報告で発覚）。README.md §6のzipコマンドも
> `zip -j`に更新済み。
>
> 2026-09-22追記: フラット化しても「7ファイル中どの3つか分かりにくい」とのフィードバックが
> 再度あったため、**必須ファイルのみの`core-files.zip`**を新設してメインのダウンロードボタンに
> し、完全版`line-emoji-kit.zip`はサブリンク（任意）に格下げした（静止画方式への刷新で
> 必須ファイルは2つに減少）。

いずれも競合ファイルを一切含まない、完全新規のオリジナル作成物とする。
`emoji_pipeline.py`は合成テスト用グリッド画像（8行×5列・40個）で`all`→チェックリスト記入→
`pack --review`の一連の動作を確認済み（180×180・96×74のPNG出力、41ファイルのZIP作成、
未記入時の拒否動作を含む）。
`emoji_pipeline_animated.py`（+`build_apng.py`）は合成テスト用の帯画像40枚（各10フレーム）で
`slice-items`→`build`→`tab`→`review`→チェックリスト記入→`pack`の一連の動作を確認済み
（APNG生成後に`is_animated=True, n_frames=10, duration=100ms, loop=3`を実際に検証、
未記入時の拒否動作、41ファイルのZIP作成を含む。apngパッケージなしのvenvで実行しエラーなし）。

## 残作業（素材・コンテンツの配置）

- [x] キットZIP本体の圧縮（`assets/kit/line-emoji-kit.zip`。ページの「プロンプトキット一式をダウンロード」ボタンからリンク済み）
- [x] ページ本文（`index.html`）の執筆（40個セット方式への書き換え済み）
- [ ] スクリーンショット・完成例画像の準備（`#about`セクションは現状テキスト＋アイコンのみ。完成イメージ画像は未着手）
- [x] `README.md`のプロジェクト固有情報への更新（`CLAUDE.md`は元から固有内容だったため対象外）
- [x] GitHub Pages公開設定（main / root。https://mion-ai-mama.github.io/line-emoji-tokuten/ で公開確認済み）
- [x] スマホ完結ルート（ファイル添付不要・プロンプト1つで完結）を追加。`40-emoji-set-plan.json`と
  `emoji_pipeline.py`の中身をプロンプト本文に埋め込み、Playwrightなしでもclaude-in-chromeで
  ローカル確認済み（コピー機能・埋め込みJSON/Pythonの構文・no_semantic_duplicate等のcheckが
  正しく動作。`<`/`>`を含むPythonコードをHTMLの`<pre>`にそのまま埋め込んでも破綻しないことを
  実機で確認）
- [x] 「40個そろったら」セクションを追加（申請前に自分の目で見比べる／番号＋修正内容を指定する使い方の案内）
- [x] バグ修正: `#smartphone-prompt-text`にスクロール制限CSS（`max-height`/`overflow-y`）が
  漏れており、埋め込みコード480行分がそのままセクションの高さになって13,377pxに達し、
  スクロール演出（IntersectionObserver, threshold 0.15）が永久に発火しない
  ＝セクション全体が非表示になる不具合が発生していた。`style.css`の該当セレクタに
  `#smartphone-prompt-text`を追加して解消（claude-in-chromeで実機確認済み）
- [x] Codexルートを静止絵文字→動く絵文字（APNG）に作り直し（競合の実LP確認による方針転換。
  `docs/requirements.md` §2.2参照）。40-emoji-animated-plan.json新設、build_apng.py復元
  （Pillow単体）、emoji_pipeline_animated.py新設（1個ずつ個別生成対応）、
  codex-emoji-set-prompt.md全面書き換え（目・口の絶対条件、整数秒ループ厳守、40回ツール呼び出し）。
  index.htmlのCodexセクション・LINEへの申請方法（仕様を2本立てに）・うまくいかないとき
  （動く絵文字特有のFAQ追加）・タイトル/hero/aboutを更新。旧core-files.zipを廃止しcodex-kit.zip
  を新設。旧chatgpt-emoji-set-prompt.md（未使用）を削除

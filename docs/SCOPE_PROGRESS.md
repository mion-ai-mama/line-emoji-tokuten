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

| ID | セクション | 状態 |
|----|-----------|------|
| P-001 | ファーストビュー | [x] |
| P-002 | 目次 | [x] |
| P-003 | できること | [x] |
| P-004 | 準備するもの（Codex/ChatGPT分岐・モチーフ選択） | [x] |
| P-005 | Codexルート（手順＋キットDLボタン） | [x] |
| P-006 | ChatGPTのみルート（手順＋プロンプト＋結合ツール案内） | [x] |
| P-007 | LINEへの申請方法 | [x] |
| P-008 | うまくいかないとき（アコーディオン） | [x] |
| P-009 | ご案内（AIマネタイズの教科書。オープンチャット誘導はなし＝この特典自体がオープンチャット経由配布のため） | [x] |
| P-010 | 参考情報・免責事項 | [x] |

## 配布キット管理表（このプロジェクト固有の成果物）

| ID | 内容 | 状態 |
|----|------|------|
| K-001 | Codex用プロンプトキット一式（表情差分生成＋Pillow文字合成＋APNG自動合成スクリプト） | [x] `assets/kit/prompts/codex-master-prompt.md` + `assets/kit/scripts/{build_apng.py,add_text_overlay.py}` |
| K-002 | ChatGPTのみルート用プロンプト（連番静止画生成） | [x] `assets/kit/prompts/chatgpt-master-prompt.md` |
| K-003 | モチーフ別デフォルト提案の指示文（動物／丸顔／人物・一貫性を保つ指示を含む） | [x] `assets/kit/prompts/motif-{animal,round-face,person}.md` |

いずれも競合ファイルを一切含まない、完全新規のオリジナル作成物とする。

## 残作業（素材・コンテンツの配置）

- [x] キットZIP本体の圧縮（`assets/kit/line-emoji-kit.zip`。ページの「プロンプトキット一式をダウンロード」ボタンからリンク済み）
- [x] ページ本文（`index.html`）の執筆
- [ ] スクリーンショット・完成例画像の準備（`#about`セクションは現状テキスト＋アイコンのみ。完成イメージ画像は未着手）
- [x] `README.md`のプロジェクト固有情報への更新（`CLAUDE.md`は元から固有内容だったため対象外）
- [x] GitHub Pages公開設定（main / root。https://mion-ai-mama.github.io/line-emoji-tokuten/ で公開確認済み）

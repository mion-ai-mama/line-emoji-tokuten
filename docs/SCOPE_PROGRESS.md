# 開発進捗（SCOPE_PROGRESS）

## アーキ構成

- 確定アーキ: #6 WEBアプリ（決定論）
- 操作者: ブラウザのエンドユーザー
- AI本体(プロンプトY): なし
- MCP: なし
- 自社DB: なし
- フロントUI: あり
- 動的変数: なし
- 種別: Web型（静的サイト）
- 配布: マイ専用（個人GitHubリポジトリ）

詳細は `docs/requirements.md` §0 を参照。

## 実装計画

### 開発フェーズ

| Phase | 名称 | 担当 | 状態 |
|-------|------|------|------|
| 1 | 要件定義 | Agent 1 | [x] |
| 2 | Git管理 | Agent 2 | [x]（CI/CD・Gitフック・main保護まで整備済み） |
| 3 | フロントエンド基盤 | Agent 3 | スキップ(ビルド不要の静的サイトのため。requirements.md §0 の必須条件によりReact/Vite/MUIは導入しない。デザイン基盤は css/style.css の :root に集約済み) |
| 4 | ページ実装 | Agent 4 | [x](本セッションで完成ページを実装) |
| 5 | 環境構築 | Agent 5 | スキップ(外部API連携なし) |
| 6 | バックエンド計画 | Agent 6 | スキップ(バックエンドなし) |
| 7 | エージェント構築 | Agent 7 | スキップ(AI本体Yなし) |
| 8 | バックエンド実装 | Agent 8 | スキップ(バックエンドなし) |
| 9 | フロントエンド実装(API統合) | Agent 9 | スキップ(API連携なし) |
| 10 | E2Eテスト | Agent 10 | [x](ブラウザで表示・コピー機能・動画埋め込みを確認済み) |
| 11 | ローカル動作確認 | Agent 11 | [x] |
| 12 | デプロイ | Agent 12 | [x](GitHub Pages公開済み: https://mion-ai-mama.github.io/instagram-tokuten-template/) |

## ページ / ファイル管理表

| ID | 名称 | 内容 | 着手 | 完了 |
|----|------|------|------|------|
| P-001 | index.html | 特典ページ本体(13セクション＋実例動画) | [x] | [x] |
| P-002 | css/style.css | デザイン(アイボリー基調＋大人ピンク系アクセント、レスポンシブ) | [x] | [x] |
| P-003 | js/content.js | 編集用コンテンツ一元管理ファイル | [x] | [x] |
| P-004 | js/script.js | コピー機能・スクロールアニメーション等 | [x] | [x] |
| P-005 | README.md | 複製・編集・公開方法(日本語) | [x] | [x] |

## 外部アカウント準備状況

| サービス | アカウント | 備考 |
|---------|-----------|------|
| GitHub | [x] mion-ai-mama（発信用アカウント。本名の 旧アカウント とは別、ログイン確認済み） | リポジトリ作成・Pages公開に使用 |
| LINE公式アカウント | [x] 既存の登録導線あり | CTAリンクは仮URL(`https://example.com/`)。本番URLへの差し替えが必要 |

## 未完了・ユーザー対応が必要な項目

- [x] `js/content.js` の `cta.buttonUrl` → AIマネタイズの教科書のLINE登録URLを設定済み
- [x] `assets/videos/example.mp4`（14MB）と `assets/images/video-poster.jpg`（720x405）→ 実データ配置済み
- [x] GitHub Pagesの公開設定 → 完了（`https://mion-ai-mama.github.io/instagram-tokuten-template/`）
- [x] リポジトリを「テンプレートリポジトリ」に設定 → 完了
- [x] ルートに未追跡で置かれていた `square-banner.png` → 削除（特定特典専用のブルー系バナーで、テンプレートの配色・用途と不一致のため）

## 経緯メモ（プライバシー対応）

当初 `旧アカウント`（本名ベースのアカウント）配下で公開したところ、GitHub Pagesの
URL構造上、公開URLに本名が露出することが判明。発信用の別アカウント `mion-ai-mama` を
新規作成し、リポジトリ移動・Pages再設定・テンプレート設定の引き継ぎを完了した。
今後の特典リポジトリもすべて `mion-ai-mama` 側で作成する。

2026-08-25、テンプレートのデフォルト配色をくすみブルー系から「大人ピンク×アイボリー系」
（`css/style.css` の `:root` カラー変数）に変更。以後複製する新しい特典ページは、この
配色がデフォルトになる。参照元: `assets/images/cta-banner.png`（『AIマネタイズの教科書』
バナー）の配色トーン。

2026-09-15、Phase 2（Git管理）の仕上げとして以下を整備した。

- `.gitignore`: 秘密情報ファイルと、配下に置かれた別プロジェクト
  （`chatgpt-illustration-tokuten/`・`tokuten-matome/`）のテンプレートへの混入を防止。
- Gitフック: `prepare-commit-msg`（コミット日時の自動付与）、
  `pre-commit`（秘密情報ファイルの混入拒否・JavaScript構文チェック）。
- GitHub Actions `.github/workflows/ci.yml` の `verify`:
  JavaScript構文 / 必須ファイル存在 / `index.html` のリンク切れを検査。
  ビルド工程のない静的サイトのため、npmビルド・テストは意図的に載せていない。
- `main` にブランチ保護を設定（`verify` グリーン必須・force push / 削除の禁止）。
  `enforce_admins` は false のため、オーナー本人は従来どおり直接pushできる。
- `develop` ブランチを作成。
- コミット著者名の是正: コミットが本名名義・個人メールで記録されていた。公開リポジトリのため
  発信用アカウントへ移行した経緯と矛盾する。

2026-09-16、本名の露出を全面的に除去した。

- Gitのglobal設定を `mion-ai-mama <309648686+mion-ai-mama@users.noreply.github.com>` に変更。
  これが本名混入の根本原因だった（新規リポジトリを作るたびに刻まれ続けていた）。
- 全21リポジトリ（公開16・非公開5）の履歴を書き換え、著者名・コミッター名・メール・
  ファイル本文から本名と個人メールを除去。GitHub API で全ブランチ検証済み（残存ゼロ）。
- ローカルの作業コピー14個を新しい履歴に同期（古い履歴のまま push すると復活するため）。
- GitHub Pages の公開状態・CI がグリーンであることを確認済み。
- 手順の詳細は AI の memory `github-realname-history-cleanup` に記録。

⚠️ 残課題:
- force push 後も GitHub は旧コミットを SHA 直指定で一定期間参照できる。完全消去が必要なら
  GitHub Support に purge を依頼する。フォーク・クローン済みのコピーには手が届かない。

# p_CBSTM03A 詳細設計書

## 1. 概要

`p_CBSTM03A.py` は、月次利用明細書（ステートメント）を生成するバッチプログラムです。PostgreSQL の各テーブルから情報を統合し、顧客別・アカウント別に PDF または HTML 形式（旧テキスト形式を包含）のファイルを生成して Cloud Storage (GCS) に出力します。

## 2. プログラム情報

- **プログラム ID**: `p_CBSTM03A.py`
- **言語**: Python 3.10+
- **接続DB**: Cloud SQL for PostgreSQL
- **主要モジュール**: `SQLAlchemy`, `Jinja2` (HTMLテンプレート用), `google-cloud-storage`

## 3. 入出力定義

### 3.1. 入力 (Database)

- **accounts**: アカウント基本情報・残高。
- **customers**: 顧客属性（氏名・住所）。
- **transactions**: 当月分の取引明細。

### 3.2. 出力 (Cloud Storage)

- **GCS Object**: `gs://carddemo-data/statements/{YYYYMM}/{acct_id}.html`
- **GCS Object**: `gs://carddemo-data/statements/{YYYYMM}/{acct_id}.txt` (レガシー互換として必要な場合)

## 4. 処理ロジック詳細

### 4.1. データ集計フロー

1. 全アカウント（または処理対象アカウント）のリストを取得。
2. 各アカウントに対して：
    - 顧客情報を結合。
    - 直近 1 ヶ月分の取引レコードを `transactions` から取得。
3. 情報を集約したデータオブジェクト（DTO）を作成。

### 4.2. ステートメント生成

- **HTML 形式**: Jinja2 テンプレートを使用し、集約データを流し込んで HTML を生成。旧システムの埋め込み CSS をモダンなスタイルに刷新。
- **テキスト形式**: 固定幅 80 桁のフォーマットに従い、文字列操作により生成。

### 4.3. 共通情報の取得

- 旧システムで制御ブロックから取得していたジョブ名等は、Python の環境変数や実行時引数から取得するように変更。

## 5. エラーハンドリング

- 特定アカウントのみの生成失敗（データ不足等）は警告ログを出力し、次のアカウントの処理へ続行。
- GCS への書き込み失敗等のシステムエラーは、リトライ後に異常終了。

---
[バッチ処理編](file:///Users/inohara/Documents/antigravity-demo/python-carddemo/docs/p_BasicDesign_Batch.md)

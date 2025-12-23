# p_DBUNLDGS 詳細設計書

## 1. 概要

`p_DBUNLDGS.py` は、データベース上の承認データを読み込み、Cloud Storage (GCS) 上の CSV または JSONL ファイルへエクスポート（アンロード）するバッチプログラムです。旧システム `DBUNLDGS` (IMS/GSAM) の機能を Python で再実装します。

## 2. プログラム情報

- **プログラム ID**: `p_DBUNLDGS.py`
- **言語**: Python 3.10+
- **接続DB**: Cloud SQL for PostgreSQL
- **主要モジュール**: `SQLAlchemy`, `google-cloud-storage`

## 3. 入出力定義

### 3.1. 入力 (Database)

- **Tables**: `auth_summaries`, `auth_details`（旧 IMS セグメント相当）

### 3.2. 出力 (Cloud Storage)

- **GCS Object**: `gs://carddemo-data/backup/auth_unload_{YYYYMMDD}.jsonl`
- **内容**: アカウントサマリーと関連する承認明細を統合した JSON 形式のデータ。

## 4. 処理ロジック詳細

1. **データ抽出**: `auth_summaries` と `auth_details` を JOIN し、アカウント単位でレコードを抽出。
2. **フォーマット変換**: 取得したレコードを Python 辞書形式に変換し、JSON Lines (`jsonl`) 形式でシリアライズ。
3. **ストリームアップロード**: GCS クライアントライブラリを使用し、メモリ効率良くクラウドストレージへ書き込み。

## 5. エラーハンドリング

- DB 接続エラー、GCS 書き込み権限エラー時はログ出力後、異常終了。
- データ不備のあるレコードはスキップし、エラーログに記録。

---
[バッチ処理編](file:///Users/inohara/Documents/antigravity-demo/python-carddemo/docs/p_BasicDesign_Batch.md)

# p_PAUDBUNL 詳細設計書

## 1. 概要

`p_PAUDBUNL.py` は、データベース上の承認データを読み込み、Cloud Storage (GCS) 上のファイルへエクスポート（アンロード）するバッチプログラムです。旧システム `PAUDBUNL` (IMS) の機能を Python で再実装します。`p_DBUNLDGS` と同様の目的で使用されますが、出力形式は再ロード (`p_PAUDBLOD`) に最適化されています。

## 2. プログラム情報

- **プログラム ID**: `p_PAUDBUNL.py`
- **言語**: Python 3.10+
- **接続DB**: Cloud SQL for PostgreSQL
- **主要モジュール**: `SQLAlchemy`, `google-cloud-storage`

## 3. 入出力定義

### 3.1. 入力 (Database)

- **Tables**: `auth_summaries`, `auth_details`

### 3.2. 出力 (Cloud Storage)

- **GCS Objects**:
  - `gs://carddemo-data/backup/auth_summaries.jsonl`
  - `gs://carddemo-data/backup/auth_details.jsonl`

## 4. 処理ロジック詳細

1. **データ抽出**: `auth_summaries` および `auth_details` を全件（または条件指定で）クエリ。
2. **フォーマット変換**: 各テーブルのスキーマに基づき JSON 形式へシリアライズ。
3. **並列出力**: サマリーと明細を別ファイル、または統合ファイルとして GCS へアップロード。

## 5. エラーハンドリング

- DB 接続、GCS 書き込みエラー時は異常終了。
- トランザクション分離レベルを調整し、読み取り一貫性を確保（必要に応じて）。

---
[バッチ処理編](file:///Users/inohara/Documents/antigravity-demo/python-carddemo/docs/p_BasicDesign_Batch.md)

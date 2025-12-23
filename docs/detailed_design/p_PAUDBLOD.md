# p_PAUDBLOD 詳細設計書

## 1. 概要

`p_PAUDBLOD.py` は、Cloud Storage (GCS) 上のファイルから承認・サマリーデータを読み込み、データベース上の `auth_summaries` および `auth_details` テーブルにロードするバッチプログラムです。旧システム `PAUDBLOD` (IMS) の機能を Python で再実装します。

## 2. プログラム情報

- **プログラム ID**: `p_PAUDBLOD.py`
- **言語**: Python 3.10+
- **接続DB**: Cloud SQL for PostgreSQL
- **主要モジュール**: `SQLAlchemy`, `google-cloud-storage`

## 3. 入出力定義

### 3.1. 入力 (Cloud Storage)

- **GCS Objects**:
  - `gs://carddemo-data/backup/auth_summaries.jsonl`
  - `gs://carddemo-data/backup/auth_details.jsonl`
  - (または `p_PAUDBUNL` で生成された統合ファイル)

### 3.2. 出力 (Database)

- **Tables**: `auth_summaries`, `auth_details`

## 4. 処理ロジック詳細

1. **データ読込**: GCS からバックアップファイルをストリーム読み込み。
2. **依存関係解決**:
    - 外部キー制約を考慮し、まず `auth_summaries` をインサート。
    - 次に、紐づく `auth_details` をインサート。
3. **高速ロード**: 大量データの場合は、SQLAlchemy の `bulk_insert_mappings` または PostgreSQL の `COPY` コマンドを使用して効率化。

## 5. エラーハンドリング

- 重複キー時（移行試行時のリラン等）の動作（スキップ or 上書き）をパラメータで制御。
- DB 整合性エラー時はロールバックし、エラー内容を報告。

---
[バッチ処理編](file:///Users/inohara/Documents/antigravity-demo/python-carddemo/docs/p_BasicDesign_Batch.md)

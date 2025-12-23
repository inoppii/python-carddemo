# p_CBIMPORT 詳細設計書

## 1. 概要

`p_CBIMPORT.py` は、`p_CBEXPORT.py` によって生成された統合 JSONL ファイルを Cloud Storage (GCS) から読み込み、レコード種別に基づいて PostgreSQL の各テーブル（顧客、アカウント、カード等）へデータを配布するバッチプログラムです。

## 2. プログラム情報

- **プログラム ID**: `p_CBIMPORT.py`
- **言語**: Python 3.10+
- **接続DB**: Cloud SQL for PostgreSQL
- **主要モジュール**: `SQLAlchemy`, `google-cloud-storage`

## 3. 入出力定義

### 3.1. 入力 (Cloud Storage)

- **GCS Object**: `gs://carddemo-data/migration/export_data.jsonl`

### 3.2. 出力 (Database)

- **各テーブル**: `customers`, `accounts`, `card_xref`, `transactions`, `card_details`
- **エラーログ**: インポートに失敗したレコードや未知の種別をログ出力。

## 4. 処理ロジック詳細

### 4.1. データ配布ロジック

1. GCS からオブジェクトをストリーム読み込み。
2. 各行（JSON）の `type` フィールドに基づいて、対応する SQLAlchemy ORM モデルへ変換。
    - `C` → `customers`
    - `A` → `accounts`
    - `X` → `card_xref`
    - `T` → `transactions`
    - `D` → `card_details`
3. DB へのバルクインサートまたは個別インサートを実行。

### 4.2. トランザクション管理

- 整合性を保つため、一定レコード数ごと（例：1,000件）または種別ごとにコミットを行います。拠点移行の特性上、全データを一括トランザクションで処理することを推奨。

## 5. エラーハンドリング

- 未知の `type` を含むレコードはスキップし、エラーログに詳細を出力。
- DB 制約違反等が発生した場合は、当該バッチ（またはレコード）をロールバックし、エラーを記録。

---
[バッチ処理編](file:///Users/inohara/Documents/antigravity-demo/python-carddemo/docs/p_BasicDesign_Batch.md)

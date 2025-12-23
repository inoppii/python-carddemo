# p_CBEXPORT 詳細設計書

## 1. 概要

`p_CBEXPORT.py` は、拠点移行のために PostgreSQL 内の全関連データを抽出し、Cloud Storage (GCS) 上の統合 JSON 形式オブジェクトにエクスポートするバッチプログラムです。旧システム `CBEXPORT` (COBOL) の機能を Python / GCS 環境で再実装します。

## 2. プログラム情報

- **プログラム ID**: `p_CBEXPORT.py`
- **言語**: Python 3.10+
- **接続DB**: Cloud SQL for PostgreSQL
- **主要モジュール**: `SQLAlchemy`, `google-cloud-storage`, `pydantic`

## 3. 入出力定義

### 3.1. 入力 (Database)

- **テーブル**: `customers`, `accounts`, `card_xref`, `transactions`, `card_details` (旧 `CARDFILE` 相当)
- **読込**: 各テーブルを全件取得。

### 3.2. 出力 (Cloud Storage)

- **GCS Object**: `gs://carddemo-data/migration/export_data.jsonl` (JSON Lines 形式)
  - レコードごとに `{ "type": "C", "data": { ... } }` のようなメタデータを付与。

## 4. 処理ロジック詳細

### 4.1. データ統合・シリアライズ

1. GCS クライアントの初期化。
2. 以下の順序でテーブルを走査：
    - 顧客 (`type: 'C'`)
    - アカウント (`type: 'A'`)
    - クロスリファレンス (`type: 'X'`)
    - 取引履歴 (`type: 'T'`)
    - カード詳細 (`type: 'D'`)
3. 各レコードに対し、タイムスタンプ、シーケンス番号、固定値（Branch ID '0001' 等）を付与。
4. JSON 形式にシリアライズし、GCS へアップロード。

### 4.2. 統計処理

- 各カテゴリごとの処理件数をカウントし、終了時にログ出力。

## 5. エラーハンドリング

- いずれかのテーブル読込または GCS 書き込みに失敗した場合は、ロールバック等は行わず（読込のみのため）、エラーログを出力して異常終了。

---
[バッチ処理編](file:///Users/inohara/Documents/antigravity-demo/python-carddemo/docs/p_BasicDesign_Batch.md)

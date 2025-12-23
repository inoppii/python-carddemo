# p_COBTUPDT 詳細設計書

## 1. 概要

`p_COBTUPDT.py` は、Cloud Storage (GCS) 上の CSV または JSON 入力に基づき、PostgreSQL の `transaction_types` テーブルを一括更新（追加・変更・削除）するバッチプログラムです。

## 2. プログラム情報

- **プログラム ID**: `p_COBTUPDT.py`
- **言語**: Python 3.10+
- **接続DB**: Cloud SQL for PostgreSQL
- **主要モジュール**: `SQLAlchemy`, `google-cloud-storage`

## 3. 入出力定義

### 3.1. 入力 (Cloud Storage)

- **GCS Object**: `gs://carddemo-data/input/trntype_updates.csv`
  - レイアウト: `action` (A/U/D), `tr_type_cd`, `description`

### 3.2. 出力 (Database)

- **更新テーブル**: `transaction_types`

## 4. 処理ロジック詳細

1. GCS から入力ファイルを読み込み。
2. レコードごとに `action` に応じた処理を実行：
    - **'A' (Add)**: `INSERT` 実行。重複時はエラーログを出力しスキップ。
    - **'U' (Update)**: `UPDATE` 実行。対象不在時は警告ログ。
    - **'D' (Delete)**: `DELETE` 実行。
3. すべての処理を 1 つのトランザクション、またはレコードごとに実行するかをパラメータで制御。

## 5. エラーハンドリング

- ファイル形式不正、DB 接続エラー時は異常終了。
- 個別レコードのエラーはログに出力して処理を続行。

---
[バッチ処理編](file:///Users/inohara/Documents/antigravity-demo/python-carddemo/docs/p_BasicDesign_Batch.md)

# p_CBTRN02C 詳細設計書

## 1. 概要

`p_CBTRN02C.py` は、Cloud Storage (GCS) から日次取引データ (`daily_trans.csv`) を読み込み、バリデーションを行った上で各種テーブル（`transactions`, `accounts`, `category_balances`）へ反映するバッチプログラムです。旧システム `CBTRN02C` の中核機能を Python / PostgreSQL 環境で再実装します。

## 2. プログラム情報

- **プログラム ID**: `p_CBTRN02C.py`
- **言語**: Python 3.10+
- **接続DB**: Cloud SQL for PostgreSQL
- **主要モジュール**: `SQLAlchemy`, `pandas` (または `csv`), `google-cloud-storage`

## 3. 入出力定義

### 3.1. 入力

- **GCS Object**: `gs://carddemo-data/input/daily_trans.csv`
- **Database Tables**:
  - `card_xref`: カード番号からアカウント ID の解決に使用。
  - `accounts`: 残高および限度額チェック、更新に使用。

### 3.2. 出力・更新 (Database / GCS)

- **transactions**: 有効な取引を新規レコードとして挿入。
- **accounts**: `acct_curr_bal` および期間合算項目を更新。
- **category_balances**: アカウント/種別/カテゴリ単位の残高を Upsert (挿入または更新)。
- **GCS Object**: `gs://carddemo-data/output/rejected_trans.csv` (エラー取引の出力)。

## 4. 処理ロジック詳細

### 4.1. バリデーションフロー

1. **データ形式チェック**: 数値項目や日付項目の妥当性を確認。
2. **クロスリファレンス解決**: 取引のカード番号に対応する `acct_id` が `card_xref` に存在するか。
3. **アカウント検証**:
    - `acct_id` が `accounts` テーブルに存在し、アクティブであるか。
    - 取引実行後の残高が信用限度額 (`acct_limit`) を超えないか。

### 4.2. 取引反映 (トランザクション管理)

以下の更新を DB トランザクション内で実行し、アトミック性を確保します。

1. **category_balances 更新**:
    - 既存レコードの加算、または新規レコードの作成 (ON CONFLICT DO UPDATE)。
2. **accounts 更新**:
    - `acct_curr_bal` を更新し、金額に応じて `acct_curr_cyc_credit/debit` を加算。
3. **transactions 登録**:
    - 取引明細を新規挿入。

## 5. エラーハンドリング

- バリデーションエラー時は個別レコードを `rejected_trans.csv` に書き出し、処理を続行。
- DB 接続失敗等の致命的エラー時は、全ロールバックを行い異常終了。

---
[バッチ処理編](file:///Users/inohara/Documents/antigravity-demo/python-carddemo/docs/p_BasicDesign_Batch.md)

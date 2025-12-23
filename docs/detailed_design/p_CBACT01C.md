# p_CBACT01C 詳細設計書

## 1. 概要

`p_CBACT01C.py` は、PostgreSQL の `accounts` テーブルから全レコードを読み込み、Cloud Storage (GCS) 上の複数のオブジェクトにデータを抽出・変換して出力する Python プログラムです。旧システムの `CBACT01C` (COBOL) の機能を踏襲します。

## 2. プログラム情報

- **プログラム ID**: `p_CBACT01C.py`
- **言語**: Python 3.10+
- **接続DB**: Cloud SQL for PostgreSQL
- **主要ライブラリ**: `SQLAlchemy`, `google-cloud-storage`, `pydantic`

## 3. 入出力定義

### 3.1. 入力 (Database)

- **テーブル**: `accounts`
- **主要フィールド**: `acct_id`, `acct_status`, `acct_curr_bal`, `acct_limit`, `acct_reissue_date` 等

### 3.2. 出力 (Cloud Storage)

- **Object 1**: `gs://carddemo-data/output/p_acct_extract.csv`
  - 基本属性（アカウントID、ステータス等）を抽出した標準形式。
- **Object 2**: `gs://carddemo-data/output/p_acct_balances.json`
  - 残高情報を JSON 形式で出力。旧システムの `ARRY-FILE` (OCCURS) に相当。
- **Object 3**: `gs://carddemo-data/output/p_acct_variable.jsonl`
  - 可変長レコードを模擬した JSON Lines 形式。旧システムの `VBRC-FILE` に相当。

## 4. 処理ロジック詳細

### 4.1. 主処理フロー

1. GCS クライアントおよび DB セッションの初期化。
2. `accounts` テーブルから全件取得。
3. レコードごとに以下の抽出処理を実行：
    - **標準抽出**: フィールドを CSV 形式に整形。
    - **残高抽出**: 残高データを辞書形式にまとめ、JSON 配列化。
    - **可変長シミュレーション**: レコードタイプごとに異なるスキーマで JSON オブジェクトを作成し、出力。
4. ファイルのクローズと GCS へのアップロード（またはストリーミング書き込み）。

### 4.2. データ変換仕様

- **日付変換**: `acct_reissue_date` は ISO 8601 形式 (`YYYY-MM-DD`) または業務要件に合わせた形式に変換。
- **金額形式**: `NUMERIC` から文字列または浮動小数点数への適切な変換。

## 5. エラーハンドリング

- DB 接続エラー、GCS 書き込みエラー発生時は例外をキャッチし、ログを出力した上でプロセスの異常終了 (Exit Code 1) とします。

---
[バッチ処理編](file:///Users/inohara/Documents/antigravity-demo/python-carddemo/docs/p_BasicDesign_Batch.md)

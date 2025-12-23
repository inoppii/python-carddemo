# p_CBTRN01C 詳細設計書

## 1. 概要

`p_CBTRN01C.py` は、日次取引データ (`daily_trans.csv`) の整合性をマスタテーブル（顧客、アカウント、カード）と照合して検証するバッチプログラムです。DB の更新は行わず、検証結果をログに出力します。

## 2. プログラム情報

- **プログラム ID**: `p_CBTRN01C.py`
- **言語**: Python 3.10+
- **接続DB**: Cloud SQL for PostgreSQL
- **主要モジュール**: `SQLAlchemy`, `pandas` (または `csv`), `google-cloud-storage`

## 3. 入出力定義

### 3.1. 入力 (GCS / Database)

- **GCS Object**: `gs://carddemo-data/input/daily_trans.csv`
- **Tables**: `customers`, `accounts`, `card_xref`, `transactions` (参照のみ)

### 3.2. 出力

- **標準出力 / ログ**: 検証エラー明細、正常件数、異常件数のサマリー。

## 4. 処理ロジック詳細

### 4.1. 整合性検証フロー

1. GCS から日次取引データを読み込み。
2. レコードごとに以下の検証を実施：
    - **カード検証**: カード番号が `card_xref` に存在するか。
    - **アカウント検証**: 得られたアカウント ID が `accounts` テーブルに存在するか。
    - **顧客検証**: 顧客 ID が `customers` テーブルに存在するか（必要に応じて）。
3. 検証に失敗した場合は、エラー内容（「CARD NOT FOUND」等）をログに出力。

### 4.2. 特徴

- 本プログラムは `p_CBTRN02C`（反映処理）の事前チェック用として機能します。
- 全件走査を行い、データの品質状態をレポートします。

## 5. エラーハンドリング

- システム上の致命的エラー（DB 接続不可、GCS 読込不可）はログ出力後に異常終了。
- データ不整合は業務エラーとしてログ出力し、処理自体は継続。

---
[バッチ処理編](file:///Users/inohara/Documents/antigravity-demo/python-carddemo/docs/p_BasicDesign_Batch.md)

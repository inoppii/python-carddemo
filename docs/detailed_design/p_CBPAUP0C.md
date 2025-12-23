# p_CBPAUP0C 詳細設計書

## 1. 概要

`p_CBPAUP0C.py` は、保存期間を過ぎた承認履歴データを PostgreSQL のテーブルから削除するバッチプログラムです。旧システム `CBPAUP0C` (IMS) の機能を、リレーショナルデータベース環境で再実装します。

## 2. プログラム情報

- **プログラム ID**: `p_CBPAUP0C.py`
- **言語**: Python 3.10+
- **接続DB**: Cloud SQL for PostgreSQL
- **主要モジュール**: `SQLAlchemy`, `pydantic`

## 3. 入出力定義

### 3.1. パラメータ (JSON / Environment)

- `expiry_days`: 保存期間（日数）。
- `batch_size`: 1トランザクションあたりの削除件数。

### 3.2. Database (PostgreSQL)

- **削除対象テーブル**:
  - `auth_summaries`
  - `auth_details` (カスケード削除または明示的な削除)

## 4. 処理ロジック詳細

### 4.1. 削除対象の特定

1. 現在日付から `expiry_days` を減算した基準日を算出。
2. `auth_summaries` テーブルの中から、最終更新日が基準日より古いレコードを特定。

### 4.2. 削除実行

1. `auth_details` レコードの削除（外部キー制約 `ON DELETE CASCADE` が設定されている場合は、サマリーの削除のみで可）。
2. `auth_summaries` レコードの削除。
3. 指定された `batch_size` ごとにコミットを行い、長時間ロックを回避。

### 4.3. 統計・ログ

- 削除したサマリー件数、詳細件数をカウントし、終了時にログ出力。

## 5. エラーハンドリング

- DB 接続エラー時はリトライまたは異常終了。
- 制約違反等で削除に失敗した場合は、エラー内容を記録し、そのレコードをスキップ。

---
[バッチ処理編](file:///Users/inohara/Documents/antigravity-demo/python-carddemo/docs/p_BasicDesign_Batch.md)

# p_COBIL00C 詳細設計書

## 1. 概要

`p_COBIL00C.py` は、オンラインでアカウントの引き落とし（支払い）を処理するオンラインプログラムです。現在の残高を確認し、全額支払いを実行して、その内容を `transactions` テーブルに記録します。

## 2. プログラム情報

- **プログラム ID**: `p_COBIL00C.py`
- **言語**: Python 3.10+
- **接続DB**: Cloud SQL for PostgreSQL
- **主要モジュール**: `FastAPI`, `SQLAlchemy`

## 3. 入出力定義

### 3.1. API インターフェース

- **GET `/billing/{acct_id}`**: 現在の残高を取得して表示。
- **POST `/billing/{acct_id}/pay`**: 全額支払い（残高の清算）を実行。
  - **Request Body**: `confirm`: boolean (支払確認フラグ)

### 3.2. Database (PostgreSQL)

- **更新テーブル**:
  - `accounts`: `acct_curr_bal` を 0 にリセット。
  - `transactions`: 支払い履歴（System レコード）を新規挿入。

## 4. 処理ロジック詳細

### 4.1. 支払いプロセス（トランザクション管理）

1. 指定された `acct_id` の現在の `acct_curr_bal` を取得。
2. 残高が 0 以下の場合はエラーを返却（支払い不要）。
3. ユーザーの確認が取れている場合、以下の処理を DB トランザクション内で実行：
    - **取引登録**: `transactions` テーブルに `trn_type_cd = '02'` (支払い)、金額、日時をインサート。
    - **残高更新**: `accounts` テーブルの `acct_curr_bal` を 0 にセット。
4. コミット。

## 5. エラーハンドリング

- **404 Not Found**: アカウントが存在しない場合。
- **400 Bad Request**: 残高が 0 以下、または確認フラグが未設定の場合。
- **500 Internal Server Error**: DB 更新失敗時のロールバックとエラー通知。

---
[オンライン処理編](file:///Users/inohara/Documents/antigravity-demo/python-carddemo/docs/p_BasicDesign_Online.md)

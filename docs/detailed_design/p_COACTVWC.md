# p_COACTVWC 詳細設計書

## 1. 概要

`p_COACTVWC.py` は、アカウント情報の詳細照会を行うオンライン処理プログラムです。PostgreSQL の `accounts` および `customers` テーブルを結合し、指定されたアカウント ID に基づく詳細情報を取得して返却します。

## 2. プログラム情報

- **プログラム ID**: `p_COACTVWC.py`
- **言語**: Python 3.10+
- **接続DB**: Cloud SQL for PostgreSQL
- **主要モジュール**: `FastAPI`, `SQLAlchemy`, `pydantic`

## 3. 入出力定義

### 3.1. API インターフェース

- **GET `/accounts/{acct_id}/view`**
- **Query Parameter**: `acct_id` (数値 11桁)
- **Response Body**:
  - アカウント詳細: 残高、限度額、開設日、ステータス等。
  - 顧客詳細: 氏名、住所、SSN等。

### 3.2. Database (PostgreSQL)

- **参照テーブル**: `accounts`, `customers`
- **クエリ例**:

    ```sql
    SELECT a.*, c.*
    FROM accounts a
    JOIN customers c ON a.cust_id = c.cust_id
    WHERE a.acct_id = :acct_id
    ```

## 4. 処理ロジック詳細

1. リクエストされた `acct_id` の形式チェック。
2. データベースに対し、`acct_id` をキーとした結合クエリを実行。
3. 取得したデータを `pydantic` モデルにマッピング。
4. 旧システムでは `CXACAIX` (Alternate Index) を経ていたが、リレーショナル DB では ORM による直接的な JOIN または FKey 参照で実現。
5. フォーマット済みデータを JSON 形式で返却。

## 5. エラーハンドリング

- **404 Not Found**: アカウントが存在しない場合（旧 VSAM `NOTFND` 相当）。
- **400 Bad Request**: アカウント ID の入力形式が不正な場合。

---
[オンライン処理編](file:///Users/inohara/Documents/antigravity-demo/python-carddemo/docs/p_BasicDesign_Online.md)

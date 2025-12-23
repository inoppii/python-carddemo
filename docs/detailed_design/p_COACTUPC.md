# p_COACTUPC 詳細設計書

## 1. 概要

`p_COACTUPC.py` は、アカウント情報および関連する顧客情報の詳細照会・更新を行うオンライン処理プログラムです。旧システム `COACTUPC` (CICS) を、FastAPI 等のモダンな Web フレームワークを用いた REST API または画面遷移ロジックとして再実装します。

## 2. プログラム情報

- **プログラム ID**: `p_COACTUPC.py`
- **言語**: Python 3.10+
- **接続DB**: Cloud SQL for PostgreSQL
- **主要モジュール**: `FastAPI`, `SQLAlchemy`, `pydantic`

## 3. 入出力定義

### 3.1. API インターフェース

- **GET `/accounts/{acct_id}`**: アカウントおよび顧客情報の取得。
- **PUT `/accounts/{acct_id}`**: アカウントおよび顧客情報の更新。
  - **Request Body**: 更新対象の多岐にわたるフィールド（住所、限度額、ステータス等）。

### 3.2. Database (PostgreSQL)

- **参照・更新テーブル**: `accounts`, `customers`
- **リレーション**: `accounts.cust_id` を介した結合。

## 4. 処理ロジック詳細

### 4.1. 検索・照会

- 指定された `acct_id` をキーに `accounts` をクエリし、紐づく `customers` 情報を JOIN して返却。

### 4.2. 更新前検証

- **データ形式チェック**: Pydantic モデルによるバリデーション（電話番号形式、日付妥当性等）。
- **ビジネスルールチェック**: 限度額の有効範囲確認等。

### 4.3. 更新処理 (楽観的排他制御)

- **方式**: PostgreSQL の標準機能、または `updated_at` タイムスタンプによる競合検知を使用。

1. トランザクション開始。
2. 対象レコードを最新状態で取得（必要に応じて `FOR UPDATE`）。
3. 取得時のタイムスタンプがリクエスト時のものと一致するか確認。
4. 一致していれば `accounts` および `customers` テーブルを更新。
5. コミット。

## 5. エラーハンドリング

- **404 Not Found**: 対象アカウントまたは顧客が存在しない場合。
- **409 Conflict**: 楽観的ロックエラー（他者による同時更新検知）。
- **400 Bad Request**: バリデーションエラー。

---
[オンライン処理編](file:///Users/inohara/Documents/antigravity-demo/python-carddemo/docs/p_BasicDesign_Online.md)

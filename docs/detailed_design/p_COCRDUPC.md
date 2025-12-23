# p_COCRDUPC 詳細設計書

## 1. 概要

`p_COCRDUPC.py` は、クレジットカード情報の照会および更新を行うオンライン処理プログラムです。旧システム `COCRDUPC` (CICS) を基に、データベース上の `card_details` テーブルの属性変更機能を提供します。

## 2. プログラム情報

- **プログラム ID**: `p_COCRDUPC.py`
- **言語**: Python 3.10+
- **接続DB**: Cloud SQL for PostgreSQL
- **主要モジュール**: `FastAPI`, `SQLAlchemy`, `pydantic`

## 3. インターフェース定義

### 3.1. API インスタンス

- **GET `/card-management/cards/{card_num}/edit`**: 現在の情報の取得。
- **PUT `/card-management/cards/{card_num}`**: カード情報の更新。
  - **Request Body**: `card_name`, `status`, `expiry_month`, `expiry_year`, `updated_at` (排他制御用)。

### 3.2. Database (PostgreSQL)

- **更新テーブル**: `card_details`
- **主キー**: `card_num`

## 4. 処理ロジック詳細

### 4.1. 更新前検証

- **属性バリデーション**: `expiry_month` (1-12), `status` (Y/N) 等の形式チェック。
- **変更検知**: リクエストデータが現状と同一であれば更新をスキップ。

### 4.2. 楽観的排他制御 (Update Logic)

1. DB トランザクション開始。
2. 対象レコードを検索し、`updated_at` タイムスタンプを確認。
3. クライアントから送られた `updated_at` と DB の値が異なる場合は 409 Conflict を返却。
4. 一致していれば、各種属性を更新し、`updated_at` を現在時刻に更新して `REWRITE` 相当の操作を実行。
5. コミット。

## 5. エラーハンドリング

- **404 Not Found**: カードが存在しない場合。
- **409 Conflict**: 同時更新エラー。
- **400 Bad Request**: バリデーションエラー。

---
[オンライン処理編](file:///Users/inohara/Documents/antigravity-demo/python-carddemo/docs/p_BasicDesign_Online.md)

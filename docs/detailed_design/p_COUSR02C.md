# p_COUSR02C 詳細設計書

## 1. 概要

`p_COUSR02C.py` は、既存ユーザーの情報を更新するためのオンライン処理プログラムです。旧システム `COUSR02C` (CICS) を基に、データベース上の `users` テーブルに対する更新機能を提供します。

## 2. プログラム情報

- **プログラム ID**: `p_COUSR02C.py`
- **言語**: Python 3.10+
- **接続DB**: Cloud SQL for PostgreSQL
- **主要モジュール**: `FastAPI`, `SQLAlchemy`, `pydantic`, `passlib`

## 3. インターフェース定義

### 3.1. API インターフェース

- **GET `/admin/users/{user_id}`**: 現在の情報の取得。
- **PUT `/admin/users/{user_id}`**: ユーザー情報の更新。
  - **Request Body**: `first_name`, `last_name`, `password` (任意), `user_type`.

### 3.2. Database (PostgreSQL)

- **更新テーブル**: `users`

## 4. 処理ロジック詳細

1. **認可チェック**: 管理者権限を保持しているか確認。
2. **バリデーション**: 入力形式のチェック。
3. **更新処理 (楽観的排他制御)**:
    - リクエストされた `user_id` で現在のレコードを取得。
    - パスワードが入力されている場合はハッシュ化して更新対象に含める。
    - `users` テーブルを更新。
4. **結果返却**: 成功メッセージまたは失敗の詳細を JSON で返却。

## 5. エラーハンドリング

- **404 Not Found**: ユーザーが存在しない場合。
- **403 Forbidden**: 権限不足。
- **400 Bad Request**: バリデーションエラー。

---
[オンライン処理編](file:///Users/inohara/Documents/antigravity-demo/python-carddemo/docs/p_BasicDesign_Online.md)

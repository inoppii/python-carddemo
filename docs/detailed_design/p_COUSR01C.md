# p_COUSR01C 詳細設計書

## 1. 概要

`p_COUSR01C.py` は、システムに新しいユーザーを追加登録するためのオンライン処理プログラムです。旧システム `COUSR01C` (CICS) を基に、データベースの `users` テーブルへの新規レコード挿入機能を実装します。

## 2. プログラム情報

- **プログラム ID**: `p_COUSR01C.py`
- **言語**: Python 3.10+
- **接続DB**: Cloud SQL for PostgreSQL
- **主要モジュール**: `FastAPI`, `SQLAlchemy`, `pydantic`, `passlib` (パスワードハッシュ化用)

## 3. インターフェース定義

### 3.1. API インターフェース

- **POST `/admin/users`**
  - **Request Body**:
    - `user_id`: ユーザー ID (必須、一意)
    - `first_name`, `last_name`: 氏名
    - `password`: 生パスワード
    - `user_type`: ユーザータイプ ('A': Admin, 'R': Regular)

### 3.2. Database (PostgreSQL)

- **更新テーブル**: `users`

## 4. 処理ロジック詳細

1. **認可チェック**: 管理者権限を保持しているか確認。
2. **バリデーション**: すべての必須項目が含まれているか、ID が重複していないかを確認。
3. **パスワードハッシュ化**: セキュリティ向上のため、パスワードはハッシュ化（例：bcrypt）して保存。旧システムからの改善点。
4. **登録**: `users` テーブルにインサート。
5. **結果返却**: 成功メッセージまたはエラーの詳細を JSON で返却。

## 5. エラーハンドリング

- **409 Conflict**: 指定されたユーザー ID が既に存在する場合。
- **400 Bad Request**: バリデーションエラー、パラメータ不足。
- **403 Forbidden**: 権限不足。

---
[オンライン処理編](file:///Users/inohara/Documents/antigravity-demo/python-carddemo/docs/p_BasicDesign_Online.md)

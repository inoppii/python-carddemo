# p_COUSR00C 詳細設計書

## 1. 概要

`p_COUSR00C.py` は、システムに登録されているユーザーの一覧を表示するオンライン処理プログラムです。旧システム `COUSR00C` (CICS) を基に、データベース上の `users` テーブル（旧 `USRSEC` 相当）から情報を取得し、ページング形式で提供します。

## 2. プログラム情報

- **プログラム ID**: `p_COUSR00C.py`
- **言語**: Python 3.10+
- **接続DB**: Cloud SQL for PostgreSQL
- **主要モジュール**: `FastAPI`, `SQLAlchemy`, `pydantic`

## 3. インターフェース定義

### 3.1. API インターフェース

- **GET `/admin/users`**
  - **Query Parameters**:
    - `limit`: ページあたりの件数（初期値 10）。
    - `offset`: 取得開始位置。
- **Response Body**: ユーザー情報のリスト（ID, 氏名、タイプ、作成日時等）。

### 3.2. Database (PostgreSQL)

- **参照テーブル**: `users`
- **クエリ例**:

    ```sql
    SELECT * FROM users
    ORDER BY user_id
    LIMIT :limit OFFSET :offset
    ```

## 4. 処理ロジック詳細

1. **認可チェック**: 管理者権限を保持しているか確認。
2. **データ取得**: `users` テーブルから全件、またはページング指定に基づいてレコードを抽出。
3. **ページング**: 標準的な Web API のページング方式を採用。
4. **ナビゲーション**: ユーザー更新 (`p_COUSR02C`) および削除 (`p_COUSR03C`) 画面への遷移、または新規追加画面へのリンク情報を付与。

## 5. エラーハンドリング

- **403 Forbidden**: 非管理者によるアクセス。
- **404 Not Found**: ユーザーが 1 件も登録されていない場合。

---
[オンライン処理編](file:///Users/inohara/Documents/antigravity-demo/python-carddemo/docs/p_BasicDesign_Online.md)

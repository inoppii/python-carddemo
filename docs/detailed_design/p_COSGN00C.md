# p_COSGN00C 詳細設計書

## 1. 概要

`p_COSGN00C.py` は、CardDemo アプリケーションの認証（サインオン）ロジックを実装した Python モジュールです。ユーザー ID とパスワードを受け取り、PostgreSQL の `users` テーブルと照合して認証を行い、JWT (JSON Web Token) を発行します。

## 2. プログラム情報

- **プログラム ID**: `p_COSGN00C.py`
- **言語**: Python 3.10+
- **接続DB**: Cloud SQL for PostgreSQL
- **主要モジュール**: `FastAPI`, `SQLAlchemy`, `PyJWT`, `passlib`

## 3. 入出力定義

### 3.1. API インターフェース

- **Endpoint**: `POST /auth/login`
- **Request Body**:
  - `username`: ユーザー ID (旧 `USERIDI`)
  - `password`: パスワード (旧 `PASSWDL`)
- **Response**:
  - `access_token`: JWT トークン
  - `user_type`: ユーザー権限 ('A': 管理者, 'R': 一般)
  - `status`: 'success' または 'failure'

### 3.2. Database

- **テーブル**: `users` (旧 `USRSEC`)
- **クエリ**: `SELECT * FROM users WHERE usr_id = :username`

## 4. 処理ロジック詳細

### 4.1. 認証フロー

1. リクエストから `username` と `password` を取得。
2. DB から当該ユーザーのレコードを検索。
3. ユーザーが存在しない、またはパスワード（ハッシュ）が一致しない場合は認証エラー (401 Unauthorized) を返却。
4. 認証成功時、ペイロードに `usr_id` と `usr_type` を含めた JWT を生成。
5. トークンおよび遷移先情報のヒントを返却。

### 4.2. セッション管理 (COMMAREA 相当)

- 従来の COMMAREA へのデータセットに代わり、JWT のペイロードまたは Redis 等のセッションストアにユーザー情報を保持し、以降のリクエストで利用可能にします。

## 5. エラーハンドリング

- **Invalid User**: 「ユーザー名またはパスワードが正しくありません」と返却。
- **DB Connection Error**: 500 Internal Server Error として処理し、詳細をログに出力。

---
[オンライン処理編](file:///Users/inohara/Documents/antigravity-demo/python-carddemo/docs/p_BasicDesign_Online.md)

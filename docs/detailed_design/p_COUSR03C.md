# p_COUSR03C 詳細設計書

## 1. 概要

`p_COUSR03C.py` は、システムからユーザーを削除するためのオンライン処理プログラムです。旧システム `COUSR03C` (CICS) を基に、データベース上の `users` テーブルからのレコード物理削除機能を実装します。

## 2. プログラム情報

- **プログラム ID**: `p_COUSR03C.py`
- **言語**: Python 3.10+
- **接続DB**: Cloud SQL for PostgreSQL
- **主要モジュール**: `FastAPI`, `SQLAlchemy`, `pydantic`

## 3. インターフェース定義

### 3.1. API インターフェース

- **GET `/admin/users/{user_id}/confirm`**: 削除前の確認用データの取得。
- **DELETE `/admin/users/{user_id}`**: ユーザーの削除。

### 3.2. Database (PostgreSQL)

- **更新テーブル**: `users`

## 4. 処理ロジック詳細

1. **認可チェック**: 管理者権限を保持しているか確認。
2. **削除確認**: クライアント側で削除確認ダイアログ等を表示するためのメタデータを返却。
3. **削除実行**:
    - 指定された `user_id` で `users` テーブルを検索。
    - 存在すれば `DELETE` を実行。
    - 拠点のセキュリティポリシーに基づき、物理削除または `is_deleted` フラグによる論理削除を選択可能（本設計では旧踏襲の物理削除を基本とする）。
4. **結果返却**: 成功メッセージを JSON で返却。

## 5. エラーハンドリング

- **404 Not Found**: ユーザーが存在しない。
- **403 Forbidden**: 権限不足。

---
[オンライン処理編](file:///Users/inohara/Documents/antigravity-demo/python-carddemo/docs/p_BasicDesign_Online.md)

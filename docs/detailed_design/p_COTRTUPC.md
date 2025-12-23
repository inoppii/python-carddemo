# p_COTRTUPC 詳細設計書

## 1. 概要

`p_COTRTUPC.py` は、取引種別の詳細表示、新規追加、更新、および削除（CRUD 操作）を行うオンライン処理プログラムです。旧システム `COTRTUPC` (CICS) を基に、データベース上の `transaction_types` テーブルに対する単一レコード操作を再実装します。

## 2. プログラム情報

- **プログラム ID**: `p_COTRTUPC.py`
- **言語**: Python 3.10+
- **接続DB**: Cloud SQL for PostgreSQL
- **主要モジュール**: `FastAPI`, `SQLAlchemy`, `pydantic`

## 3. インターフェース定義

### 3.1. API インターフェース

- **GET `/admin/transaction-types/{tr_type}`**: 詳細情報の取得。
- **POST `/admin/transaction-types`**: 新規追加。
- **PUT `/admin/transaction-types/{tr_type}`**: 既存情報の更新。
- **DELETE `/admin/transaction-types/{tr_type}`**: 削除。

### 3.2. Database (PostgreSQL)

- **操作テーブル**: `transaction_types`
- **主キー**: `tr_type` (2桁コード)

## 4. 処理ロジック詳細

1. **認可チェック**: 管理者権限を保持しているか確認。
2. **バリデーション**: `tr_type` コードの重複チェック（新規追加時）、説明の長さチェック等。
3. **CRUD 処理**:
    - **照会**: 該当 ID を `SELECT`。
    - **追加/更新**: SQLAlchemy ORM を使用してステートを保存。
    - **削除**: 該当 ID の物理削除、または論理削除（運用方針に依存）。
4. **結果返却**: 処理成功メッセージまたは詳細データを JSON で返却。

## 5. エラーハンドリング

- **409 Conflict**: 重複する種別コードでの登録試行。
- **404 Not Found**: 対象の種別が存在しない。
- **403 Forbidden**: 権限不足。

---
[オンライン処理編](file:///Users/inohara/Documents/antigravity-demo/python-carddemo/docs/p_BasicDesign_Online.md)

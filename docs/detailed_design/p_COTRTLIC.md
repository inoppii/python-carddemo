# p_COTRTLIC 詳細設計書

## 1. 概要

`p_COTRTLIC.py` は、取引種別の一覧を表示し、更新・削除・追加のナビゲーションを行うオンライン処理プログラムです。旧システム `COTRTLIC` (CICS) を基に、データベース上の `transaction_types` テーブルから情報を取得し、ページング形式で提供します。

## 2. プログラム情報

- **プログラム ID**: `p_COTRTLIC.py`
- **言語**: Python 3.10+
- **接続DB**: Cloud SQL for PostgreSQL
- **主要モジュール**: `FastAPI`, `SQLAlchemy`, `pydantic`

## 3. インターフェース定義

### 3.1. API インターフェース

- **GET `/admin/transaction-types`**
  - **Query Parameters**:
    - `tr_type`: コードによる前方一致検索 (オプション)。
    - `description`: 説明による部分一致検索 (オプション)。
    - `limit`: ページあたりの件数（初期値 7）。
    - `offset`: 取得開始位置。
- **Response Body**: 取引種別のリスト。

### 3.2. Database (PostgreSQL)

- **参照テーブル**: `transaction_types`
- **クエリ例**:

    ```sql
    SELECT * FROM transaction_types
    WHERE (:tr_type IS NULL OR tr_type LIKE :tr_type || '%')
      AND (:description IS NULL OR tr_description ILIKE '%' || :description || '%')
    ORDER BY tr_type
    LIMIT :limit OFFSET :offset
    ```

## 4. 処理ロジック詳細

1. **認可チェック**: 管理者権限を保持しているか確認。
2. **データ取得**: `transaction_types` テーブルから検索条件に基づいてレコードを抽出。
3. **ページング**: 標準的な Web API のページング方式を採用。
4. **ナビゲーション**: 更新/削除画面 (`p_COTRTUPC`) への遷移、または新規追加画面へのリンク情報を付与。

## 5. エラーハンドリング

- **403 Forbidden**: 非管理者によるアクセス。
- **404 Not Found**: 該当する種別が存在しない場合。

---
[オンライン処理編](file:///Users/inohara/Documents/antigravity-demo/python-carddemo/docs/p_BasicDesign_Online.md)

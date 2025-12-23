# p_COTRN00C 詳細設計書

## 1. 概要

`p_COTRN00C.py` は、取引履歴の一覧を表示するオンライン処理プログラムです。旧システム `COTRN00C` (CICS) を基に、データベース上の `transactions` テーブルから取引データを取得し、ページング形式で提供します。

## 2. プログラム情報

- **プログラム ID**: `p_COTRN00C.py`
- **言語**: Python 3.10+
- **接続DB**: Cloud SQL for PostgreSQL
- **主要モジュール**: `FastAPI`, `SQLAlchemy`, `pydantic`

## 3. インターフェース定義

### 3.1. API インターフェース

- **GET `/transactions`**
  - **Query Parameters**:
    - `start_trn_id`: 検索開始位置となる取引 ID (オプション)。
    - `limit`: ページあたりの件数（初期値 10）。
    - `offset`: 取得開始位置。
- **Response Body**: 取引データのリスト（ID, 日時、金額、タイプ等）。

### 3.2. Database (PostgreSQL)

- **参照テーブル**: `transactions`
- **クエリ例**:

    ```sql
    SELECT * FROM transactions
    WHERE (:start_trn_id IS NULL OR trn_id >= :start_trn_id)
    ORDER BY trn_id
    LIMIT :limit OFFSET :offset
    ```

## 4. 処理ロジック詳細

1. **入力バリデーション**: `start_trn_id` が数値であることを確認。
2. **データ取得**: `transactions` テーブルから指定された条件でレコードを取得。
3. **ページング**: `LIMIT` と `OFFSET` を使用。
4. **結果返却**: リスト形式でレスポンス。詳細表示 (`p_COTRN01C`) へのリンク用メタデータを含める。

## 5. エラーハンドリング

- **404 Not Found**: 取引履歴が 1 件も見つからない場合。
- **400 Bad Request**: 引数の形式が不正な場合。

---
[オンライン処理編](file:///Users/inohara/Documents/antigravity-demo/python-carddemo/docs/p_BasicDesign_Online.md)

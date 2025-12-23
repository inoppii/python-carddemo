# p_COCRDLIC 詳細設計書

## 1. 概要

`p_COCRDLIC.py` は、クレジットカードの一覧を表示するオンライン処理プログラムです。アカウント ID またはカード番号に基づき、カード情報のリストをページング形式で提供します。

## 2. プログラム情報

- **プログラム ID**: `p_COCRDLIC.py`
- **言語**: Python 3.10+
- **接続DB**: Cloud SQL for PostgreSQL
- **主要モジュール**: `FastAPI`, `SQLAlchemy`, `pydantic`

## 3. インターフェース定義

### 3.1. API インターフェース

- **GET `/card-management/cards`**
  - **Query Parameters**:
    - `acct_id`: アカウント ID (オプション)。
    - `card_num`: カード番号 (オプション、フィルタ用)。
    - `limit`: ページあたりの件数（初期値 7）。
    - `offset`: 取得開始位置。

### 3.2. Database (PostgreSQL)

- **参照テーブル**: `card_details` (旧 `CARDDAT` 相当), `card_xref`
- **クエリ例**:

    ```sql
    SELECT * FROM card_details
    WHERE (:acct_id IS NULL OR acct_id = :acct_id)
      AND (:card_num IS NULL OR card_num LIKE :card_num)
    ORDER BY card_num
    LIMIT :limit OFFSET :offset
    ```

## 4. 処理ロジック詳細

1. 入力パラメータのバリデーション。
2. 指定された条件（アカウント ID 等）に基づいて `card_details` テーブルをクエリ。
3. **ページング**: `LIMIT` および `OFFSET` を使用して、旧システムのスクロール機能をエミュレート。
4. 返却結果には、詳細表示 (`p_COCRDSLC`) および更新 (`p_COCRDUPC`) へのリンク（または識別子）を含める。

## 5. エラーハンドリング

- **404 Not Found**: 該当するカードが存在しない場合。
- **400 Bad Request**: パラメータの形式が不正な場合。

---
[オンライン処理編](file:///Users/inohara/Documents/antigravity-demo/python-carddemo/docs/p_BasicDesign_Online.md)

# p_COPAUS0C 詳細設計書

## 1. 概要

`p_COPAUS0C.py` は、承認リクエストの履歴を一覧表示するオンライン処理プログラムです。旧システム `COPAUS0C` (CICS/IMS) を基に、データベース上の承認履歴テーブルから情報を取得し、ページング形式で提供します。

## 2. プログラム情報

- **プログラム ID**: `p_COPAUS0C.py`
- **言語**: Python 3.10+
- **接続DB**: Cloud SQL for PostgreSQL
- **主要モジュール**: `FastAPI`, `SQLAlchemy`, `pydantic`

## 3. インターフェース定義

### 3.1. API インターフェース

- **GET `/authorizations/summaries`**
  - **Query Parameters**:
    - `acct_id`: アカウント ID (必須)
    - `limit`: 1ページあたりの件数。
    - `offset`: 取得開始位置。
- **Response Body**: 承認履歴のサマリーリスト。

### 3.2. Database (PostgreSQL)

- **参照テーブル**: `auth_summaries`, `auth_details`
- **クエリ例**:

    ```sql
    SELECT * FROM auth_details
    WHERE acct_id = :acct_id
    ORDER BY auth_timestamp DESC
    LIMIT :limit OFFSET :offset
    ```

## 4. 処理ロジック詳細

1. **認可チェック**: 承認閲覧権限を保持しているか確認。
2. **データ取得**: 指定されたアカウント ID に紐づく承認明細を、最新順に取得。
3. **ページング**: 標準的な Web API のページング方式を採用。
4. **ナビゲーション**: 個別の承認明細詳細 (`p_COPAUS1C`) へのリンク情報を付与。

## 5. エラーハンドリング

- **404 Not Found**: 該当するアカウントまたは履歴が存在しない場合。
- **400 Bad Request**: アカウント ID が未入力、または形式不正。

---
[オンライン処理編](file:///Users/inohara/Documents/antigravity-demo/python-carddemo/docs/p_BasicDesign_Online.md)

# p_COCRDSLC 詳細設計書

## 1. 概要

`p_COCRDSLC.py` は、特定のクレジットカードの詳細情報を照会・表示するオンライン処理プログラムです。カード番号またはアカウント ID に紐づくカード詳細をデータベースから取得して返却します。

## 2. プログラム情報

- **プログラム ID**: `p_COCRDSLC.py`
- **言語**: Python 3.10+
- **接続DB**: Cloud SQL for PostgreSQL
- **主要モジュール**: `FastAPI`, `SQLAlchemy`, `pydantic`

## 3. インターフェース定義

### 3.1. API インターフェース

- **GET `/card-management/cards/{card_num}`**
  - **Path Parameter**: `card_num` (16桁)
  - **Response Body**:
    - `acct_id`: アカウント ID
    - `card_name`: カード名義人
    - `status`: ステータス
    - `expiry_month`, `expiry_year`: 有効期限

### 3.2. Database (PostgreSQL)

- **参照テーブル**: `card_details`
- **クエリ**: `SELECT * FROM card_details WHERE card_num = :card_num`

## 4. 処理ロジック詳細

1. **入力バリデーション**: `card_num` が 16桁かつ数値であることを確認。
2. **データ取得**: `card_details` テーブルから指定されたカード番号のレコードを取得。
3. **結果返却**: 取得データを `pydantic` モデル経由で JSON として返却。
4. **遷移ヒント**: クライアント側で更新画面 (`p_COCRDUPC`) への遷移を容易にするためのメタデータを含める。

## 5. エラーハンドリング

- **404 Not Found**: カードが存在しない場合。
- **400 Bad Request**: 引数の形式が不正な場合。

---
[オンライン処理編](file:///Users/inohara/Documents/antigravity-demo/python-carddemo/docs/p_BasicDesign_Online.md)

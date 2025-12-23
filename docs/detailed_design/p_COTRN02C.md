# p_COTRN02C 詳細設計書

## 1. 概要

`p_COTRN02C.py` は、新しい取引データを手動で追加するためのオンライン処理プログラムです。旧システム `COTRN02C` (CICS) を基に、アカウント ID またはカード番号による補完機能、およびデータのバリデーション機能を再実装します。

## 2. プログラム情報

- **プログラム ID**: `p_COTRN02C.py`
- **言語**: Python 3.10+
- **接続DB**: Cloud SQL for PostgreSQL
- **主要モジュール**: `FastAPI`, `SQLAlchemy`, `pydantic`

## 3. インターフェース定義

### 3.1. API インターフェース

- **GET `/transactions/new-context`**: 直前の入力データの取得（テンプレート機能用、任意）。
- **POST `/transactions`**: 新規取引の登録。
  - **Request Body**: `acct_id` または `card_num`, `trn_type_cd`, `trn_catg_cd`, `amount`, `orig_date`, `merchant_name` 等。

### 3.2. Database (PostgreSQL)

- **参照・更新テーブル**:
  - `transactions`: 新規レコード挿入。
  - `accounts`, `card_xref`: アカウント/カードの存在確認および相互補完。

## 4. 処理ロジック詳細

### 4.1. アカウント/カード相互補完

1. `acct_id` のみが入力された場合、`card_xref` を参照して `card_num` を特定。
2. `card_num` のみが入力された場合、同様に `acct_id` を特定。
3. 両方入力された場合は整合性をチェック。

### 4.2. データバリデーション

- Pydantic モデルによる型・形式チェック。
- `orig_date` 等の日付妥当性（未来日付の制限、フォーマット等）。
- 金額の範囲チェック。

### 4.3. 登録処理

1. DB トランザクション開始。
2. 取引 ID は PostgreSQL の `SERIAL` または `UUID` 等を使用して自動採番。
3. `transactions` テーブルにインサート。
4. コミット。成功時に生成された取引 ID を返却。

## 5. エラーハンドリング

- **404 Not Found**: アカウントまたはカードが存在しない。
- **400 Bad Request**: バリデーションエラー、不整合なデータ。

---
[オンライン処理編](file:///Users/inohara/Documents/antigravity-demo/python-carddemo/docs/p_BasicDesign_Online.md)

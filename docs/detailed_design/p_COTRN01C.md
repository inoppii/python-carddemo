# p_COTRN01C 詳細設計書

## 1. 概要

`p_COTRN01C.py` は、特定の取引の全項目（カード番号、金額、取引日時、加盟店情報など）を表示する詳細照会プログラムです。旧システム `COTRN01C` (CICS) を基に、データベースから単一の取引情報を取得して提供します。

## 2. プログラム情報

- **プログラム ID**: `p_COTRN01C.py`
- **言語**: Python 3.10+
- **接続DB**: Cloud SQL for PostgreSQL
- **主要モジュール**: `FastAPI`, `SQLAlchemy`, `pydantic`

## 3. インターフェース定義

### 3.1. API インターフェース

- **GET `/transactions/{trn_id}`**
- **Path Parameter**: `trn_id`
- **Response Body**: 取引詳細（カード番号、タイプ名、カテゴリ名、金額、日時、加盟店情報等）。

### 3.2. Database (PostgreSQL)

- **参照テーブル**: `transactions`
- **関連参照**: `transaction_types`, `transaction_categories`

## 4. 処理ロジック詳細

1. **データ取得**: `trn_id` をキーに `transactions` テーブルをクエリ。
2. **名称解決**: コード値に対応するタイプ名称やカテゴリ名称を、DB 結合またはキャッシュから取得。
3. **データ整形**: 金額、日時のフォーマット（ISO 形式等）を調整。
4. **結果返却**: JSON 形式で詳細情報を返却。

## 5. エラーハンドリング

- **404 Not Found**: 取引 ID が存在しない場合。
- **400 Bad Request**: 引数の形式が不正な場合。

---
[オンライン処理編](file:///Users/inohara/Documents/antigravity-demo/python-carddemo/docs/p_BasicDesign_Online.md)

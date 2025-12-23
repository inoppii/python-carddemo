# p_COPAUS1C 詳細設計書

## 1. 概要

`p_COPAUS1C.py` は、特定の承認リクエストの詳細情報を表示するオンライン処理プログラムです。旧システム `COPAUS1C` (CICS/IMS) を基に、データベース上の承認履歴テーブルから単一の承認詳細を取得して提供します。

## 2. プログラム情報

- **プログラム ID**: `p_COPAUS1C.py`
- **言語**: Python 3.10+
- **接続DB**: Cloud SQL for PostgreSQL
- **主要モジュール**: `FastAPI`, `SQLAlchemy`, `pydantic`

## 3. インターフェース定義

### 3.1. API インターフェース

- **GET `/authorizations/{auth_key}`**
- **Path Parameter**: `auth_key` (承認・取引キー)
- **Response Body**: 承認詳細（カード番号、金額、日時、加盟店情報、承認結果理由、不正フラグ等）。

### 3.2. Database (PostgreSQL)

- **参照テーブル**: `auth_details`
- **クエリ**: `SELECT * FROM auth_details WHERE auth_key = :auth_key`

## 4. 処理ロジック詳細

1. **データ取得**: `auth_key` をキーに `auth_details` テーブルをクエリ。
2. **名称・理由解決**: 理由コード（`0000` -> "APPROVED" 等）を人間が読めるメッセージに変換。
3. **ナビゲーション**: 不正フラグ設定 (`p_COPAUS2C`) へのリンク情報を付与。
4. **結果返却**: JSON 形式で詳細情報を返却。

## 5. エラーハンドリング

- **404 Not Found**: 承認キーが見つからない場合。
- **400 Bad Request**: キーの形式が不正な場合。

---
[オンライン処理編](file:///Users/inohara/Documents/antigravity-demo/python-carddemo/docs/p_BasicDesign_Online.md)

# p_COPAUS2C 詳細設計書

## 1. 概要

`p_COPAUS2C.py` は、特定の承認取引を不正 (Fraud) としてマークする、または解除するためのオンライン処理プログラムです。旧システム `COPAUS2C` (CICS/IMS) を基に、データベース上の `auth_details` テーブルおよび監査用 `auth_frauds` テーブルの更新機能を実装します。

## 2. プログラム情報

- **プログラム ID**: `p_COPAUS2C.py`
- **言語**: Python 3.10+
- **接続DB**: Cloud SQL for PostgreSQL
- **主要モジュール**: `FastAPI`, `SQLAlchemy`, `pydantic`

## 3. インターフェース定義

### 3.1. API インターフェース

- **POST `/authorizations/{auth_key}/report-fraud`**: 不正として報告。
- **POST `/authorizations/{auth_key}/remove-fraud`**: 不正報告の解除。

### 3.2. Database (PostgreSQL)

- **更新テーブル**:
  - `auth_details`: 該当レコードの `fraud_flag` を更新。
  - `auth_frauds`: 不正報告の履歴（監査ログ）を挿入または更新。

## 4. 処理ロジック詳細

1. **認可チェック**: 承認管理者権限を保持しているか確認。
2. **不正報告処理**:
    - DB トランザクション開始。
    - `auth_details` の特定レコードに対し、フラグを設定。
    - `auth_frauds` テーブルに、誰がいつ報告したかの情報を記録。
3. **解除処理**:
    - 同様にフラグをリセットし、監査記録を更新。
4. **結果返却**: 成功またはエラーメッセージを JSON で返却。

## 5. エラーハンドリング

- **404 Not Found**: 承認キーが存在しない。
- **403 Forbidden**: 権限不足。

---
[オンライン処理編](file:///Users/inohara/Documents/antigravity-demo/python-carddemo/docs/p_BasicDesign_Online.md)

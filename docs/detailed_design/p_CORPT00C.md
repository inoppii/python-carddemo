# p_CORPT00C 詳細設計書

## 1. 概要

`p_CORPT00C.py` は、オンライン（API/Web）からバッチジョブの実行リクエストを受け取り、各種レポートを作成するためのプログラムです。旧システム `CORPT00C` (CICS) を基に、Cloud Workflows や Cloud Scheduler を介したバッチキックの仕組みを再実装します。

## 2. プログラム情報

- **プログラム ID**: `p_CORPT00C.py`
- **言語**: Python 3.10+
- **接続DB**: Cloud SQL for PostgreSQL
- **主要モジュール**: `FastAPI`, `google-cloud-workflows`

## 3. インターフェース定義

### 3.1. API インターフェース

- **POST `/reports/submit`**
  - **Request Body**:
    - `type`: レポートタイプ (MONTHLY/YEARLY/CUSTOM)
    - `start_date`, `end_date`: 対象期間
- **Response Body**: ジョブ実行 ID またはステータス。

## 4. 処理ロジック詳細

1. **認可チェック**: レポート作成権限を保持しているか確認。
2. **パラメータ作成**: 指定されたタイプに基づき、開始日・終了日を確定。
3. **バッチ実行リクエスト**:
    - メインフレームの JCL 投入に代わり、Google Cloud Workflows の API を呼び出してバッチ処理（例：`p_CBTRN03C`）を実行。
    - 入力パラメータ（日付範囲等）を Workflow の引数として渡す。
4. **結果返却**: ジョブを受け付けた旨と、非同期処理の実行状況を確認するための ID を返却。

## 5. エラーハンドリング

- **400 Bad Request**: 日付指定の不整合、またはサポートされていないレポートタイプ。
- **500 Internal Server Error**: Workflows API 呼び出し失敗。

---
[オンライン処理編](file:///Users/inohara/Documents/antigravity-demo/python-carddemo/docs/p_BasicDesign_Online.md)

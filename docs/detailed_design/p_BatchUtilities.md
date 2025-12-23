# p_BatchUtilities 詳細設計書

## 1. 概要

本設計書は、Python バッチ処理群で共通的に使用されるユーティリティモジュールの設計を定義します。旧システムのシステムルーチンや LE API を、Python 標準ライブラリおよび共通クラスで再実装します。

## 2. ユーティリティ一覧 (Python)

### 2.1. 日付ユーティリティ (`p_date_utils.py`)

- **役割**: 日付形式の検証、変換、および日付差計算を提供します。
- **機能**:
  - `validate_date(date_str, format)`: 指定された形式での日付妥当性チェック。
  - `to_iso_format(date_str, input_format)`: 各種形式から ISO 8601 形式への変換。
  - `get_days_diff(date1, date2)`: 2つの日付間の日数計算（旧 `CEEDAYS` 相当）。
- **実装**: Python 標準の `datetime` モジュールを使用。

### 2.2. 待機処理 (`p_wait_utils.py`)

- **役割**: 指定された秒数だけプロセスを停止させます。
- **機能**:
  - `wait_seconds(seconds)`: 指定秒数（少数点以下可）の待機。
- **実装**: `time.sleep()` を使用。

### 2.3. データアクセス抽象化 (`p_db_utils.py`)

- **役割**: SQLAlchemy を用いたデータベース（Cloud SQL）接続およびクエリ実行の抽象化。
- **機能**:
  - `get_session()`: DB セッションの取得。
  - `execute_query(sql, params)`: 生の SQL 実行。
  - `common_crud`: テーブルごとの基本操作を提供する ORM モデルベースのラッパー。

## 3. 特記事項

- メインフレーム固有の低レイヤな呼び出しを Python の高抽象な機能で置き換えることで、コードの可読性と保守性を向上させます。
- すべてのバッチプログラム (`p_*.py`) は、これらのユーティリティをインポートして使用することを標準とします。

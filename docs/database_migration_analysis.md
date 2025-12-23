# データベース移行分析レポート: DB2 to PostgreSQL

CardDemo アプリケーションのデータベースを DB2 から PostgreSQL に変更することの実現可能性について分析しました。

## 結論

**変更は可能です。**
スキーマ定義 (DDL) およびアプリケーションコード (COBOL 内の埋め込み SQL) は、PostgreSQL と非常に高い互換性を持っており、移行の難易度は低いです。

ただし、実行環境 (メインフレームエミュレーターやモダナイゼーション後のプラットフォーム) が PostgreSQL 接続をサポートしている必要があります。

## 詳細分析

### 1. スキーマ定義 (DDL) の互換性

現在の DDL (`app/app-transaction-type-db2/ddl/`) は標準的な SQL データ型を使用しており、PostgreSQL でもそのまま使用可能です。

| DB2 データ型 | PostgreSQL 対応型 | 備考 |
| :--- | :--- | :--- |
| `CHAR(n)` | `CHAR(n)` | 完全互換 |
| `VARCHAR(n)` | `VARCHAR(n)` | 完全互換 |
| `DECIMAL(p,s)` | `DECIMAL(p,s)` | 完全互換 |
| `TIMESTAMP` | `TIMESTAMP` | 完全互換 |
| `DATE` | `DATE` | 完全互換 |

**実際の定義例 (TRNTYCAT.ddl):**

```sql
CREATE TABLE CARDDEMO.TRANSACTION_TYPE_CATEGORY
(   TRC_TYPE_CODE                  CHAR(2) NOT NULL,
    ...
    PRIMARY KEY(TRC_TYPE_CODE,TRC_TYPE_CATEGORY),
    FOREIGN KEY ... ON DELETE RESTRICT);
```

この定義は PostgreSQL 構文としても完全に有効です (スキーマ `CARDDEMO` を事前に作成する必要があります)。

### 2. アプリケーションコード (埋め込み SQL) の互換性

COBOL プログラム (`COTRTLIC.cbl` 等) で使用されている埋め込み SQL を確認しました。

- **SQL 構文**: `SELECT`, `INSERT`, `UPDATE`, `DELETE`, `CURSOR`, `ORDER BY` など標準的な構文が使用されています。
- **関数**: `TRIM()` 関数が使用されていますが、これは PostgreSQL でもサポートされています。
- **ホスト変数**: `:VAR-NAME` 形式の使用はプリコンパイラによりますが、一般的なモダン化ツール (Micro Focus, GnuCOBOL など) は PostgreSQL 向けのプリコンパイルまたは ODBC 経由での実行をサポートしています。

### 3. 移行に必要な手順

もし AWS Mainframe Modernization のコンテキストで PostgreSQL (Amazon Aurora PostgreSQL 等) に移行する場合：

1. **データベース構築**:
   - PostgreSQL インスタンスを作成または用意します。
   - `CARDDEMO` スキーマを作成します (`CREATE SCHEMA CARDDEMO;`)。
   - DDL を実行してテーブルを作成します。

2. **アプリケーションランタイム構成**:
   - **リプラットフォーム (Micro Focus / Blu Age)**: 環境設定で DB 接続先を DB2 から PostgreSQL に変更し、適切な ODBC ドライバー等を設定します。
   - **リファクター (Java 化)**: Java アプリケーション (Spring Boot 等) に変換する場合、`application.properties` 等で JDBC 接続先を PostgreSQL に変更します。

3. **データの移行**:
   - 既存のデータを CSV 等でエクスポートし、PostgreSQL の `COPY` コマンド等でロードします。

## 注意点

- **実行環境**: COBOL のままローカル PC (macOS) で動作させる場合、GnuCOBOL と PostgreSQL の連携設定 (OpenESQL や ODBC) が必要となり、環境構築の難易度はやや高いです。
- **DB2 固有機能**: 今回の調査範囲では見当たりませんでしたが、もし DB2 固有のストアドプロシージャや特殊なデータ型を使用している箇所があれば、手動での修正が必要です。

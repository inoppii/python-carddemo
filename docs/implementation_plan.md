# PostgreSQL 変換・導入計画

AWS Mainframe Modernization CardDemo のデータベース定義 (DDL) を PostgreSQL 用に変換し、検証を経てリポジトリに追加します。

## ユーザーレビューが必要な事項

- **検証環境**: 現在の環境には Docker がありません。`brew install postgresql` を実行してローカルに PostgreSQL をインストールし、検証を行ってもよろしいでしょうか？ (検証後にアンインストールも可能です)
- **成果物**: 既存の DB2 ファイルを上書きせず、`ddl_postgres` などの新しいディレクトリを作成して配置します。

## 変更内容

以下の新しいディレクトリとファイルを作成します。

### [NEW] `app/app-transaction-type-db2/ddl-postgres/`

- `TRNTYPE.sql` (PostgreSQL 用 DDL)
- `TRNTYCAT.sql` (PostgreSQL 用 DDL)
- `XTRNTYPE.sql` (PostgreSQL 用 Index DDL - 必要であれば)
- `XTRNTYCAT.sql` (PostgreSQL 用 Index DDL - 必要であれば)

### [NEW] `app/app-authorization-ims-db2-mq/ddl-postgres/`

- `AUTHFRDS.sql`

## 検証計画

### 1. ローカル検証 (承認された場合)

1. `brew install postgresql` で PostgreSQL をインストール。
2. ローカルサーバーを起動 (`pg_ctl start`).
3. `createdb carddemo_test` でテスト用DB作成。
4. `psql` コマンドで変換後の SQL ファイルを実行し、エラーが出ないことを確認。
5. 検証終了後、停止・削除。

### 2. 静的検証 (インストール不可の場合)

- 生成された SQL 文法を目視およびドキュメント照合で確認。

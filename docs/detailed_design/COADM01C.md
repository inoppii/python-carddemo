# COADM01C 詳細設計書

## 1. 概要

`COADM01C` は、管理者権限を持つユーザーが使用するメインメニュープログラムです。ユーザー管理（追加、更新、削除、一覧）やトランザクションタイプの管理機能へのエントリポイントを提供します。

## 2. プログラム情報

- **プログラム ID**: `COADM01C`
- **トランザクション ID**: `CA00`
- **タイプ**: CICS オンラインプログラム
- **使用マップ**: `COADM1A` (Mapset: `COADM01`)

## 3. 画面レイアウト

- **メニュー項目**:
  1. User List (Security) -> `COUSR00C`
  2. User Add (Security) -> `COUSR01C`
  3. User Update (Security) -> `COUSR02C`
  4. User Delete (Security) -> `COUSR03C`
  5. Transaction Type List/Update (Db2) -> `COTRTLIC`
  6. Transaction Type Maintenance (Db2) -> `COTRTUPC`

## 4. 処理ロジック詳細

### 4.1. 初期処理 (`MAIN-PARA`)

- コマエリアが空の場合は、サインオン画面 (`COSGN00C`) へ戻ります。
- `CDEMO-PGM-REENTER` がオフの場合は、画面を初期化して送出します。

### 4.2. 入力処理 (`PROCESS-ENTER-KEY`)

- ユーザーが入力したオプション番号を取得し、バリデーション（数値チェック、範囲チェック）を行います。
- 有効なオプションが選択された場合、`XCTL` を使用して対象のプログラムへ制御を移します。
- 遷移先プログラムに渡すための `CDEMO-FROM-PROGRAM` や `CDEMO-FROM-TRANID` などのコンテキスト情報を設定します。

### 4.3. 終了・戻り処理

- `PF3` キーが押された場合、サインオン画面 (`COSGN00C`) へ戻ります。

## 5. 関連リソース

- **コピー句**:
  - `COCOM01Y`: 共通コマエリア定義
  - `COADM02Y`: 管理メニューオプション定義
  - `COADM01`: BMS マップ定義
- **ファイル**:
  - 本プログラム自体はファイルアクセスを行いません（遷移先で実施）。

## 6. 特記事項

- メニュー項目は `COADM02Y` において定義されており、動的に画面に表示されます。
- `DUMMY` で始まるプログラム名が設定されている場合は、未インストールのメッセージを表示します。

# COCRDLIC 詳細設計書

## 1. 概要

`COCRDLIC` は、クレジットカードの一覧を表示する CICS オンラインプログラムです。
主にアカウント ID に紐づくカードを一覧表示するために使用されます。管理者権限を持つユーザーはすべてのカードを表示できるロジックが含まれていますが、基本的にはアカウント ID コンテキストでの使用が想定されています。

## 2. プログラム情報

- **プログラム ID**: `COCRDLIC`
- **作成者**: AWS
- **タイプ**: CICS COBOL, VSAM, BMS
- **トランザクション ID**: `CCLI`
- **マップセット**: `COCRDLI`
- **マップ名**: `CCRDLIA`

## 3. 入出力定義

### 3.1. 画面 (BMS)

- **マップセット**: `COCRDLI`
- **主要フィールド**:
  - **検索条件**: `ACCTSIDI` (Account ID), `CARDSIDI` (Card Number - フィルタ用)。
  - **一覧表示 (配列)**: 最大 7 件まで表示可能。
    - `CRDSEL1` ~ `CRDSEL7`: 選択フィールド ('S': 詳細, 'U': 更新)。
    - `ACCTNO1` ~ `ACCTNO7`: アカウント ID。
    - `CRDNUM1` ~ `CRDNUM7`: カード番号。
    - `CRDSTS1` ~ `CRDSTS7`: ステータス。

### 3.2. VSAM ファイル

- **CARDDAT**: クレジットカード情報のマスターファイル。
- **CARDAIX**: Account ID をキーにしてカードを検索するための Alternate Index (Path)。

### 3.3. COMMAREA

- **ページング制御**:
  - `WS-CA-FIRST-CARDKEY`: 現在のページの一番上のキー（前ページへ戻る用）。
  - `WS-CA-LAST-CARDKEY`: 現在のページの一番下のキー（次ページへ進む用）。
  - `WS-CA-SCREEN-NUM`: 現在のページ番号。

## 4. 処理ロジック詳細

### 4.1. 初期表示 (MAIN-PARA)

- メニュー (`COMEN01C`) や他のプログラムから遷移してきた場合、COMMAREA の内容を確認。
- アカウント ID が指定されていれば、そのアカウントに紐づくカードを検索して表示。
- 管理者の場合、検索条件なしであれば全件表示を試みる（`CARDDAT` の直接スキャン）。

### 4.2. 一覧取得 (9000-READ-FORWARD / 9100-READ-BACKWARDS)

- **前方スクロール (F8)**:
  - `STARTBR` (Start Browse) を実行。キーは `CARDAIX` (Account ID 順) または `CARDDAT` (Card Number 順)。
  - `READNEXT` で順次読み込み、画面配列 (7件分) を埋める。
  - 読み込んだ最後のレコードのキーを `WS-CA-LAST-CARDKEY` に保存。
- **後方スクロール (F7)**:
  - `READPREV` を使用して前のページのデータを取得するロジック（または開始キーを調整して再検索）。

### 4.3. 画面遷移 (EVALUATE TRUE)

- **詳細表示 ('S')**:
  - リストで 'S' が入力された行のカード情報を COMMAREA にセット。
  - `COCRDSLC` (Credit Card Detail) へ `XCTL`。
- **更新 ('U')**:
  - リストで 'U' が入力された行のカード情報を COMMAREA にセット。
  - `COCRDUPC` (Credit Card Update) へ `XCTL`。

## 5. エラーハンドリング

- **検索エラー**: 条件に合致するレコードがない場合、「NO RECORDS FOUND」を表示。
- **選択エラー**: 複数行を選択した場合や、無効な文字を入力した場合のエラーチェック。

## 6. 特記事項

- **フィルタリング**: アカウント ID だけでなく、カード番号によるフィルタリングも実装されている。
- **ページング**: 標準的な CICS のブラウズ処理 (Start/ReadNext) を実装。

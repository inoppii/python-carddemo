# COACTVWC 詳細設計書

## 1. 概要

`COACTVWC` は、アカウント (口座) 情報の照会を行う CICS オンラインプログラムです。ユーザーが指定したアカウント ID に基づき、VSAM ファイルから口座情報および関連する顧客情報を取得して表示します。

## 2. プログラム情報

- **プログラム ID**: `COACTVWC`
- **作成者**: AWS
- **タイプ**: CICS COBOL, VSAM, BMS
- **トランザクション ID**: `CAVW`
- **マップセット**: `COACTVW`
- **マップ名**: `CACTVWA`

## 3. 入出力定義

### 3.1. 画面 (BMS)

- **マップセット**: `COACTVW`
- **主要フィールド**:
  - `ACCTSIDI` (入力): 検索対象のアカウント ID (Account ID)。
  - **出力フィールド**:
    - アカウント情報: `ACSTTUSO` (Status), `ACURBALO` (Current Balance), `ACRDLIMO` (Credit Limit) 等。
    - 顧客情報: `ACSTNUMO` (Customer ID), `ACSTSSNO` (SSN), `ACSFNAMO` (Full Name) 等。

### 3.2. VSAM ファイル

- **ACCTDAT** (Account Master): 口座情報の詳細。キーは Acct ID。
- **CUSTDAT** (Customer Master): 顧客情報の詳細。キーは Cust ID。
- **CXACAIX** (Card Cross Reference - Path): `CARDDAT` の Alternate Index。Account ID から Customer ID や Card Number を引くために使用。

## 4. 処理ロジック詳細

### 4.1. 初期表示 (MAIN-PARA)

- トランザクション起動時、COMMAREA を確認。
- 前画面から検索条件 (`CC-ACCT-ID`) が渡されている場合、即座に検索処理を実行 (`9000-READ-ACCT`)。
- 渡されていない場合、検索条件入力待ち状態とする。

### 4.2. 検索処理 (PROCESS-INPUTS -> READ-ACCT)

1. **入力検証**:
   - アカウント ID が数値 11桁であることをチェック。
2. **クロスリファレンス検索 (9200-GETCARDXREF-BYACCT)**:
   - `CXACAIX` (Path) を Account ID で検索。
   - 関連する Customer ID (`XREF-CUST-ID`) と Card Number を取得。
   - レコードが存在しない場合、エラーを表示。
3. **アカウント情報取得 (9300-GETACCTDATA-BYACCT)**:
   - `ACCTDAT` を Account ID で検索。
   - 口座詳細（残高、限度額、開設日など）を取得。
4. **顧客情報取得 (9400-GETCUSTDATA-BYCUST)**:
   - 手順2で取得した Customer ID をキーに `CUSTDAT` を検索。
   - 顧客詳細（氏名、住所、SSNなど）を取得。
5. **画面表示**:
   - 取得した情報を画面項目にセットし、`SEND MAP` で表示。

## 5. エラーハンドリング

- **検索エラー**: 該当するアカウントが存在しない場合 (VSAM `NOTFND`)、エラーメッセージを表示。
- **入力エラー**: アカウント ID の形式不正などに対し警告を表示。

## 6. 特記事項

- アカウント ID だけでは顧客を特定できないため、まず `CXACAIX` (Alternate Index) を経由して顧客 ID を特定する「逆引き」ロジックが実装されている。

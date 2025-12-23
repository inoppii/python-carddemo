# COPAUS2C 詳細設計書

## 1. 概要

`COPAUS2C` は、承認取引を不正 (Fraud) としてマークする、またはマークを解除するための CICS オンラインプログラムです。`COPAUS1C` から `EXEC CICS LINK` で呼び出され、IMS データベース上の承認レコードの更新と、DB2 テーブル (`AUTHFRDS`) への監査記録の追加・更新を行います。

## 2. プログラム情報

- **プログラム ID**: `COPAUS2C`
- **作成者**: AWS
- **タイプ**: CICS COBOL, IMS, DB2
- **機能**: 不正データ更新 (Mark Authorization Message Fraud)

## 3. 入出力定義

### 3.1. COMMAREA (入力/出力)

- 親プログラム (`COPAUS1C`) から受け取るデータ構造。
- **入力**:
  - `WS-ACCT-ID`: アカウント ID
  - `WS-CUST-ID`: 顧客 ID
  - `WS-FRAUD-AUTH-RECORD`: 不正対象の承認レコード詳細 (IMSセグメントレイアウト)
  - `WS-FRD-ACTION`: アクションフラグ ('F': Report Fraud, 'R': Remove Fraud)
- **出力**:
  - `WS-FRD-UPDATE-STATUS`: 更新結果 ('S': Success, 'F': Failed)
  - `WS-FRD-ACT-MSG`: 結果メッセージ

### 3.2. IMS データベース (参照のみ)

- 本プログラム自体は IMS 更新を行わない (親プログラムがハンドルする場合が多い) か、あるいは設計上は DB2 のみを担当しているように見える。
- *注記*: ソースコード上、IMS 関連の記述 (DLI コマンド) が見当たらない場合、このプログラムは純粋に DB2 側の「不正履歴」を管理する役割である可能性が高い。IMS 側の `PA-FRAUD-CONFIRMED` フラグ更新は呼び出し元の `COPAUS1C` が行っていると推測される。

### 3.3. DB2 テーブル (更新)

- **テーブル名**: `CARDDEMO.AUTHFRDS`
- **用途**: 不正として報告された承認取引の履歴管理。
- **主要カラム**:
  - `CARD_NUM`: カード番号
  - `AUTH_TS`: 承認タイムスタンプ
  - `AUTH_FRAUD`: 不正状態 ('F' or 'R' or ' ')
  - `FRAUD_RPT_DATE`: 報告日
  - その他取引詳細 (金額、加盟店、結果コード等)

## 4. 処理ロジック詳細

### 4.1. メイン処理 (MAIN-PARA)

1. **初期設定**:
   - `CICS ASKTIME` / `FORMATTIME` で現在日時を取得。
   - COMMAREA から受け取った承認レコードのタイムスタンプ等を DB2 用フォーマットに変換。
   - SQL 用ホスト変数への転送。

2. **DB2 登録/更新 (INSERT/UPDATE)**:
   - **INSERT 試行**:
     - まず `INSERT INTO CARDDEMO.AUTHFRDS` を実行し、新規レコードとして登録を試みる。
     - 成功 (`SQLCODE = 0`) した場合は、処理ステータスを「成功 (`S`)」に設定して終了。
   - **重複時の UPDATE**:
     - INSERT が一意制約違反 (`SQLCODE = -803`) で失敗した場合、既にレコードが存在するとみなす。
     - `UPDATE CARDDEMO.AUTHFRDS` を実行し、該当レコードのステータス (`AUTH_FRAUD`) と報告日 (`FRAUD_RPT_DATE`) を更新する (`FRAUD-UPDATE` ラベル)。
   - **エラー処理**:
     - その他の SQL エラーが発生した場合、処理ステータスを「失敗 (`F`)」とし、SQL コードとステートをメッセージに設定する。

### 4.2. 終了処理

- `EXEC CICS RETURN` で呼び出し元 (`COPAUS1C`) へ制御を戻す。
- トランザクションのコミットやロールバックは、通常呼び出し元 (Link元) の同期点管理 (Syncpoint) に委ねられる。

## 5. エラーハンドリング

- **DB2 エラー**: SQL エラー発生時、`WS-FRD-ACT-MSG` に "SYSTEM ERROR DB2: CODE:..." の形式で詳細をセットし、親プログラムへ通知する。

## 6. 特記事項

- **データ整合性**: IMS (運用データ) と DB2 (分析/履歴データ) の整合性を保つため、このプログラムの実行は親プログラムのトランザクション内で行われる必要がある。
- **タイムスタンプ**: IMS のタイムスタンプ書式と DB2 の `TIMESTAMP` 型の変換ロジックが含まれている。

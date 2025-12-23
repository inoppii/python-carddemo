# COPAUS1C 詳細設計書

## 1. 概要

`COPAUS1C` は、特定の承認リクエストの詳細情報を表示する CICS オンラインプログラムです。`COPAUS0C` (一覧画面) から選択された承認レコードの詳細を IMS データベースから取得し、画面に表示します。また、表示された取引に対して「不正 (Fraud)」フラグを設定する機能 (`COPAUS2C` への連携) も提供する可能性があります。

## 2. プログラム情報

- **プログラム ID**: `COPAUS1C`
- **作成者**: AWS
- **タイプ**: CICS COBOL, IMS, BMS
- **トランザクション ID**: `CPVD` (View Detail)
- **マップセット**: `COPAU01`
- **マップ名**: `COPAU1A`

## 3. 入出力定義

### 3.1. 画面 (BMS)

- **マップセット**: `COPAU01`
- **主要フィールド (出力)**:
  - 日時 (`AUTHDTO`, `AUTHTMO`)
  - 承認金額 (`AUTHAMTO`)
  - 結果コード/理由 (`AUTHRSPO`, `AUTHRSNO`)
  - カード情報 (`CARDNUMO`, `CRDEXPO`)
  - 加盟店情報 (`MERNAMEO`, `MERIDO`, `MERCITYO` 等)
  - 不正フラグ状態 (`AUTHFRDO`)
- **主要フィールド (入力)**:
  - 特になし (主に表示専用、PF キーによる操作)

### 3.2. IMS データベース

- **PSB**: `PSBPAUTB`
- **セグメント**:
  - `PAUTSUM0` (ルート): アカウント検索用。
  - `PAUTDTL1` (子供): 詳細情報取得用。検索キーは承認キー (`PA-AUTHORIZATION-KEY`)。

### 3.3. COMMAREA (共通領域)

- **入力**:
  - `CDEMO-ACCT-ID`: アカウント ID
  - `CDEMO-CPVS-PAU-SELECTED`: 選択された承認キー
- **出力**:
  - 不正設定用の連携データ (`CDEMO-CPVD-FRAUD-DATA`)

## 4. 処理ロジック詳細

### 4.1. 初期化・メイン処理 (MAIN-PARA)

1. `EIBCALEN` チェック。
2. COMMAREA を受信。
3. **データ取得 & 表示 (PROCESS-ENTER-KEY)**:
   - COMMAREA 内の `CDEMO-ACCT-ID` と `CDEMO-CPVS-PAU-SELECTED` (承認キー) を検証。
   - `DLI GU` でルートセグメント (`PAUTSUM0`) を取得。
   - `DLI GNP` で指定された承認キーを持つ子セグメント (`PAUTDTL1`) を特定 (`WHERE (PAUT9CTS = PA-AUTHORIZATION-KEY)` か、またはループで探索)。
   - 取得した IMS セグメントの内容を BMS マップの各フィールドへ転送 (`POPULATE-AUTH-DETAILS`)。
   - 承認理由コード (`PA-AUTH-RESP-REASON`) をメッセージテキストに変換して表示 (例: `0000` -> "APPROVED", `4100` -> "INSUFFICNT FUND")。
   - `SEND-AUTHVIEW-SCREEN` で画面送信。

### 4.2. ユーザー操作対応 (RECEIVE-AUTHVIEW-SCREEN 後)

- **PF3 (戻る)**:
  - 呼び出し元プログラム (`COPAUS0C`) へ戻るため、`XCTL` を発行。
  - プログラム名: `WS-PGM-AUTH-SMRY` (`COPAUS0C`)。
- **PF5 (不正フラグ切替)**:
  - 表示中の取引を不正 (Fraud) または非不正としてマークする。
  - `MARK-AUTH-FRAUD` ルーチンを実行。
  - サブルーチンまたは別プログラム (`COPAUS2C`/`WS-PGM-AUTH-FRAUD`) を `LINK` で呼び出し、更新処理を委譲。
  - 更新成功後、画面を再表示してステータス (`AUTHFRDO`) を更新 (例: "FRAUD CONFIRMED" 等を表示)。
- **PF8 (次へ)**:
  - 次の承認詳細へ進む (`PROCESS-PF8-KEY`)。
  - IMS 上で次の子セグメント (`DLI GNP`) を取得し、画面を更新。

## 5. エラーハンドリング

- **IMS エラー**: セグメントが見つからない場合、システムエラーメッセージを表示。
- **無効な遷移**: 必要なキー情報が COMMAREA にない場合、エラーとして戻る。

## 6. 特記事項

- **不正フラグ連携**: 不正フラグの管理はビジネス上重要であり、IMS データ (`PA-FRAUD-CONFIRMED` フラグ) の更新と同時に、監査テーブル (DB2) への記録も行われる可能性がある (連携先プログラムの責任)。
- **日付フォーマット**: 画面表示用に `YY/MM/DD` や `MM/DD/YY` 等の変換ロジックを含む。

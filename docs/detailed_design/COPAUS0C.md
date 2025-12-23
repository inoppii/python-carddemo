# COPAUS0C 詳細設計書

## 1. 概要

`COPAUS0C` は、承認リクエストの履歴を一覧表示 (サマリー照会) する CICS オンラインプログラムです。IMS データベースから顧客の過去の承認履歴を取得し、BMS マップを用いて画面に一覧表示します。ユーザーは詳細を確認したい取引を選択することができます。

## 2. プログラム情報

- **プログラム ID**: `COPAUS0C`
- **作成者**: AWS
- **タイプ**: CICS COBOL, IMS, BMS
- **トランザクション ID**: `CPVS` (View Summary)
- **マップセット**: `COPAU00`
- **マップ名**: `COPAU0A`

## 3. 入出力定義

### 3.1. 画面 (BMS)

- **マップセット**: `COPAU00`
- **主要フィールド**:
  - アカウント ID (`ACCTSID`): 入力/表示
  - 取引リスト (配列): 日付、時刻、金額、店舗名、承認結果など
  - 選択フィールド (`SEL0001` - `SEL000x`): 詳細遷移用の選択フラグ
  - ページング情報: 現在ページ、次ページ有無

### 3.2. IMS データベース

- **PSB**: `PSBPAUTB`
- **セグメント**:
  - `PAUTSUM0` (ルート): アカウントサマリー。`ACCNTID` (アカウントID) で検索。
  - `PAUTDTL1` (子供): 承認明細。`PAUT9CTS` (タイムスタンプ) 等で検索。

### 3.3. COMMAREA (共通領域)

- **入力**:
  - `CDEMO-FROM-TRANID`: 呼び出し元トランザクションID
  - `CDEMO-FROM-PROGRAM`: 呼び出し元プログラムID
  - `CDEMO-ACCT-ID`: 対象アカウントID
  - `CDEMO-PGM-CONTEXT`: ページング制御用コンテキスト
- **出力**:
  - 選択された明細のキー情報 (`CDEMO-CPVS-AUTH-KEYS`)
  - 次画面への遷移情報

## 4. 処理ロジック詳細

### 4.1. メイン処理 (MAIN-PARA)

1. **初期表示 (First Entry)**:
   - `EIBCALEN = 0` の場合。
   - `SYSTEM-DT` より現在日時を取得。
   - 初期画面を表示する (`SEND-PAGNUM-SCREEN`)。
2. **再入時 (Re-entry)**:
   - `EIBCALEN > 0` の場合。
   - COMMAREA を復元。
   - ユーザー入力キー (`EIBAID`) に応じて分岐。
     - **Enter**: 入力値検証、検索実行、または詳細画面へ遷移。
     - **PF3 / PF12**: メニューまたは前画面へ戻る (`RETURN-TO-PREV-SCREEN`)。
     - **PF7 / PF8**: 前ページ / 次ページへのスクロール処理 (`PROCESS-PAGE-BACKWARD`, `PROCESS-PAGE-FORWARD`)。
     - **Clear**: 画面クリア。

### 4.2. 検索・一覧表示 (PROCESS-ENTER-KEY, DISPLAY-AUTH-PAGE)

1. ユーザーが入力したアカウント ID (`CDEMO-ACCT-ID`) を取得。
2. **IMS 検索**:
   - `DLI GU` (Get Unique): ルートセグメント `PAUTSUM0` を `ACCNTID` で検索。
   - 見つからない場合、「アカウントが存在しない」旨のエラーメッセージを表示。
   - `DLI GNP` (Get Next Within Parent): 子セグメント `PAUTDTL1` を順次読み込み。
   - 一度の表示件数 (10〜15件程度) 分だけ配列に格納し、画面マップに出力。
   - 次のページがある場合はフラグ (`CDEMO-CPVS-NEXT-PAGE-FLG`) を設定。

### 4.3. 詳細遷移 (PROCESS-ENTER-KEY)

- 一覧画面で任意の行の「選択」フィールド (`SEL000x`) に文字が入力された場合。
- 選択された行に対応する承認キー (`PA-AUTHORIZATION-KEY`) を COMMAREA に設定。
- `XCTL` コマンドで詳細照会プログラム `COPAUS1C` へ制御を移行。
  - プログラム名: `COPAUS1C` (定数 `WS-PGM-AUTH-DTL` より)

### 4.4. ページング制御

- **前方スクロール (PF8)**:
  - COMMAREA に保存された「現在の最後のキー」を使用し、IMS データベースの読み込み開始位置を調整。
- **後方スクロール (PF7)**:
  - ページ履歴配列 (`CDEMO-CPVS-PAUKEY-PREV-PG`) から前のページの開始キーを取得し、再検索を行う。

## 5. エラーハンドリング

- **IMS エラー**: DB 利用不可、セグメント不在 (`GE`) などのステータスコード (`DIBSTAT`) をチェックし、画面最下部のメッセージ領域にエラーコードを表示。
- **入力エラー**: アカウント ID が未入力、数値以外の場合、エラーメッセージを表示して再入力を促す。
- **不正なキー操作**: 未定義の PF キーが押された場合、「Invalid Key」メッセージを表示。

## 6. 特記事項

- **ナビゲーション**: メニュー画面 (`COMEN01C`) から呼ばれること、および詳細画面 (`COPAUS1C`) へ遷移することを想定。
- **データ表示**: 承認結果 (Approve/Decline) を色分けやコード (`A`/`D`) で視覚的に区別するロジックが含まれる。

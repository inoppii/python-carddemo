# CORPT00C 詳細設計書

## 1. 概要

`CORPT00C` は、オンライン画面からバッチジョブを投入 (Submit) して、取引レポートを作成するための CICS プログラムです。ユーザーはレポートの種類（月次、年次、期間指定）を選択し、JCL テンプレートに必要なパラメータを埋め込んで、CICS の TDQ (Transient Data Queue) 経由でジョブを実行します。

## 2. プログラム情報

- **プログラム ID**: `CORPT00C`
- **作成者**: AWS
- **タイプ**: CICS COBOL, TDQ, JCL Submission
- **トランザクション ID**: `CR00`
- **マップセット**: `CORPT00`
- **マップ名**: `CORPT0A`

## 3. 入出力定義

### 3.1. 画面 (BMS)

- **主要フィールド**:
  - `MONTHLYI`, `YEARLYI`, `CUSTOMI`: レポートタイプの選択。
  - `SDTMMI`, `SDTDDI`, `SDTYYYYI`: 開始日（カスタム指定時）。
  - `EDTMMI`, `EDTDDI`, `EDTYYYYI`: 終了日（カスタム指定時）。
  - `CONFIRMI`: ジョブ投入の最終確認。

### 3.2. TDQ (Transient Data Queue)

- **JOBS**: 内部読込装置 (Internal Reader) に接続された Extra-partition TDQ。ここに JCL 行を書き出すことでジョブがサブミットされる。

## 4. 処理ロジック詳細

### 4.1. パラメータ設定 (`PROCESS-ENTER-KEY`)

- **月次/年次**: 現在日付から月初・月末、あるいは年初・年末を自動計算。
- **カスタム**: ユーザー入力の日付をバリデーションサブプログラム (`CSUTLDTC`) でチェック。

### 4.2. ジョブ投入処理 (`SUBMIT-JOB-TO-INTRDR`)

1. **JCL 構築**: プログラム内に定義された `JOB-DATA` (JCL 雛形) の `PARM-START-DATE`, `PARM-END-DATE` 箇所を入力値で置換。
2. **TDQ 書き込み (`WIRTE-JOBSUB-TDQ`)**:
    - `EXEC CICS WRITEQ TD QUEUE('JOBS')` をループ実行し、JCL 各行をキューへ出力。
    - これにより、OS レベルの Job Entry System (JES) にジョブが渡される。

## 5. エラーハンドリング

- 不正な日付形式の入力チェック。
- TDQ への書き込み失敗時のエラーハンドリング。

## 6. 特記事項

- 「オンラインからバッチをキックする」メインフレーム特有のパターンを実装している。
- 実際のレポート作成（データ抽出とフォーマット）は、ここで投入されたバッチプログラム（`TRANREPT` 等）側で行われる。
- JCL 内で `JCLLIB` を指定し、共通の `PROC` を呼び出す構成となっている。

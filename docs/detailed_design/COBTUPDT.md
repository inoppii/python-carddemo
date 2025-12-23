# COBTUPDT 詳細設計書

## 1. 概要

- **プログラムID**: COBTUPDT
- **論理層**: Business Logic (Batch)
- **機能**: 順編成ファイル入力に基づき、トランザクションタイプマスタを一括更新(追加・変更・削除)します。

## 2. 入出力

### 入力

- **ファイル**: `TR-RECORD` (DD名: `INPFILE`)
  - 形式: 順編成 (Sequential)
  - レコード長: 80バイト (推定)
  - レイアウト:
    - 処理区分 (1桁): `A`(Add), `U`(Update), `D`(Delete)
    - トランザクションタイプ (2桁)
    - 説明 (50桁)

### 出力

- **データベース更新**: `TRANSACTION_TYPE` テーブル
- **SYSOUT/DISPLAY**: 処理件数、エラーメッセージ、実行ログ

## 3. 外部仕様

### ファイル

- **INPFILE**: 入力トランザクションファイル

### データベース

- **テーブル**: `CARDDEMO.TRANSACTION_TYPE`
  - `INSERT`
  - `UPDATE`
  - `DELETE`

## 4. 主要ロジック

### メインループ (`1001-READ-NEXT-RECORDS`)

- ファイル末尾 (`LASTREC = 'Y'`) までループ処理。
- 1レコード読み込むごとに `1003-TREAT-RECORD` を呼び出す。

### レコード処理 (`1003-TREAT-RECORD`)

- **処理区分 (`INPUT-REC-TYPE`)** による分岐:
  - `'A'`: `10031-INSERT-DB` を呼び出し。
    - `INSERT INTO TRANSACTION_TYPE ...`
    - 重複エラー時はエラーメッセージを出力して継続(またはAbend)。
  - `'U'`: `10032-UPDATE-DB` を呼び出し。
    - `UPDATE TRANSACTION_TYPE SET ... WHERE TR_TYPE = ...`
    - 対象不在時 (SQLCODE +100) はエラー扱い。
  - `'D'`: `10033-DELETE-DB` を呼び出し。
    - `DELETE FROM TRANSACTION_TYPE WHERE ...`
  - `'*'`: コメント行として無視。
  - その他: エラーメッセージを出力して Abend (`9999-ABEND`)。

### エラーハンドリング

- SQL エラー発生時は `WS-RETURN-MSG` に詳細を編集し、`9999-ABEND` を呼び出してジョブを異常終了させる (Return Code 4 以上を設定)。
- 正常終了時は Return Code 0。

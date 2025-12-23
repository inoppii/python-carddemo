# CardDemo システム 基本設計書（関連システムインターフェース編）

## 1. 概要

本書は、CardDemo システムが外部システムや他コンポーネントとデータを交換するためのインターフェース仕様を定義します。リアルタイムのメッセージング連携およびファイルベースのバッチ連携を網羅します。

## 2. リアルタイム連携 (IMS/MQ)

承認機能において、外部の承認エンジンや他決済ネットワークと連携するためのインターフェースです。

### 2.1. メッセージフロー

1. **要求送信**: オンライン画面 (`COPAUA0C`) から、承認要求メッセージを MQ キューに送出。
2. **非同期処理**: IMS 側でメッセージを受信し、承認判定を実施。
3. **結果受信**: オンライン側で MQ キューから判定結果を読み取り、画面に反映。

### 2.2. 主要コンポーネント

- **MQSeries**: メッセージの運搬を担うミドルウェア。
- **COPAUA0C**: CICS 側の要求/応答制御プログラム。

## 3. バッチ連携 (Sequential Files)

バッチプログラム間、および外部とのデータ授受に使用されるフラットファイルの仕様です。

### 3.1. 授受ファイル一覧

| ファイル物理名 | 形式 | LRECL | 説明 |
| :--- | :--- | :--- | :--- |
| `DALYTRAN.PS` | FB | 350 | 日次取引入力データ |
| `DALYREJS.PS` | FB | 430 | バリデーションエラーによる却下データ |
| `EXPFILE.PS` | FB | 500 | 拠点移行用統合エクスポートファイル |
| `REPTFILE.PS` | FB | 133 | 印刷用取引レポート出力 |

## 4. プロトコル・方式

- **文字コード**: EBCDIC (メインフレーム環境内)
- **転送方式**: FTP/SFTP (外部送信時、`FTPJCL.JCL` を使用)
- **エラー通知**: バッチジョブの戻り値 (Cond Code) および SYSOUT へのログ出力により連携。

---
[概要編](file:///Users/inohara/Documents/antigravity-demo/aws-mainframe-modernization-carddemo/docs/BasicDesign.md) | [オンライン処理編](file:///Users/inohara/Documents/antigravity-demo/aws-mainframe-modernization-carddemo/docs/BasicDesign_Online.md) | [バッチ処理編](file:///Users/inohara/Documents/antigravity-demo/aws-mainframe-modernization-carddemo/docs/BasicDesign_Batch.md) | [データベース設計編](file:///Users/inohara/Documents/antigravity-demo/aws-mainframe-modernization-carddemo/docs/BasicDesign_Database.md) | [運用管理編](file:///Users/inohara/Documents/antigravity-demo/aws-mainframe-modernization-carddemo/docs/BasicDesign_Operations.md)

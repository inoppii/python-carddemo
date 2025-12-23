# CardDemo システム 基本設計書（関連システムインターフェース編）

## 1. 概要

本書は、Google Cloud 上に移行された CardDemo システムの外部連携およびコンポーネント間連携仕様を定義します。旧システムの MQSeries は Cloud Pub/Sub に、FB ファイル連携は Cloud Storage (GCS) に置き換えます。

## 2. リアルタイム連携 (Cloud Pub/Sub)

承認機能において、外部の承認エンジンや他コンポーネントと非同期メッセージングを行うためのインターフェースです。

### 2.1. メッセージフロー

1. **要求送信**: オンライン API (`p_COPAUA0C.py`) が、承認要求メッセージを Pub/Sub トピック (`card-auth-request`) にパブリッシュします。
2. **非同期処理**: 外部システム（またはエミュレートされた承認サービス）がサブスクリプションを介して要求を受信。
3. **結果受信**: オンライン API が応答トピック (`card-auth-response`) から判定結果をプルまたはプッシュ（Webhook）で受信し、ステータスを更新します。

### 2.2. 主要コンポーネント

- **Cloud Pub/Sub**: メッセージ配信基盤。
- **p_COPAUA0C.py**: Python による要求/応答制御ロジック。

## 3. ファイルベース連携 (Cloud Storage)

バッチ処理の入力データや、他システムへの出力ファイルに使用するインターフェースです。

### 3.1. 授受バケット・オブジェクト一覧

| 旧ファイル物理名 | GCS オブジェクトパス | 形式 | 説明 |
| :--- | :--- | :--- | :--- |
| `DALYTRAN.PS` | `gs://carddemo-data/input/daily_trans.csv` | CSV / JSON | 日次取引入力データ |
| `DALYREJS.PS` | `gs://carddemo-data/output/rejected_trans.csv` | CSV / JSON| バリデーションエラー却下データ |
| `EXPFILE.PS` | `gs://carddemo-data/output/export_all.json` | JSON | 拠点移行用統合データ |
| `REPTFILE.PS` | `gs://carddemo-data/reports/trans_report.txt` | Text | 印刷用取引レポート出力 |

## 4. プロトコル・方式

- **文字コード**: UTF-8 (統一)
- **転送方式**: Google Cloud Client Library (Python) または `gsutil` / `gcloud storage` コマンド。
- **データ形式**: メインフレーム時代の固定長形式から、可読性の高い CSV または JSON へ移行します。

---
[概要編](file:///Users/inohara/Documents/antigravity-demo/python-carddemo/docs/p_BasicDesign.md) | [オンライン処理編](file:///Users/inohara/Documents/antigravity-demo/python-carddemo/docs/p_BasicDesign_Online.md) | [バッチ処理編](file:///Users/inohara/Documents/antigravity-demo/python-carddemo/docs/p_BasicDesign_Batch.md) | [データベース設計編](file:///Users/inohara/Documents/antigravity-demo/python-carddemo/docs/p_BasicDesign_Database.md)

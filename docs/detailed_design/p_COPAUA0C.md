# p_COPAUA0C 詳細設計書

## 1. 概要

`p_COPAUA0C.py` は、Cloud Pub/Sub を通じてカード承認リクエストを受信し、判定結果を応答する非同期メッセージング処理プログラムです。旧システムの `COPAUA0C` (CICS/MQ/IMS) の機能を、Google Cloud のマネージドサービスおよび PostgreSQL 環境で再実装します。

## 2. プログラム情報

- **プログラム ID**: `p_COPAUA0C.py`
- **言語**: Python 3.10+
- **接続DB**: Cloud SQL for PostgreSQL
- **主要モジュール**: `google-cloud-pubsub`, `SQLAlchemy`, `pydantic`

## 3. 入出力定義

### 3.1. メッセージ (Cloud Pub/Sub)

- **Input Subscription**: `card-auth-request-sub`
- **Output Topic**: `card-auth-response`
- **メッセージ形式**: JSON (旧 MQ の CSV 形式から移行)
  - `card_num`, `amount`, `expiry_date`, `merchant_id`, `trans_id`

### 3.2. Database (PostgreSQL)

- **マスタテーブル**: `card_xref`, `accounts`, `customers` (旧 VSAM 相当)
- **履歴・累計テーブル**: `auth_summaries`, `auth_details` (旧 IMS セグメント相当)

## 4. 処理ロジック詳細

### 4.1. 受信・解析

1. Pub/Sub サブスクリプションからメッセージをプル (またはプッシュで起動)。
2. JSON ペイロードを Pydantic モデルでバリデーション。

### 4.2. 承認判定 (Auth Logic)

1. **マスタ検証**:
    - カード、アカウント、顧客の存在および有効性を PostgreSQL 上で結合検索または順次検索して確認。
2. **利用可能枠確認**:
    - `auth_summaries` テーブル（旧 IMS ルート相当）から現在の承認済み累計額を取得。
    - アカウントの `acct_limit - acct_curr_bal - (承認済み額)` により、リアルタイムの利用可能枠を算出。
3. **判定**:
    - 枠内であれば `approve`、不足していれば `decline` (理由コード付き) を決定。

### 4.3. 応答・記録 (トランザクション管理)

1. **DB 更新**:
    - `auth_summaries` の累計額を更新。
    - `auth_details` に今回の取引結果を記録。
2. **メッセージ送信**:
    - 判定結果を JSON 形式で応答トピックにパブリッシュ。
3. **Acknowledge**:
    - メッセージの処理完了を Pub/Sub に通知 (Ack)。

## 5. エラーハンドリング

- **メッセージ形式不正**: Ack せず（またはデッドレターキューへ移動し）エラーログを出力。
- **DB 接続エラー**: 一時的なエラーの場合はリトライ、永続的な場合はエラー応答を試みた後に Ack。

---
[関連システムインターフェース編](file:///Users/inohara/Documents/antigravity-demo/python-carddemo/docs/p_BasicDesign_Interface.md)

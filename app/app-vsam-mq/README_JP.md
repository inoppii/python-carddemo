# MQ と VSAM を使用したアカウント抽出 - CardDemo 拡張機能

![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)
![License](https://img.shields.io/badge/license-Apache%202.0-green.svg)

## 概要

アカウント抽出モジュールは、VSAM と IBM MQ 間の統合を示す CardDemo アプリケーションのオプションの拡張機能です。このモジュールにより、MQ チャネルを通じたアカウントデータの抽出と送信が可能になり、メインフレーム環境で一般的に使用される非同期処理パターンが示されます。

## 目次

- [機能](#機能)
- [コンポーネント](#コンポーネント)
- [インストール](#インストール)
- [使用方法](#使用方法)
- [技術詳細](#技術詳細)
- [依存関係](#依存関係)

## 機能

この拡張機能は以下の機能を提供します：

- **MQ によるシステム日付照会**: MQ リクエスト/レスポンスパターンを通じたシステム日付の照会 (CDRD トランザクション)
- **MQ によるアカウント詳細照会**: MQ チャネルを通じたアカウント情報の取得 (CDRA トランザクション)
- **非同期処理**: システム間の非同期通信パターンを示します
- **MQ 統合**: MQ を既存の VSAM ベースのアプリケーションと統合する方法を示します

## コンポーネント

### オンラインコンポーネント

| トランザクション | プログラム | 機能 | 備考 |
|:---|:---|:---|:---|
| CDRD | CODATE01 | MQ によるシステム日付照会 | MQ リクエスト/レスポンスパターンのデモ |
| CDRA | COACCT01 | MQ によるアカウント詳細照会 | MQ リクエスト/レスポンスパターンのデモ |

### ディレクトリ構造

- **cbl/**: MQ 統合用の COBOL プログラム
- **csd/**: MQ トランザクション用の CICS リソース定義

## インストール

### 前提条件

- 基本となる CardDemo アプリケーションがインストールされ動作していること
- CICS からアクセス可能な IBM MQ が構成されていること
- MQ サポートを備えた CICS

### インストール手順

1. **MQ リソースの構成**
   - 必要な MQ キューを作成します：

     ```
     DEFINE QLOCAL('CARDDEMO.REQUEST.QUEUE') REPLACE
     DEFINE QLOCAL('CARDDEMO.RESPONSE.QUEUE') REPLACE
     ```

2. **プログラムのコンパイル**
   - MQ サポートを使用して COBOL プログラムをコンパイルします

3. **CICS リソースの定義**
   - 提供された CSD 定義を使用して、トランザクションを CICS リージョンに追加します：

     ```
     DEFINE TRANSACTION(CDRD) GROUP(CARDDEMO) PROGRAM(CODATE01)
     DEFINE TRANSACTION(CDRA) GROUP(CARDDEMO) PROGRAM(COACCT01)
     ```

4. **CICS-MQ 接続の構成**
   - 必要な CICS-MQ 接続リソースを定義します：

     ```
     DEFINE MQCONN(MQ01) GROUP(CARDDEMO)
     DEFINE MQQUEUE(CARDREQ) GROUP(CARDDEMO) QNAME(CARDDEMO.REQUEST.QUEUE)
     DEFINE MQQUEUE(CARDRES) GROUP(CARDDEMO) QNAME(CARDDEMO.RESPONSE.QUEUE)
     ```

## 使用方法

### システム日付照会 (CDRD)

CDRD トランザクションは、システム日付を取得するための単純な MQ リクエスト/レスポンスパターンを示します：

1. CICS で CDRD トランザクションを実行します
2. トランザクションはリクエストキューにリクエストメッセージを送信します
3. リスナープログラムがリクエストを処理し、レスポンスキューにシステム日付を送信します
4. CDRD トランザクションはレスポンスを取得して表示します

### アカウント詳細照会 (CDRA)

CDRA トランザクションは、MQ を介してアカウント情報を取得する方法を示します：

1. アカウント番号を指定して CICS で CDRA トランザクションを実行します
2. トランザクションはアカウント番号を含むリクエストメッセージをリクエストキューに送信します
3. リスナープログラムが VSAM からアカウントの詳細を取得し、レスポンスキューに送信します
4. CDRA トランザクションはアカウント情報を取得して表示します

## 技術詳細

### メッセージ形式

**日付リクエストメッセージ形式:**

```
01 DATE-REQUEST-MSG.
   05 REQUEST-TYPE        PIC X(4) VALUE 'DATE'.
   05 REQUEST-ID          PIC X(8).
```

**日付レスポンスメッセージ形式:**

```
01 DATE-RESPONSE-MSG.
   05 RESPONSE-TYPE       PIC X(4) VALUE 'DATE'.
   05 RESPONSE-ID         PIC X(8).
   05 SYSTEM-DATE         PIC X(10).
```

**アカウントリクエストメッセージ形式:**

```
01 ACCT-REQUEST-MSG.
   05 REQUEST-TYPE        PIC X(4) VALUE 'ACCT'.
   05 REQUEST-ID          PIC X(8).
   05 ACCOUNT-NUMBER      PIC X(11).
```

**アカウントレスポンスメッセージ形式:**

```
01 ACCT-RESPONSE-MSG.
   05 RESPONSE-TYPE       PIC X(4) VALUE 'ACCT'.
   05 RESPONSE-ID         PIC X(8).
   05 ACCOUNT-DATA        PIC X(300).
```

### 統合パターン

この拡張機能は、いくつかの MQ 統合パターンを示します：

1. **リクエスト/レスポンス**: 非同期 MQ を使用して同期リクエスト/レスポンスパターンを実装する方法を示します
2. **メッセージ相関**: リクエストメッセージとレスポンスメッセージを相関させる方法を示します
3. **データ抽出**: MQ 経由で送信するために VSAM ファイルからデータを抽出する方法を示します
4. **エラー処理**: MQ 操作の適切なエラー処理が含まれます

## 依存関係

- 基本 CardDemo アプリケーション
- IBM MQ
- MQ サポートを備えた CICS

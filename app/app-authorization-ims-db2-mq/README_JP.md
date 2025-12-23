# CardDemo 拡張機能 - IMS, DB2, MQ を使用したクレジットカード承認

![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)
![License](https://img.shields.io/badge/license-Apache%202.0-green.svg)

## 概要

クレジットカード承認拡張機能は、IMS DB, DB2, および MQ テクノロジーを統合した包括的な承認処理システムで CardDemo を強化します。この拡張機能は、加盟店の最初のリクエストから承認/拒否の決定まで、不正検出機能を備えた実際のクレジットカード承認フローをシミュレートします。

## 目次

- [機能](#機能)
- [テクノロジー](#テクノロジー)
- [アーキテクチャ](#アーキテクチャ)
- [ビジネスロジック](#ビジネスロジック)
- [インストール](#インストール)
  - [前提条件](#前提条件)
  - [IMS データベースセットアップ](#ims-データベースセットアップ)
  - [DB2 テーブルセットアップ](#db2-テーブルセットアップ)
  - [プログラムコンパイル](#プログラムコンパイル)
  - [CICS リソース](#cics-リソース)
- [アプリケーションコンポーネント](#アプリケーションコンポーネント)
  - [プログラム](#プログラム)
  - [コピーブック](#コピーブック)
  - [CICS トランザクション](#cics-トランザクション)
  - [CICS 画面](#cics-画面)
  - [JCL](#jcl)
  - [IMS DB コンポーネント](#ims-db-コンポーネント)
  - [DB2 コンポーネント](#db2-コンポーネント)
  - [MQ 構成](#mq-構成)
- [データモデル](#データモデル)
  - [MQ メッセージ形式](#mq-メッセージ形式)
  - [IMS DB 構造](#ims-db-構造)
  - [DB2 スキーマ](#db2-スキーマ)
- [ユーザーインターフェース](#ユーザーインターフェース)
- [ライセンス](#ライセンス)

## 機能

この拡張機能は、CardDemo に以下の機能を追加します：

- MQ を介したリアルタイムのクレジットカード承認処理
- 承認リクエストの検証とビジネスルールの適用
- IMS 階層型データベースへの承認詳細の保存
- DB2 統合による不正検出とレポート
- IMS DB と DB2 にまたがる 2 フェーズコミットトランザクション
- 承認履歴の表示と管理
- 期限切れの承認のバッチパージ

## テクノロジー

クレジットカード承認拡張機能は以下を活用します：

- **COBOL**: コアビジネスロジックの実装
- **CICS**: トランザクション処理と画面管理
- **IMS DB**: 承認ストレージ用の階層型データベース
- **DB2**: 不正分析用のリレーショナルデータベース
- **MQ**: 承認リクエスト/レスポンス用のメッセージキューイング
- **VSAM**: アカウントおよび顧客データアクセス用

## アーキテクチャ

![Authorization Flow](../../diagrams/auth_flow.png "Authorization Flow Diagram")

*注: 図に示されている Cloud クライアントコンポーネントは、サンプルコードには含まれていません。指定された形式で承認リクエストを送信できる MQ 互換クライアントであればどれでも使用できます。*

## ビジネスロジック

承認拡張機能は、以下のビジネスプロセスを実装しています：

### 1. 承認処理

- クラウドベースの POS エミュレーターが MQ 経由で承認リクエストを送信
- MQ メッセージによってトリガーされた CICS プログラムがリクエストを処理
- VSAM 相互参照を介してアカウントと顧客データを取得
- リクエストを承認または拒否するビジネスルールを適用
- 返信 MQ キュー経由でレスポンスを送信
- 承認詳細を IMS データベースに保存

### 2. 承認管理

- アカウントと承認サマリーの表示
- 詳細な承認情報の確認
- 複数の承認間のナビゲート
- 不審なトランザクションを不正としてマーク
- 分析のために不正ケースを DB2 に保存

### 3. バッチ処理

- 期限切れの承認の日次パージ
- 不一致の承認が削除されたときの利用可能クレジットの調整

## インストール

### 前提条件

この拡張機能をインストールする前に、ベースとなる CardDemo アプリケーションをインストールする必要があります。この拡張機能を進める前に、[メインインストールガイド](../../README_JP.md#インストール)に従ってコアアプリケーションをセットアップしてください。

### IMS データベースセットアップ

クレジットカード承認拡張機能は、HIDAM IMS データベース構造を使用します。IMS データベース管理者と協力して以下を行ってください：

1. 提供された DBD を使用して必要な IMS データベースを作成します：
   - DBPAUTP0 (HIDAM プライマリデータベース)
   - DBPAUTX0 (HIDAM インデックス)

2. PSB をインストールします：
   - PSBPAUTB (BMP PSB)
   - PSBPAUTL (Load PSB)

DBD および PSB 定義は `app/app-authorization-ims-db2-mq/ims` ディレクトリに提供されています。

### DB2 テーブルセットアップ

以下の DB2 スクリプトを実行して、不正追跡に必要なテーブルとインデックスを作成します：

```sql
CREATE TABLE <<db2-schema>>.AUTHFRDS                   
(CARD_NUM              CHAR(16)    NOT NULL,
AUTH_TS                TIMESTAMP   NOT NULL,
AUTH_TYPE              CHAR(4)             ,
CARD_EXPIRY_DATE       CHAR(4)             ,
MESSAGE_TYPE           CHAR(6)             ,
MESSAGE_SOURCE         CHAR(6)             ,
AUTH_ID_CODE           CHAR(6)             ,
AUTH_RESP_CODE         CHAR(2)             ,
AUTH_RESP_REASON       CHAR(4)             ,
PROCESSING_CODE        CHAR(6)             ,
TRANSACTION_AMT        DECIMAL(12,2)       ,
APPROVED_AMT           DECIMAL(12,2)       ,
MERCHANT_CATAGORY_CODE CHAR(4)             ,
ACQR_COUNTRY_CODE      CHAR(3)             ,
POS_ENTRY_MODE         SMALLINT            ,
MERCHANT_ID            CHAR(15)            ,
MERCHANT_NAME          VARCHAR(22)         ,
MERCHANT_CITY          CHAR(13)            ,
MERCHANT_STATE         CHAR(02)            ,
MERCHANT_ZIP           CHAR(09)            ,
TRANSACTION_ID         CHAR(15)            ,
MATCH_STATUS           CHAR(1)             ,
AUTH_FRAUD             CHAR(1)             ,
FRAUD_RPT_DATE         DATE                ,
ACCT_ID                DECIMAL(11)         ,
CUST_ID                DECIMAL(9)          ,
PRIMARY KEY(CARD_NUM,AUTH_TS )             )
IN <<db2-database>>.AWSTSFRD;

CREATE UNIQUE INDEX <<db2-schema>>.XAUTHFRD           
ON <<db2-schema>>.AUTHFRDS                         
(CARD_NUM ASC, AUTH_TS DESC)             
USING STOGROUP <<db2-storage-group>>                     
COPY YES;
```

**重要**: プログラム `COPAUS2C.cbl` 内の DB2 スキーマ名を環境に合わせて更新してください。

### プログラムコンパイル

提供された JCL テンプレートを使用して COBOL プログラムをコンパイルします：

1. IMS DB アクセスのある CICS プログラムの場合：CICS-IMS コンパイル JCL を使用
2. DB2 アクセスのある CICS プログラムの場合：CICS-DB2 コンパイル JCL を使用
3. MQ 統合のある CICS プログラムの場合：CICS-MQ コンパイル JCL を使用
4. IMS DB アクセスのあるバッチプログラムの場合：BATCH-IMS コンパイル JCL を使用

### CICS リソース

ベースの CardDemo CICS リソースをインストールした後、承認拡張機能用の追加リソースを定義します：

1. プログラム、マップセット、およびトランザクションを定義します：

   ```
   DEF PROGRAM(COPAUA0C) GROUP(CARDDEMO)
   DEF MAPSET(COPAU00) GROUP(CARDDEMO)
   DEFINE PROGRAM(COPAUA0C) GROUP(CARDDEMO) DA(ANY) TRANSID(CP00) DESCRIPTION(Authorization Main Module)
   DEFINE TRANSACTION(CP00) GROUP(CARDDEMO) PROGRAM(COPAUA0C) TASKDATAL(ANY)
   ```

2. DB2 プランとトランザクションを定義します：

   ```
   DEF DB2ENTRY(DB201PLN) GROUP(CARDDEMO)
   DEF DB2TRAN(CPVDTRAN) ENTRY(DB201PLN) TRANSID(CPVD) GROUP(CARDDEMO)
   ```

3. CICS リージョンにリソースをインストールします：

   ```
   CEDA INSTALL TRANS(CP00) GROUP(CARDDEMO)
   CEDA INSTALL TRANS(CPVS) GROUP(CARDDEMO)
   CEDA INSTALL TRANS(CPVD) GROUP(CARDDEMO)
   CEDA INSTALL DB2ENTRY(DB201PLN) GROUP(CARDDEMO)
   CEDA INSTALL DB2TRAN(CPVDTRAN) GROUP(CARDDEMO)
   ```

4. プログラムに対して NEWCOPY を実行します：

   ```
   CEMT SET PROG(COPAUA0C) NEWCOPY
   CEMT SET PROG(COPAU0*) NEWCOPY  
   CEMT SET PROG(COPAUS*C) NEWCOPY 
   ```

## アプリケーションコンポーネント

クレジットカード承認拡張機能のすべてのコンポーネントは `app/app-authorization-ims-db2-mq` ディレクトリにあります。

### プログラム

| プログラム | タイプ | 説明 | トランザクション |
|:---|:---|:---|:---|
| COPAUA0C | CICS | 承認リクエストプロセッサ (MQ トリガー) | CP00 |
| COPAUS0C | CICS | 承認サマリー表示 | CPVS |
| COPAUS1C | CICS | 承認詳細表示 | CPVD |
| COPAUS2C | CICS | 不正マーキングおよび DB2 更新 | (呼び出し) |
| CBPAUP0C | Batch | 期限切れ承認パージ | N/A |

### コピーブック

| コピーブック | 説明 |
|:---|:---|
| CIPAUSMY | 保留中の承認サマリー IMS セグメント |
| CIPAUDTY | 保留中の承認詳細 IMS セグメント |
| CCPAURQY | 承認リクエスト構造 |
| CCPAURLY | 承認レスポンス構造 |
| CCPAUERY | 承認エラーログ |

### CICS トランザクション

| トランザクション | プログラム | 説明 |
|:---|:---|:---|
| CP00 | COPAUA0C | 承認リクエスト処理 (MQ トリガー) |
| CPVS | COPAUS0C | 承認サマリー表示 |
| CPVD | COPAUS1C | 承認詳細表示 |

### CICS 画面

| マップセット | 説明 |
|:---|:---|
| COPAU00 | 承認サマリー画面 |
| COPAU01 | 承認詳細画面 |

### JCL

| ジョブ | 説明 |
|:---|:---|
| CBPAUP0J | 期限切れ承認をパージするバッチジョブ |

### IMS DB コンポーネント

#### DBD (データベース定義)

| DBD | タイプ | 説明 | DD 名 |
|:---|:---|:---|:---|
| DBPAUTP0 | HIDAM | プライマリ承認データベース | DDPAUTP0 |
| DBPAUTX0 | HIDAM Index | 承認データベース用インデックス | DDPAUTX0 |

#### セグメント

| セグメント | DBD | 説明 |
|:---|:---|:---|
| PAUTSUM0 | DBPAUTP0 | 承認サマリー (ルート) |
| PAUTDTL1 | DBPAUTP0 | 承認詳細 (子) |
| PAUTINDX | DBPAUTX0 | インデックスセグメント |

#### PSB (プログラム仕様ブロック)

| PSB | タイプ | 説明 |
|:---|:---|:---|
| PSBPAUTB | BMP | バッチ処理用 |
| PSBPAUTL | Load | オンライン処理用 |

### DB2 コンポーネント

| コンポーネント | 説明 |
|:---|:---|
| AUTHFRDS | 不正追跡用 DB2 テーブル |
| XAUTHFRD | AUTHFRDS テーブルのインデックス |

### MQ 構成

| キュー名 | 説明 |
|:---|:---|
| AWS.M2.CARDDEMO.PAUTH.REQUEST | 承認リクエスト用入力キュー |
| AWS.M2.CARDDEMO.PAUTH.REPLY | 承認レスポンス用出力キュー |

## データモデル

### MQ メッセージ形式

#### 入力リクエストメッセージ形式

承認リクエストは、以下の順序でカンマ区切り値として受信されます：

```
AUTH-DATE  
AUTH-TIME  
CARD-NUM              
AUTH-TYPE             
CARD-EXPIRY-DATE      
MESSAGE-TYPE          
MESSAGE-SOURCE        
PROCESSING-CODE       
TRANSACTION-AMT       
MERCHANT-CATAGORY-CODE  
ACQR-COUNTRY-CODE     
POS-ENTRY-MODE        
MERCHANT-ID           
MERCHANT-NAME         
MERCHANT-CITY         
MERCHANT-STATE        
MERCHANT-ZIP          
TRANSACTION-ID
```

#### 出力レスポンスメッセージ形式

承認レスポンスは、以下の順序でカンマ区切り値として送信されます：

```
CARD-NUM        
TRANSACTION-ID  
AUTH-ID-CODE    
AUTH-RESP-CODE  
AUTH-RESP-REASON
APPROVED-AMT  
```

### IMS DB 構造

IMS データベースは、ルートセグメント (承認サマリー) と子セグメント (承認詳細) を持つ階層構造を使用します：

![IMS Data Model](../../diagrams/ims_model.png "IMS Data Model")

### DB2 スキーマ

DB2 テーブルには、不正としてマークされた承認レコードが格納されます：

![DB2 Data Model](../../diagrams/db2_model.png "DB2 Data Model")

## ユーザーインターフェース

### 承認サマリー画面

承認サマリー画面には、保留中の承認とアカウントの詳細が表示されます：

![Authorization Summary](../../diagrams/auth_summary.png "Authorization Summary")

ナビゲーション：

- PF7/PF8: 承認リストをスクロール
- 'S' で承認を選択し、Enter キーを押して詳細を表示

### 承認詳細画面

承認詳細画面には、特定の承認に関する包括的な情報が表示されます：

![Authorization Details](../../diagrams/auth_details.png "Authorization Details")

### 不正マーキング

承認詳細画面で PF5 を押すと、トランザクションが不正としてマークされます：

![Mark Authorization Fraud](../../diagrams/auth_fraud.png "Mark Authorization Fraud")

## ライセンス

このプロジェクトは、メインフレームモダナイゼーションのためのコミュニティリソースとして Apache 2.0 ライセンスの下で公開されています。

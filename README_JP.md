# CardDemo - メインフレーム クレジットカード管理アプリケーション

![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)
![License](https://img.shields.io/badge/license-Apache%202.0-green.svg)

## エグゼクティブサマリー

CardDemo は、クレジットカード管理システムをシミュレートする包括的なメインフレームアプリケーションです。メインフレームの移行およびモダナイゼーションのシナリオにおいて、AWS とパートナーのテクノロジーを紹介するために特別に設計されており、検出 (Discovery)、移行、パフォーマンステスト、サービス化 (Service Enablement) など、さまざまなモダナイゼーションアプローチをテストするための現実的な環境を提供します。

## 目次

- [説明](#説明)
- [テクノロジー](#テクノロジー)
- [オプション機能](#オプション機能)
- [インストール](#インストール)
- [バッチジョブの実行](#バッチジョブの実行)
- [アプリケーションの詳細](#アプリケーションの詳細)
  - [ユーザー機能](#ユーザー機能)
  - [管理者機能](#管理者機能)
  - [アプリケーションインベントリ](#アプリケーションインベントリ)
  - [アプリケーション画面](#アプリケーション画面)
- [技術的なハイライト](#技術的なハイライト)
- [サポート](#サポート)
- [ロードマップ](#ロードマップ)
- [コントリビューション](#コントリビューション)
- [ライセンス](#ライセンス)
- [プロジェクトの状況](#プロジェクトの状況)

## 説明

CardDemo は、メインフレームの移行およびモダナイゼーションのユースケースにおいて、AWS とパートナーのテクノロジーをテストおよび紹介するために設計されたメインフレームアプリケーションです。以下のような現実的な環境を提供します：

- アプリケーションの検出と分析
- 移行の評価と計画
- モダナイゼーション戦略の策定
- パフォーマンステスト
- システムの拡張
- サービス化と抽出
- テストの作成と自動化

このアプリケーションは、さまざまなメインフレームプログラミングパラダイムにわたる分析、変換、および移行ツールを検証するために、意図的にさまざまなコーディングスタイルとパターンを取り入れています。

## テクノロジー

### コアテクノロジー

- **COBOL**:主要なプログラミング言語
- **CICS**: トランザクション処理
- **VSAM (KSDS with AIX)**: データストレージ
- **JCL**: バッチ処理
- **RACF**: セキュリティ
- **ASSEMBLER**: システムレベルプログラミング
  - MVSWAIT: バッチジョブのタイマー制御
  - COBDATFT: 日付形式変換ユーティリティ

### オプションテクノロジー

- **Db2**: リレーショナルデータベース管理
- **IMS DB**: 階層型データベース
- **MQ**: メッセージキューイング
- **JCL ユーティリティ**: FTP, TXT2PDF, DB2 LOAD/UNLOAD, IMS DB LOAD/UNLOAD, Internal Reader
- **高度なデータ形式**: COMP, COMP-3, Zoned Decimal, Signed, Unsigned
- **追加のデータセットタイプ**: VSAM (ESDS/RRDS), GDG, PDS
- **レコード形式**: VB, FBA, その他
- **複雑なコピーブック構造**: REDEFINES, OCCURS, OCCURS DEPENDING ON

## オプション機能

CardDemo には、基本機能を拡張するいくつかのオプションモジュールが含まれています：

1. **IMS, DB2, MQ を使用したクレジットカード承認**
   - MQ を使用してクレジットカード承認リクエストをシミュレーション
   - IMS データベースから顧客データを取得
   - DB2 テーブルにトランザクションをログ記録
   - 機能：
     - 承認リクエスト処理
     - 保留中の承認のサマリーと詳細
     - 期限切れの承認のバッチパージ
   - 詳細：[Pending Authorization Extension](./app/app-authorization-ims-db2-mq/README_JP.md)

2. **DB2 を使用したトランザクションタイプ管理**
   - DB2 テーブルでトランザクションタイプ参照データを維持
   - CICS トランザクションからトランザクションタイプを追加、更新、または削除
   - バッチジョブによるトランザクションタイプの管理
   - カーソルや SQL 操作を含む DB2 統合パターンをデモ

3. **MQ と VSAM を使用したアカウント抽出**
   - MQ チャネルを通じてアカウントデータを抽出および送信
   - MQ 経由のシステム日付照会 (CDRD トランザクション)
   - MQ 経由のアカウント詳細照会 (CDRA トランザクション)
   - 非同期処理パターンをデモ

4. **追加の JCL ユーティリティ**
   - FTP 統合
   - テキストから PDF への変換
   - DB2 および IMS DB のロード/アンロード操作
   - 内部リーダー (Internal Reader) 機能

## インストール

### 前提条件

- CICS, VSAM, JCL をサポートするメインフレーム環境
- オプション：拡張機能用の DB2, IMS DB, MQ
- ローカル環境とメインフレーム間のファイル転送機能

### インストール手順

1. **環境の準備**
   - このリポジトリをローカル開発環境にクローンします
   - メインフレーム環境への適切なアクセス権があることを確認します

2. **メインフレームデータセットの作成**
   - データセットの高位修飾子 (HLQ) を定義します
   - 以下の形式でデータセットを作成します：

     | HLQ    | 名前          | 形式 | 長さ |
     | :----- | :------------ | :----- | -----: |
     | AWS.M2 | CARDDEMO.JCL  | FB     |     80 |
     | AWS.M2 | CARDDEMO.PROC | FB     |     80 |
     | AWS.M2 | CARDDEMO.CBL  | FB     |     80 |
     | AWS.M2 | CARDDEMO.CPY  | FB     |     80 |
     | AWS.M2 | CARDDEMO.BMS  | FB     |     80 |
     | AWS.M2 | CARDDEMO.ASM  | FB     |     80 |
     | AWS.M2 | CARDDEMO.MACLIB| FB    |     80 |

3. **ソースコードのアップロード**
   - リポジトリからアプリケーションのソースフォルダをメインフレームにアップロードします
   - $INDFILE またはお好みのファイル転送ツールを使用します
   - 必要に応じて適切な転送モード (バイナリ/テキスト) を確認してください

4. **サンプルデータのアップロード**
   - `main/-/data/EBCDIC/` フォルダからサンプルデータをメインフレームに転送します
   - データ整合性を維持するためにバイナリ転送モードを使用してください
   - 以下のデータセットを作成します：

     | データセット名                      | 説明                                         | コピーブック     | 形式 | 長さ |
     | :----------------------------------| :------------------------------------------- | :-------------- | :--- | ---: |
     | AWS.M2.CARDDEMO.USRSEC.PS         | ユーザーセキュリティファイル                 | CSUSR01Y     | FB     |     80 |
     | AWS.M2.CARDDEMO.ACCTDATA.PS       | アカウントデータ                             | CVACT01Y     | FB     |    300 |
     | AWS.M2.CARDDEMO.CARDDATA.PS       | カードデータ                                 | CVACT02Y     | FB     |    150 |
     | AWS.M2.CARDDEMO.CUSTDATA.PS       | 顧客データ                                   | CVCUS01Y     | FB     |    500 |
     | AWS.M2.CARDDEMO.CARDXREF.PS       | 顧客アカウントカード相互参照                 | CVACT03Y     | FB     |     50 |
     | AWS.M2.CARDDEMO.DALYTRAN.PS.INIT  | トランザクションデータベース初期化レコード   | CVTRA06Y     | FB     |    350 |
     | AWS.M2.CARDDEMO.DALYTRAN.PS       | 投稿用トランザクションデータ                 | CVTRA06Y     | FB     |    350 |
     | AWS.M2.CARDDEMO.TRANSACT.VSAM.KSDS| オンライントランザクションデータ             | CVTRA05Y     | FB     |    350 |
     | AWS.M2.CARDDEMO.DISCGRP.PS        | 開示グループ                                 | CVTRA02Y     | FB     |     50 |
     | AWS.M2.CARDDEMO.TRANCATG.PS       | トランザクションカテゴリティップ             | CVTRA04Y     | FB     |     60 |
     | AWS.M2.CARDDEMO.TRANTYPE.PS       | トランザクションタイプ                       | CVTRA03Y     | FB     |     60 |
     | AWS.M2.CARDDEMO.TCATBALF.PS       | トランザクションカテゴリ残高                 | CVTRA01Y     | FB     |     50 |

5. **環境の初期化**
   - 以下の JCL を順番に実行します：

     | ジョブ名 | 目的                                              | オプションモジュール |
     | :------- | :------------------------------------------------ |:------------------- |
     | DUSRSECJ | ユーザーセキュリティ VSAM ファイルのセットアップ  |                     |
     | CLOSEFIL | CICS によって開かれたファイルを閉じる             |                     |
     | ACCTFILE | サンプルデータを使用してアカウントデータベースをロード |                     |
     | CARDFILE | クレジットカードサンプルデータでカードデータベースをロード |                     |
     | CUSTFILE | 顧客データベースの作成                            |                     |
     | XREFFILE | 顧客カードアカウント相互参照のロード              |                     |
     | CREADB21 | CardDemo Db2 データベースの作成とテーブルのロード | Db2: Transaction Type Mgmt |
     | TRANFILE | 初期トランザクションファイルを VSAM にコピー      |                     |
     | TRANEXTR | Db2 から TRAN タイプとカテゴリテーブルを抽出      | Db2: Transaction Type Mgmt |
     | DISCGRP  | 初期開示グループファイルを VSAM にコピー          |                     |
     | TCATBALF | 初期 TCATBALF ファイルを VSAM にコピー            |                     |
     | TRANCATG | 初期トランザクションカテゴリファイルを VSAM にコピー |                     |
     | TRANTYPE | 初期トランザクションタイプファイルを VSAM にコピー |                     |
     | OPENFIL  | ファイルを CICS で利用可能にする                  |                     |
     | DEFGDGB  | GDG ベースの定義                                  |                     |
     | DEFGDGD  | Db2 用に追加された GDG ベースの定義               |                     |

6. **プログラムのコンパイル**
   - 標準のメインフレームコンパイル手順を使用してください
   - コンパイルを支援するために、サンプル JCL が samples フォルダに提供されています

7. **CICS リソースの構成**
   - オプション 1 (推奨)：CSD フォルダ内の CSD ファイルと共に DFHCSDUP JCL を使用する
   - オプション 2：CEDA トランザクションを使用してリソースを手動で定義する：

     ```
     DEFINE LIBRARY(COM2DOLL) GROUP(CARDDEMO) DSNAME01(&HLQ..LOADLIB)
     DEF PROGRAM(COCRDLIC) GROUP(CARDDEMO)
     DEF MAPSET(COCRDLI) GROUP(CARDDEMO)
     DEFINE PROGRAM(COSGN00C) GROUP(CARDDEMO) DA(ANY) TRANSID(CC00) DESCRIPTION(LOGIN)
     DEFINE TRANSACTION(CC00) GROUP(CARDDEMO) PROGRAM(COSGN00C) TASKDATAL(ANY)
     ```

8. **リソースのインストールとロード**
   - CICS リージョンにリソースをインストールします：

     ```
     CEDA INSTALL TRANS(CCLI) GROUP(CARDDEMO)
     CEDA INSTALL FILE(CARDDAT) GROUP(CARDDEMO)
     CECI LOAD PROG(COCRDUP)
     CECI LOAD PROG(COCRDUPC)
     ```

   - マップセットとプログラムに対して NEWCOPY を実行します：

     ```
     CEMT SET PROG(COCRDUP) NEWCOPY
     CEMT SET PROG(COCRDUPC) NEWCOPY
     ```

### アプリケーションへのアクセス

- **オンライン機能**: CC00 トランザクションを使用して CardDemo アプリケーションを開始します
  - 管理者アクセス：ユーザー ID `ADMIN001` パスワード `PASSWORD` を使用
  - ユーザーアクセス：ユーザー ID `USER0001` パスワード `PASSWORD` を使用
- **バッチ機能**: 下記の「バッチジョブの実行」セクションを参照してください

## バッチジョブの実行

完全なバッチプロセスを実行するには、以下の JCL を順番に実行してください：

| ジョブ名 | 目的 | オプションモジュール |
| :------- | :--- | :------------------- |
| CLOSEFIL | CICS によって開かれたファイルを閉じる | |
| ACCTFILE | サンプルデータを使用してアカウントデータベースロード | |
| CARDFILE | クレジットカードサンプルデータでカードデータベースをロード | |
| XREFFILE | 顧客カードアカウント相互参照を VSAM にロード | |
| CUSTFILE | 顧客データベースの作成 | |
| TRANBKP  | トランザクションデータベースの作成 | |
| TRANEXTR | トランザクションタイプの最新 Db2 データを抽出 | Db2: Transaction Type Mgmt |
| TRANCATG | 最新のトランザクションカテゴリファイルを VSAM にコピー | |
| TRANTYPE | 最新のトランザクションタイプファイルを VSAM にコピー | |
| DISCGRP  | 初期開示グループファイルを VSAM にコピー | |
| TCATBALF | 初期 TCATBALF ファイルを VSAM にコピー | |
| DUSRSECJ | ユーザーセキュリティ VSAM ファイルのセットアップ | |
| POSTTRAN | コアトランザクション処理ジョブ | |
| INTCALC  | 利息計算の実行 | |
| TRANBKP  | トランザクションデータベースのバックアップ | |
| COMBTRAN | システムトランザクションと日次トランザクションの結合 | |
| CREASTMT | トランザクション明細書の作成 | |
| TRANIDX  | トランザクションファイルの代替インデックスの定義 | |
| OPENFIL  | ファイルを CICS で利用可能にする | |
| WAITSTEP | 指定された時間ジョブを待機させるステップを定義 | |
| CBPAUP0J | 期限切れの承認をパージ | IMS-DB2-MQ: Pending Authorizations |

## アプリケーションの詳細

CardDemo は、主に COBOL を使用して構築された包括的なクレジットカード管理アプリケーションです。アカウント、クレジットカード、トランザクション、および請求書の支払いを管理する機能を提供します。

### ユーザータイプ

アプリケーションは 2 つのユーザーロールをサポートします：

- **一般ユーザー**: 標準的なカード管理機能を実行できます
- **管理者ユーザー**: ユーザー管理などの管理機能を実行できます

### ユーザー機能

![User Function Flow](./diagrams/Application-Flow-User.png "User Function Flow")

一般ユーザーは以下の機能を実行できます：

- アカウント情報の表示と更新
- クレジットカードの管理
- トランザクションの表示、追加、および処理
- トランザクションレポートの生成
- 請求書の支払い
- 保留中の承認の表示 (オプションモジュール)

### 管理者機能

![Admin Function Flow](./diagrams/Application-Flow-Admin.png "Admin Function Flow")

管理者ユーザーは以下の機能を実行できます：

- ユーザー管理 (一覧、追加、更新、削除)
- トランザクションタイプ管理 (DB2 オプションモジュールを使用)

### アプリケーションインベントリ

#### オンラインコンポーネント

(表の内容は技術的なIDや名称が多いため、必要に応じて原文の表を参照することを推奨しますが、ヘッダー等は翻訳します)

| トランザクション | BMS マップ | プログラム | 機能 | オプションモジュール | 備考 |
|:---|:---|:---|:---|:---|:---|
| CC00 | COSGN00 | COSGN00C | サインオン画面 | | |
| CM00 | COMEN01 | COMEN01C | メインメニュー | | |
| CAVW | COACTVW | COACTVWC | アカウント表示 | | |
| CAUP | COACTUP | COACTUPC | アカウント更新 | | |
| CCLI | COCRDLI | COCRDLIC | クレジットカード一覧 | | |
| CCDL | COCRDSL | COCRDSLC | クレジットカード表示 | | |
| CCUP | COCRDUP | COCRDUPC | クレジットカード更新 | | |
| CT00 | COTRN00 | COTRN00C | トランザクション一覧 | | |
| CT01 | COTRN01 | COTRN01C | トランザクション表示 | | |
| CT02 | COTRN02 | COTRN02C | トランザクション追加 | | |
| CR00 | CORPT00 | CORPT00C | トランザクションレポート | | |
| CB00 | COBIL00 | COBIL00C | 請求書支払い | | |
| CPVS | COPAU00 | COPAUS0C | 保留中の承認サマリー | IMS-DB2-MQ: Pending Authorizations | Reads IMS and VSAM |
| CPVD | COPAU01 | COPAUS1C | 保留中の承認詳細 | IMS-DB2-MQ: Pending Authorizations | Updates IMS and Insert DB2 |
| CP00 | | COPAUA0C | 承認リクエスト処理 | IMS-DB2-MQ: Pending Authorizations | MQ trigger, request and response; Insert and Update to IMS|
| CA00 | COADM01 | COADM01C | 管理メニュー | Db2: Transaction Type Mgmt | |
| CU00 | COUSR00 | COUSR00C | ユーザー一覧 | | |
| CU01 | COUSR01 | COUSR01C | ユーザー追加 | | |
| CU02 | COUSR02 | COUSR02C | ユーザー更新 | | |
| CU03 | COUSR03 | COUSR03C | ユーザー削除 | | |
| CTTU | COTRTUP | COTRTUPC | トランザクションタイプ追加/編集 | Db2: Transaction Type Mgmt | Update and insert on Db2 |
| CTLI | COTRTLI | COTRTLIC | トランザクションタイプ一覧/更新/削除 | Db2: Transaction Type Mgmt | Demonstrates cursor and delete in Db2 |
| CDRD | | CODATE01 | MQ によるシステム日付照会 | MQ Integration | Demonstrates MQ request/response pattern |
| CDRA | | COACCT01 | MQ によるアカウント詳細照会 | MQ Integration | Demonstrates MQ request/response pattern |

#### バッチコンポーネント

| ジョブ | プログラム | 機能 | オプションモジュール |
|:---|:---|:---|:---|
| DUSRSECJ | IEBGENER | ユーザーセキュリティファイルの初期ロード | |
| DEFGDGB | IDCAMS | GDG ベースのセットアップ | |
| DEFGDGD | IDCAMS | Db2 用の追加 GDG ベースのセットアップ | |
| ACCTFILE | IDCAMS | アカウントマスタの更新 | |
| CARDFILE | IDCAMS | カードマスタの更新 | |
| CUSTFILE | IDCAMS | 顧客マスタの更新 | |
| CREADB21 | DSNTEP4 | CardDemo Db2 データベースの作成とテーブルロード | Db2: Transaction Type Mgmt |
| TRANEXTR | DSNTIAUL | トランザクションタイプの最新 Db2 データの抽出 | Db2: Transaction Type Mgmt |
| DISCGRP | IDCAMS | 開示グループファイルのロード | |
| TRANFILE | IDCAMS | トランザクションマスタファイルのロード | |
| TRANCATG | IDCAMS | トランザクションカテゴリティップのロード | |
| TRANTYPE | IDCAMS | トランザクションタイプファイルのロード | |
| XREFFILE | IDCAMS | アカウント、カード、顧客の相互参照 | |
| CLOSEFIL | IEFBR14 | CICS VSAM ファイルを閉じる | |
| TCATBALF | IDCAMS | トランザクションカテゴリ残高の更新 | |
| TRANBKP | IDCAMS | トランザクションマスタの更新 | |
| POSTTRAN | CBTRN02C | トランザクション処理ジョブ | |
| TRANIDX | IDCAMS | トランザクションファイルの AIX 定義 | |
| OPENFIL | IEFBR14 | CICS ファイルを開く | |
| INTCALC | CBACT04C | 利息計算の実行 | |
| COMBTRAN | SORT | トランザクションファイルの結合 | |
| CREASTMT | CBSTM03A | トランザクション明細書の作成 | |
| TRANREPT | CBTRN03C | トランザクションレポート - CICS から送信 | |
| ESDSRRDS | IDCAMS | ESDS および RRDS VSAM ファイルの作成 | |
| CBPAUP0J | CBPAUP0C | 期限切れ承認のパージ | IMS-DB2-MQ: Pending Authorizations |
| MNTTRDB2 | COBTUPDT | トランザクションタイプテーブルの保守 | Db2: Transaction Type Mgmt |
| WAITSTEP | COBSWAIT | 指定時間ジョブを待機 | |

### アプリケーション画面

#### サインオン画面

![Signon Screen](./diagrams/Signon-Screen.png "Signon Screen")

#### メインメニュー

![Main Menu](./diagrams/Main-Menu.png "Main Menu")

**注**: オプション 11 (保留中の承認) は、オプションのクレジットカード承認機能でのみ利用可能です。詳細については、[承認に関するドキュメント](./app/app-authorization-ims-db2-mq/README_JP.md)を参照してください。

#### 管理メニュー

![Admin Menu](./diagrams/Admin-Menu.png "Admin Menu")

**注**: オプション 5 および 6 は、DB2 オプション機能を使用したトランザクションタイプ管理 (トランザクション CTTU および CTLI) をインストールした場合にのみ有効になります。

## 技術的なハイライト

| コンポーネント | ドメイン機能 | 技術的機能 |
|:---|:---|:---|
| **基本アプリケーション** | 顧客<br>アカウント<br>カード<br>トランザクション<br>請求書支払い<br>明細書/レポート | COBOL<br>CICS<br>JCL (Batch)<br>VSAM (KSDS with AIX) |
| **オプション機能** | 承認<br>不正検出<br>トランザクションタイプ (拡張) | DB2<br>MQ<br>IMS DB<br>JCL ユーティリティ<br>複雑なデータ形式<br>様々なデータセットタイプ<br>高度なコピーブック構造 |

## サポート

質問、問題、または改善の要望については、懸念事項に関する詳細情報を添えてリポジトリで issue を提起してください。メンテナは可用性に応じて対応します。

## ロードマップ

以下の機能が今後のリリースで計画されています：

1. **追加のデータベース構文使用シナリオ**
   - DB2 リワード：トランザクションタイプ、カテゴリ、およびルールに基づいてトランザクションのリワードを計算
     - ストアドプロシージャ、関数、および動的 SQL を含む予定
   - 階層型データベース：IMS DC の実装

2. **統合の強化**
   - FTP および SFTP 統合
   - Web サービス接続
   - 分散アプリケーション統合のためのトランザクションの公開

## コントリビューション

メインフレームコミュニティからのこのコードベースへの貢献と強化を歓迎します。貢献するには：

1. リポジトリをフォークする
2. 機能ブランチを作成する
3. 適切なテストを含めて変更を実装する
4. 変更の明確な説明を添えてプルリクエストを送信する

プログラマーがメインフレームを理解し、モダナイズするためのリソースとしてこのアプリケーションを構築するのを支援するために、機能強化のための issue の提起、コードの作成、およびマージリクエストの送信を自由に行ってください。

## ライセンス

このプロジェクトはコミュニティリソースを意図しており、Apache 2.0 ライセンスの下で公開されています。

## プロジェクトの状況

CardDemo アプリケーションは、機能を拡張するオプション機能で強化されています：

- IMS, DB2, MQ を使用したクレジットカード承認
- DB2 を使用したトランザクションタイプ管理
- MQ と VSAM を使用したアカウント抽出
- 追加の JCL ユーティリティ
- 強化されたデータおよびコピーブック機能

これらのオプション機能により、CardDemo はメインフレームアプリケーションのモダナイズを検討している顧客にとってさらに有用なリソースになります。DB2, MQ, IMS DB, JCL ユーティリティ、およびより多くのデータ形式のモジュールが利用可能になったことで、顧客は CardDemo を活用して、より幅広いメインフレーム移行、リファクタリング、リプラットフォーム、および拡張シナリオをテストできます。

最終更新: 2025年4月

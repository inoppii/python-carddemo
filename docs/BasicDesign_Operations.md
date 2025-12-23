# CardDemo システム 基本設計書（運用管理編）

## 1. 概要

本書は、CardDemo システムの安定稼働と保安を維持するための運用管理仕様を定義します。ユーザー管理、バックアップ、およびシステムメンテナンス用ユーティリティを網羅します。

## 2. ユーザー・セキュリティ管理

システムへのアクセスは、`USRSEC` ファイル（VSAM KSDS）によって厳格に管理されます。

### 2.1. 管理項目

- **ユーザー ID**: 8 桁の一意の識別子。
- **パスワード**: 暗号化またはハッシュ化（移行後の要件に依存）して保管。
- **権限レベル**:
  - `ADMIN`: 全機能（ユーザー管理、設定更新等）が利用可能。
  - `USER`: 一般的な取引照会・更新機能のみ利用可能。

### 2.2. 管理機能 (COUSR*C)

- オンライン画面から、管理者 ID でのみユーザーの追加、更新、削除が可能です。
- 新規ユーザー作成時は、初期パスワードの強制変更などのフローが組み込まれています。

## 3. バックアップ・リカバリ

データの欠損や障害に備え、以下のバックアップ運用を実施します。

### 3.1. バックアップ対象と方式

| 対象データ | 方式 | 頻度 | 使用 JCL (例) |
| :--- | :--- | :--- | :--- |
| **VSAM (KSDS)** | `IDCAMS REPRO` 出力 (GDG) | 日次 (サイクル前) | `TRANBKP.jcl` |
| **DB2** | `IMAGE COPY` | 定期 | (DB管理規定に準拠) |

## 4. システムメンテナンス・ユーティリティ

システムの運用を補助するための各種ツールおよびバッチジョブです。

- **`LISTCAT.txt`**: VSAM ファイルの状態（エントリ数、空き容量等）の監視に使用。
- **`OPENFIL / CLOSEFIL.jcl`**: オンライン実行中にバッチで排他取得が必要な場合、ファイルを CICS から一時的に切断するために使用。
- **`DUSRSECJ.jcl`**: セキュリティデータの初期投入およびリセット用。

## 5. ログ管理

- **SYSOUT**: バッチジョブの実行統計、エラー箇所を記録。
- **REJS (DALYREJS)**: データ不備により処理されなかったレコードの履歴。運用の一次調査資料として活用。

---
[概要編](file:///Users/inohara/Documents/antigravity-demo/aws-mainframe-modernization-carddemo/docs/BasicDesign.md) | [オンライン処理編](file:///Users/inohara/Documents/antigravity-demo/aws-mainframe-modernization-carddemo/docs/BasicDesign_Online.md) | [バッチ処理編](file:///Users/inohara/Documents/antigravity-demo/aws-mainframe-modernization-carddemo/docs/BasicDesign_Batch.md) | [データベース設計編](file:///Users/inohara/Documents/antigravity-demo/aws-mainframe-modernization-carddemo/docs/BasicDesign_Database.md) | [関連システムインターフェース編](file:///Users/inohara/Documents/antigravity-demo/aws-mainframe-modernization-carddemo/docs/BasicDesign_Interface.md)

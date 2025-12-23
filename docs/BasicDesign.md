# CardDemo システム 基本設計書（概要編）

## 1. はじめに

本書は、CardDemo システムの全体像を俯瞰することを目的とした「概要編」です。システム全体のアーキテクチャ、機能体系、および業務サイクルの概要を記載します。

詳細な設計内容については、以下の各編を参照してください。

- [オンライン処理編](file:///Users/inohara/Documents/antigravity-demo/aws-mainframe-modernization-carddemo/docs/BasicDesign_Online.md)
- [バッチ処理編](file:///Users/inohara/Documents/antigravity-demo/aws-mainframe-modernization-carddemo/docs/BasicDesign_Batch.md)
- [データベース設計編](file:///Users/inohara/Documents/antigravity-demo/aws-mainframe-modernization-carddemo/docs/BasicDesign_Database.md)
- [関連システムインターフェース編](file:///Users/inohara/Documents/antigravity-demo/aws-mainframe-modernization-carddemo/docs/BasicDesign_Interface.md)
- [運用管理編](file:///Users/inohara/Documents/antigravity-demo/aws-mainframe-modernization-carddemo/docs/BasicDesign_Operations.md)

---

## 2. 全体アーキテクチャ

システムは CICS オンライン、JCL バッチ、および VSAM/DB2 データ層の 3 層で構成されます。

![CardDemo 全体アーキテクチャ図](./diagrams/architecture_diagram.png)

## 3. 機能体系の概要

各業務カテゴリごとの機能分担は以下の通りです。詳細は各編にて詳述します。

### 3.1. オンライン機能

 TN3270 端末を介して、顧客管理、取引登録、承認フローなどのリアルタイム処理を提供します。

### 3.2. バッチ機能

夜間サイクル等で動作し、大量取引の反映、利息計算、帳票出力、データ移行を行います。

## 4. データ構造の概要

VSAM ファイルを主軸とし、一部の設定情報を DB2 で管理します。物理的なデータ格納先やレイアウトは「データベース設計編」を参照してください。

---
[オンライン処理編](file:///Users/inohara/Documents/antigravity-demo/aws-mainframe-modernization-carddemo/docs/BasicDesign_Online.md) | [バッチ処理編](file:///Users/inohara/Documents/antigravity-demo/aws-mainframe-modernization-carddemo/docs/BasicDesign_Batch.md) | [データベース設計編](file:///Users/inohara/Documents/antigravity-demo/aws-mainframe-modernization-carddemo/docs/BasicDesign_Database.md) | [関連システムインターフェース編](file:///Users/inohara/Documents/antigravity-demo/aws-mainframe-modernization-carddemo/docs/BasicDesign_Interface.md) | [運用管理編](file:///Users/inohara/Documents/antigravity-demo/aws-mainframe-modernization-carddemo/docs/BasicDesign_Operations.md)

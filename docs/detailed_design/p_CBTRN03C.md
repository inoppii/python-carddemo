# p_CBTRN03C 詳細設計書

## 1. 概要

`p_CBTRN03C.py` は、指定された期間の取引データを集計し、カード・アカウント単位の取引詳細レポートを作成するバッチプログラムです。PostgreSQL の `transactions` テーブルおよびマスタテーブルからデータを抽出し、GCS にレポートを出力します。

## 2. プログラム情報

- **プログラム ID**: `p_CBTRN03C.py`
- **言語**: Python 3.10+
- **接続DB**: Cloud SQL for PostgreSQL
- **主要モジュール**: `SQLAlchemy`, `pandas`, `google-cloud-storage`

## 3. 入出力定義

### 3.1. 入力 (Database)

- **transactions**: 取引履歴。
- **card_xref**: カード・アカウント対応。
- **transaction_types**: 取引タイプ名称。
- **transaction_categories**: カテゴリ名称。

### 3.2. 出力 (Cloud Storage)

- **GCS Object**: `gs://carddemo-data/reports/transaction_report_{YYYYMMDD}.pdf` または `.txt`
- **内容**: 改ページ制御、ヘッダー、明細、ページ合計、総合計を含む請求・監査用レポート。

## 4. 処理ロジック詳細

### 4.1. データ抽出・結合

1. 抽出期間を指定して `transactions` をクエリ。
2. 必要に応じて `transaction_types`, `transaction_categories` テーブルを JOIN し、名称を解決。
3. カード番号順、処理日時順に結果をソート。

### 4.2. 集計・フォーマット処理

1. `pandas` またはカスタム集計ロジックを使用し、カードごとの小計を算出。
2. レポート形式（PDF テンプレートまたは固定幅テキスト）へ流し込み。
3. ページ番号の付与、改ページ制御（20行ごと等）の実施。

## 5. エラーハンドリング

- DB 接続、マスタ取得エラー時はログ出力後に異常終了。
- マスタ名称が見つからない場合はコード値をそのまま表示し処理続行。

---
[バッチ処理編](file:///Users/inohara/Documents/antigravity-demo/python-carddemo/docs/p_BasicDesign_Batch.md)

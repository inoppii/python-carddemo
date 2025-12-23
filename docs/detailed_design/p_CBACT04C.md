# p_CBACT04C 詳細設計書

## 1. 概要

`p_CBACT04C.py` は、月次バッチ処理において各アカウントの利息を計算して計上するプログラムです。PostgreSQL の `category_balances` テーブルに基づき計算を行い、`transactions` テーブルへの記帳と `accounts` テーブルの残高反映を行います。

## 2. プログラム情報

- **プログラム ID**: `p_CBACT04C.py`
- **言語**: Python 3.10+
- **接続DB**: Cloud SQL for PostgreSQL

## 3. 入出力定義

### 3.1. 入力 (Database)

- **category_balances**: アカウント/カテゴリ別の現在の残高。
- **interest_rates**: （旧 `DISCGRP-FILE` 相当）カテゴリ別の利率定義テーブル。

### 3.2. 出力・更新 (Database)

- **transactions**: 計算された利息を「System」取引として新規挿入。
- **accounts**: `acct_curr_bal` の更新および、月次サイクル累計額 (`acct_curr_cyc_credit/debit`) のリセット。

## 4. 処理ロジック詳細

### 4.1. 利息計算処理

1. `category_balances` を読み込み、アカウントごとに集計。
2. 各カテゴリの残高に対し、`interest_rates` テーブルから取得した利率を適用。
3. 月利計算式: `( 残高 * 年利率 ) / 1200`
4. アカウントごとの合計利息を算出。

### 4.2. 反映・更新 (トランザクション管理)

以下の処理をアカウント単位、またはバッチ全体で一括のトランザクションとして実行します。

1. **取引登録**: `transactions` テーブルに利息明細をインサート。
2. **アカウント更新**:
    - `acct_curr_bal` に利息を加算。
    - `acct_curr_cyc_credit` および `acct_curr_cyc_debit` を 0 にリセット。

## 5. エラーハンドリング

- 利率が定義されていない場合は利息 0 として処理。
- DB 接続エラーや整合性エラー発生時はロールバックを行い、ログを出力して異常終了。

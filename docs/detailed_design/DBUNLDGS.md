# DBUNLDGS 詳細設計書

## 1. 概要

`DBUNLDGS` は、IMS データベース (`PSBPAUTB`) 上の承認データを読み込み、GSAM (Generalized Sequential Access Method) データベースを介してフラットファイルへアンロードするバッチプログラムです。通常、バックアップやデータ移行、あるいは他システムへの連携用ファイル作成に使用されます。

## 2. プログラム情報

- **プログラム ID**: `DBUNLDGS`
- **作成者**: AWS
- **タイプ**: COBOL Batch, IMS (DLI), GSAM
- **機能**: Unload Authorization Data to GSAM

## 3. 入出力定義

### 3.1. IMS データベース (入力)

- **PSB**: `PSBPAUTB` (参照用 PCB)
- **セグメント**:
  - `PAUTSUM0` (ルート): アカウント単位の承認サマリー。
  - `PAUTDTL1` (子供): 個別の承認明細。

### 3.2. GSAM データベース (出力)

- **PCB**:
  - `PASFLPCB`: ルートセグメント出力用 GSAM PCB (ファイル1に相当)。
  - `PADFLPCB`: 子セグメント出力用 GSAM PCB (ファイル2に相当)。
- **物理ファイル**: JCL で定義された DD 名 (例: `OUTFILE1`, `OUTFILE2` など、GSAM 定義に依存) に出力される。

## 4. 処理ロジック詳細

### 4.1. 初期化処理 (1000-INITIALIZE)

- 現在日付等の取得。
- 開始メッセージの出力。

### 4.2. メインループ (2000-FIND-NEXT-AUTH-SUMMARY)

IMS データベースを順次読み込み (`GN`), GSAM へ書き出す。

1. **ルートセグメント読み込み**:
   - `DLI GN` で `PAUTSUM0` を取得。
   - データ終了 (`GB`) までループ。
2. **ルート書き出し**:
   - 取得したルートセグメントを、GSAM PCB (`PASFLPCB`) を使用して `DLI ISRT` (挿入) する (`3100-INSERT-PARENT-SEG-GSAM`)。
   - これにより、GSAM に紐付いた順編成ファイルへデータが書き込まれる。
3. **明細ループ (3000-FIND-NEXT-AUTH-DTL)**:
   - ルート配下の子セグメントを全て取得するため、`DLI GNP` (Get Next Within Parent) を発行。
   - セグメントが見つかるたびに、GSAM PCB (`PADFLPCB`) を使用して `DLI ISRT` する (`3200-INSERT-CHILD-SEG-GSAM`)。
   - 子セグメントがなくなる (`GE`) まで繰り返す。

### 4.3. 終了処理 (4000-FILE-CLOSE)

- ファイルクローズ処理 (IMS/GSAM の場合は `DLI TERM` で自動的に処理されることが多いが、明示的な終了処理記述があるか確認)。
- 処理件数統計の表示。
- `GOBACK`。

## 5. エラーハンドリング

- **DLI エラー**: 各 DLI コール (`GN`, `GNP`, `ISRT`) 後のステータスコードをチェック。
- 異常時は `9999-ABEND` ルーチンへ飛び、リターンコード 16 で終了。

## 6. 特記事項

- **GSAM の使用**: 通常の順編成ファイル (QSAM) ではなく、IMS の管理下にある GSAM を使用している点が特徴。これにより、IMS のチェックポイント/リスタート機能と連動したファイル操作が可能になる。
- **データ構造**: 出力されるファイルは、IMS セグメントの内容をそのままフラットにしたバイナリ/テキスト混在形式となる。

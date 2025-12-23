# p_COMEN01C 詳細設計書

## 1. 概要

`p_COMEN01C.py` は、一般ユーザー向けのメインメニュー画面および遷移制御を提供するオンライン処理プログラムです。旧システム `COMEN01C` (CICS) を基に、Web ポータルまたは API ゲートウェイとしての役割を再実装します。

## 2. プログラム情報

- **プログラム ID**: `p_COMEN01C.py`
- **言語**: Python 3.10+
- **接続DB**: なし（セッション管理に依存）
- **主要モジュール**: `FastAPI` (Router / Navigation)

## 3. インターフェース定義

### 3.1. API / 画面遷移

- **GET `/menu`**: メインメニューの表示。
- **機能リスト**:
    1. Account View -> `p_COACTVWC`
    2. Account Update -> `p_COACTUPC`
    3. Credit Card List -> `p_COCRDLIC`
    4. Credit Card View -> `p_COCRDSLC`
    5. Credit Card Update -> `p_COCRDUPC`
    6. Transaction List -> `p_COTRN00C`
    7. Transaction View -> `p_COTRN01C`
    8. Bill Payment -> `p_COBIL00C`

## 4. 処理ロジック詳細

1. **認可チェック**: 有効なセッション（JWT）を保持しているか確認。
2. **メニュー生成**: ユーザーのロール（一般ユーザー 'R' 等）に基づいてアクセス可能な機能リストを動的に生成。
3. **遷移制御**: クライアント側（SPA 等）またはバックエンドのリダイレクトによって、選択された機能エンドポイントに誘導。

## 5. エラーハンドリング

- **401 Unauthorized**: 未ログイン時のアクセス。
- **403 Forbidden**: 権限外の機能へのアクセス試行。

---
[オンライン処理編](file:///Users/inohara/Documents/antigravity-demo/python-carddemo/docs/p_BasicDesign_Online.md)

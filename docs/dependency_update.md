# 教員（メンテナンス担当者）向け依存関係更新ガイド

このドキュメントでは、Dependabot によって `requirements.txt` が更新された後、ローカル開発環境の同期および受講生向け環境の安全な検証（グローバル汚染の防止）を行う手順を説明します。

---

## 1. 講師ローカル環境の同期手順（`uv` を使用）

講師のローカル開発環境では、`uv` を使用して高速かつ安全に同期を行います。

### 1-1. 依存関係の解決確認（dry-run）
実際にインストールする前に、依存関係に競合が発生しないかをチェックします。

```bash
# ルートの検証
uv pip install -r requirements.txt --dry-run

# 特定のChapter（例: chapter4）の検証
uv pip install -r chapter4/requirements.txt --dry-run
```

### 1-2. ローカル環境（`.venv`）への同期
競合がないことを確認したら、仮想環境に反映させます。

```bash
# ルートの依存関係を同期
uv pip sync requirements.txt

# Chapterごとの依存関係に切り替えて検証する場合
uv pip sync chapter4/requirements.txt
```
> [!NOTE]
> `uv pip sync` を使用すると、指定した `requirements.txt` に記述されていない不要なパッケージが自動的に仮想環境から削除（アンインストール）され、常にクリーンな状態が保たれます。また、これらはすべてプロジェクト直下の `.venv` 内のみが対象となり、Mac のシステム環境（グローバル）には一切影響しません。

---

## 2. 受講生向け環境の安全な検証手順（`pip` を使用）

受講生が実行する `pip install` の流れに問題がないか、講師環境でテストする際の手順です。
**Mac のグローバル環境を汚染しないよう、以下のいずれかの方法で実行してください。**

### 方法A: 仮想環境の `pip` を直接指定して実行する（推奨・安全）
アクティベート状態に関わらず、確実にプロジェクト直下の `.venv` 内にのみインストールされます。

- **macOS / Linux**:
  ```bash
  # 競合チェック (インストールはしない)
  ./.venv/bin/pip install -r chapter4/requirements.txt --dry-run

  # 実際にインストール検証
  ./.venv/bin/pip install -r chapter4/requirements.txt
  ```
- **Windows**:
  ```cmd
  # 競合チェック (インストールはしない)
  .\.venv\Scripts\pip install -r chapter4\requirements.txt --dry-run

  # 実際にインストール検証
  .\.venv\Scripts\pip install -r chapter4\requirements.txt
  ```

> [!IMPORTANT]
> **仮想環境に `pip` が存在しない場合の対処法**
> `uv venv` で作成されたクリーンな仮想環境には、デフォルトで `pip` コマンドが同梱されていません。
> 上記の `pip` 直接指定コマンドで `No module named pip` エラーが出た場合は、以下のコマンドで事前に仮想環境へ `pip` をインストールしてください（この操作もグローバル環境は汚染しません）。
> ```bash
> uv pip install pip
> ```

### 方法B: 仮想環境をアクティベートして実行する
事前に仮想環境を起動し、パスを切り替えてから実行します。

- **macOS / Linux**:
  ```bash
  source .venv/bin/activate
  pip install -r chapter4/requirements.txt --dry-run
  ```
- **Windows**:
  ```cmd
  .venv\Scripts\activate
  pip install -r chapter4\requirements.txt --dry-run
  ```

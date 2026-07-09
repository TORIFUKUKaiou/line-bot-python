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

### 1-2. ローカル環境（`.venv`）へのインストール
競合がないことを確認したら、仮想環境にインストールします。

```bash
# ルートの依存関係をインストール
uv pip install -r requirements.txt

# 特定のChapterの依存関係をインストールする場合
uv pip install -r chapter4/requirements.txt
```
> [!IMPORTANT]
> **`uv pip sync` ではなく `uv pip install -r` を使用してください**
> 今回のリポジトリでは、受講生へ提供する `requirements.txt` をシンプル（直接依存パッケージのみ記載）に保っています。
> `uv pip sync` コマンドを実行すると、記述されていないサブ依存（間接依存）パッケージ（例: `line-bot-sdk` が必要とする `requests` など）が仮想環境からすべて削除（アンインストール）されてしまい、`ModuleNotFoundError` が発生します。
> 必ず **`uv pip install -r`** を使用してインストールを行ってください。

### 1-3. 共通 `.venv` を用いたルートからの動作確認手順（推奨）
各Chapterごとに `venv` を作成して切り替えるのが手間な場合、一番依存パッケージが多い `chapter7/requirements.txt` をルートの `.venv` にインストールしておくことで、すべてのChapterのコードを1つの環境で動作確認できます。

1. **すべての依存関係をインストールする（ルートで実行）**
   ```bash
   uv pip install -r chapter7/requirements.txt
   ```
   ※ `chapter7` には `Flask`、`line-bot-sdk`、`openai` が含まれるため、他のChapter（4〜6）で必要なパッケージもすべて自動的にカバーされます。

2. **ルートディレクトリから直接実行する**
   プログラムを実行する際は、ディレクトリを移動せず、プロジェクトルートにいる状態のまま、仮想環境内の python を指定して実行します。
   ```bash
   # 環境変数不要で即座に動作確認が可能です
   uv run python chapter7/qiita.py
   ```
   > [!TIP]
   > この実行方法には以下のメリットがあります：
   > - 各Chapterフォルダに移動する手間が省けます。
   > - 環境変数を記述した `.env` ファイルをルート直下に配置している場合、カレントディレクトリがルートになるため、環境変数の読み込みエラーが発生しません。
   > - 実行対象スクリプト（`app.py`）と同じディレクトリにあるモジュール（例: `chapter7/chatgpt.py` 等）は、Pythonのインポート仕様（`sys.path`の自動追加）により、ルートから実行しても問題なく解決されます。

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

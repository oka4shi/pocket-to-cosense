# Pocket to Cosense

## 概要
Pocketに保存した記事をエクスポートして、Cosenseに対応したjson形式に変換するツールです。
Pocketがサービス終了するため、中身を移行するために作成しました。


## 使い方
### PocketのConsumer Keyの取得
1. [Pocketのアプリケーション作成ページ](https://getpocket.com/developer/apps/new)を開く
1. アプリケーション名、説明を適当に埋める
1. 権限は「Retrieve」を選択
1. プラットフォームは「Desktop (other)」を選択
1. 「Create Application」をクリック
1. [アプリケーション一覧ページ](https://getpocket.com/developer/apps/)でConsumer Keyを確認し、メモしておく


### アプリケーションの実行
1. リポジトリをクローン
   ```bash
   git clone https://github.com/oka4shi/pocket-to-cosense.git
   cd pocket-to-cosense
   ```
2. 仮想環境(venv)を作成し依存ライブラリをインストール
   ```bash
    python3 -m venv .venv
    source .venv/bin/activate
    pip install -r requirements.txt
    ```

3. PocketのConsumer Keyを環境変数に設定
    ```bash
    export POCKET_CONSUMER_KEY=xxxxxxxxxxxxxxxxxxxxxxxxx
    ```

4. 8080番のポートが使用中でないことを確認しアプリケーションを実行
    ※OAuthのRedirect URIがhttp://localhost:8080に設定されているため
    ```bash
    python main.py
    ```

5. ターミナルに表示されるURLをブラウザで開き、Pocketの認証を行い、待つ
6. output/以下にjsonファイルが出力されていることを確認する


### Cosenseにjsonをインポート
1. 左上のメニューからProject Settingsを開く
2. **インポート前にかならずバックアップを取得しておく**
3. Page Dataタブを開き、Import Pagesの部分で先程のjsonファイルを選択する




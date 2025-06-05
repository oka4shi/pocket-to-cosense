# Pocket to Cosense

## 概要
Pocketに保存した記事をエクスポートして、Cosense(旧Scrapbox)に対応したjson形式に変換するツールです。
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
1. リポジトリをクローンする
   ```bash
   git clone https://github.com/oka4shi/pocket-to-cosense.git
   cd pocket-to-cosense
   ```
2. 仮想環境(venv)を作成し依存ライブラリをインストールする
   ```bash
    python3 -m venv .venv
    source .venv/bin/activate
    pip install -r requirements.txt
    ```

3. PocketのConsumer Keyを環境変数に設定する
    ```bash
    export POCKET_CONSUMER_KEY=xxxxxxxxxxxxxxxxxxxxxxxxx
    ```

4. 8080番のポートが使用中でないことを確認しアプリケーションを実行する
    ※OAuthのRedirect URIが http://localhost:8080 に設定されているため
    ```bash
    python main.py
    ```

5. ターミナルに表示されるURLをブラウザで開き、Pocketの認証を行い、待つ
6. output/以下にjsonファイルが出力されていることを確認する


### Cosenseにjsonをインポート
1. 左上のメニューからProject Settingsを開く
2. **インポート前にかならずバックアップを取得しておく**
3. Page Dataタブを開き、Import Pagesの部分で先程のjsonファイルを選択する


## テンプレートの編集
template.txtを編集することで、Cosenseにインポートされるページの内容をカスタマイズ可能です。
jinja2を使用して変数を埋め込みできます。

### 使用できる変数
- [/v3/getエンドポイントのレスポンス](https://getpocket.com/developer/docs/v3/retrieve#:~:text=The%20JSON%20response%20will%20include%20a%20list%20object.%20This%20object%20will%20contain%20all%20of%20the%20items%20that%20matched%20your%20retrieval%20request.%20Each%20item%20may%20or%20may%20not%20contain%20the%20following%20information:)

- `title`: タイトル(重複しないし、空でもない)
- `url`: URL

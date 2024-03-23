# 事前学習用のコーパスを作るパイプライン for BTM

# 環境構築
- [setup.sh](./setup.sh)
    - minicondaで環境構築するためのscript

# 日本語のCommonCrawlデータを統合
## 1. 事前ダウンロード
- webコーパスを事前にダウンロードしておきます｡
 - 一晩くらいはかかります
- download_scriptフォルダ内のscriptを実行すれば処理が進みます
    - コーパスごとに独立に実行できます
    - jsonl.gzで分割圧縮します
    - 700 GB程度(for mc4,oscar,cc100,shisa)
~~~
#はじめの処理
cd data
mkdir original_dump
cd ../download_script

#データベースのダウンロード 
bash mc4_ja.sh
bash oscar.sh
bash cc100.sh
bash shisa.sh
bash jap2010.sh
~~~


## 2. gzファイルの一覧取得
- gzファイルの一覧を[temp/gz_list.txt](./codes/temp/gz_list.txt)に書き出します。
~~~
conda activate textprocess
cd web_codes
python 1_search_gz_list.py

~~~

## 自動実行
- 以下の3,4,...を自動実行するscriptです｡
~~~
bash auto.sh
~~~

## 3. クラスタリングモデルの学習
- [教師なしクラスタリングのためのモデルを学習します](./codes/train_classifier.ipynb)
- 人間のためのカテゴライズというよりは、dedupの計算時間を削減することが今回の目的です｡
    - dedupの計算コストや必要メモリが、naiveにはN^2に比例するため
- クラスタ数は大きめが良いかもしれません
    - 10-20分程度で終わります (学習データ数次第です。)

## 4. クリーン　&　クラスタリング
- クリーンしてクラスタリングします
- [categorized](./data/categorized)フォルダに生成されます。
    - 16並列処理で1日弱、かかりました。 (1プロセスあたり10gbほどramを消費します)
    - 700GB程度


~~~
rm -rf ../data/categorized #必要に応じて初期化
rm -rf temp/fin   #終了済みファイルリストを必要に応じて初期化
python clean_and_clustering.py 16 # 数学は並列処理の数
~~~

## 5. 重複削除
- カテゴリ別に重複削除をしていきます。
    - 計算コストが、naiveにはO(N^2)なので、時間がかかります。
    - 前述の通り、Nを小さくするための策の一つとして、一つ前のstepでクラスタリングしています。
- 700 GBに対して、50並列で1日ほど
    - 10000クラスタリングにした場合です
        - RAMは28GB程度
    - 10クラスタリングとかだと、必要RAMが数十倍以上になるので注意
        - 重複の比較のための、テキスト(のキャッシュ)データをプロセスが大量に保持しなければならないため
        - その分、並列にまわせるプロセスの数が減り、より時間がかかる
    - dedup後は650 GB
~~~
rm -rf ../data/dedup_categorized #必要に応じて初期化
python dedup.py 50 # 数値は並列処理の数
~~~


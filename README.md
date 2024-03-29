# 事前学習用のコーパスを作るパイプライン for BTM

# 環境構築
- [setup.sh](./setup.sh)
    - minicondaで環境構築するためのscript

# [1. 日本語のCommonCrawlデータを統合](./01web_codes/)
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
cd ../00download_script

#データベースのダウンロード 
bash mc4_ja.sh
bash oscar.sh
bash cc100.sh
bash shisa.sh
bash jap2010.sh
bash commoncrawl.sh
~~~


## 2. gzファイルの一覧取得
- gzファイルの一覧を[temp/gz_list.txt](./01web_codes/temp/gz_list.txt)に書き出します。
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
- [教師なしクラスタリングのためのモデルを学習します](./01web_codes/train_classifier.ipynb)
- 人間のためのカテゴライズというよりは、dedupの計算時間を削減することが今回の目的です｡
    - dedupの計算コストや必要メモリが、naiveにはN^2に比例するため
- クラスタ数は大きめが良いかもしれません
    - 10-20分程度で終わります (学習データ数次第です。)
~~~
python 2_train_classifier.py
~~~
## 4. クリーン　&　クラスタリング
- クリーンしてクラスタリングします
- [categorized](./data/categorized)フォルダに生成されます。
    - 16並列処理で1日弱、かかりました。 (1プロセスあたり10gbほどramを消費します)
    - 700GB程度


~~~
rm -rf ../data/categorized #必要に応じて初期化
rm -rf temp/fin   #終了済みファイルリストを必要に応じて初期化
python 3_clean_and_clustering.py 16 # 数学は並列処理の数
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
    - dedup後は650 GB (for mc4,cc100,oscar, shisa)
        - 466,593,931 articles 
        - 8831060 files 
~~~
rm -rf ../data/dedup_categorized #必要に応じて初期化
python 4_dedup.py 50 # 数値は並列処理の数
~~~

## 6. 件数の確認
python 5_count_articles.py

# [2. あらゆるテキストを統合したjsonlを作る](./20integrate_texts/)
- [dict](./20integrate_texts/dataset_dict.py)を更新する
- [データのバランス](./20integrate_texts/check_distribution.ipynb)を確認する
- 統合する
~~~
python integrate_dataset.py
~~~

## 7.[トークナイズ](./30tokenize/)
- 以下の処理は､GPUサーバーでなくても行えるので､ここのrepositoryに含めても良いように思われる
    - トークナイザーの学習
    - textのtokenize

# TODO
## 入れたいデータ
- 英語common crawl (CulturaX?)
- 対訳?
- Wiki**系
- 学術論文
- pdf抽出のデータ
- code関連
- ...


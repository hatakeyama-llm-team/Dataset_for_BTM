# 事前学習用のコーパスを作るパイプライン for BTM
# マニュアル類はあまり整備できてません...

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
- parquetにも対応しています｡
- TODO: [code](./01web_codes/1_search_gz_list.py)中で参照するparquetのパスが､変な場所でハードコードされている
~~~
conda activate textprocess
cd web_codes
python 1_search_gz_list.py

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
    - 16並列処理で3日ほど、かかりました。 (1プロセスあたり10gbほどramを消費します)
    - 960GB程度
- TODO: 突貫で作ったコードのため､同じテキストに対して何度も形態素解析を行うなど､処理上の無駄が多い

~~~
rm -rf ../data/categorized #必要に応じて初期化
rm -rf temp/fin   #終了済みファイルリストを必要に応じて初期化
python 3_clean_and_clustering.py 32 # 数学は並列処理の数
python 3_clean_and_clustering_via_datasets # datasetsライブラリから読み込める､軽めのデータ
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
- フォルダ内を参照

# 使われている日本語系コーパス
- 雑多なweb系
    - [mc4-ja](https://huggingface.co/datasets/allenai/c4)
    - [cc100](https://data.statmt.org/cc-100/)
    - [Oscar](https://huggingface.co/datasets/oscar)
    - [Shisa](https://huggingface.co/datasets/augmxnt/shisa-pretrain-en-ja-v1)
    - [Japanese2010](https://huggingface.co/datasets/hatakeyama-llm-team/japanese2010)
- 独自収拾のCommonCrawl(日本語ドメイン)
    - WARCから1 snapshot (2021?)
    - WETから5 snapshot (2020,2021,2022,2023,2024)
    - [CommonCrawlPDF(ja)](https://huggingface.co/datasets/hatakeyama-llm-team/CommonCrawlPDFJa)
- 特定のドメイン(一部はまだ非公開)
    - [NHK News](https://huggingface.co/datasets/hatakeyama-llm-team/nhk-news-170k)
    - [NHK school](https://huggingface.co/datasets/hatakeyama-llm-team/nhk_for_school_outline)
    - [青空文庫](https://huggingface.co/datasets/globis-university/aozorabunko-clean)
    - [国会議事録]()
    - [Wikipedia-ja](https://huggingface.co/datasets/hpprc/wikipedia-20240101)
    - [Wikipediaから自動生成したQA](https://huggingface.co/datasets/alfredplpl/wikipedia-qa-ja-1m)
    - [J-ResearchCorpus](https://huggingface.co/datasets/kunishou/J-ResearchCorpus/viewer/default/train)
    - [Cosmopedia-ja](https://huggingface.co/datasets/kunishou/cosmopedia-100k-ja-preview)
    - [WikiBook-ja](https://huggingface.co/datasets/hatakeyama-llm-team/WikiBookJa)
    - [Novels-ja](https://huggingface.co/datasets/atsushi3110/novels-ja)
    - [CodingBlog-ja](https://huggingface.co/datasets/atsushi3110/coding-blog-ja)
    - [日英コーパス](https://huggingface.co/datasets/atsushi3110/en-ja-parallel-corpus-augmented)
    - [Soda-ja](https://huggingface.co/datasets/atsushi3110/soda-ja-instruction)
    - [Shosetsu711K](https://huggingface.co/datasets/RyokoAI/Syosetu711K)
    - [JapeneseNews](https://huggingface.co/datasets/atsushi3110/news-ja)
    - [light-novel-4m](https://huggingface.co/datasets/isek-ai/light-novel-4m)
    - [JetCopper-10B](https://huggingface.co/datasets/sudy-super/JetCopper-10B)
# 使われている英語・コード系コーパス
- [peS2o](https://huggingface.co/datasets/allenai/peS2o/viewer/v1/train)
- [wikipedia](https://huggingface.co/datasets/wikipedia)
- [wikibook](https://huggingface.co/datasets/bigscience-data/roots_en_wikibooks)
- [pile_stackexchange](https://huggingface.co/datasets/suolyer/pile_stackexchange)
- [python-codes](https://huggingface.co/datasets/flytech/python-codes-25k)
- [OpenMathInstruct-ja](https://huggingface.co/datasets/kunishou/OpenMathInstruct-1-1.8m-ja)
- [proof-pile-2(python)](https://huggingface.co/datasets/EleutherAI/proof-pile-2)
- [open-web-math](https://huggingface.co/datasets/open-web-math/open-web-math)
- [flan](https://huggingface.co/datasets/Muennighoff/flan)
- [alt-parallel-en-ja](https://huggingface.co/datasets/hpprc/alt-parallel-en-ja)
- [github-code-more-filtering ](https://huggingface.co/datasets/loubnabnl/github-code-more-filtering)
- [Oasst](https://huggingface.co/datasets/sablo/oasst2_curated)
- [Dolly](https://huggingface.co/datasets/databricks/databricks-dolly-15k)
- [Cosmopedia](https://huggingface.co/datasets/HuggingFaceTB/cosmopedia)
- [PMC(CC-BY)](https://huggingface.co/datasets/hatakeyama-llm-team/PMC)
## done
## TODO
- WikiNewsなど
- 学術論文
    - chem
- https://hplt-project.org/datasets/v1.2

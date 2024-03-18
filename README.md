# 日本語のwebデータなどを統合するパイプラインのテスト

- とりあえず､畠山の方でBTMの練習が必要なので､たたき台のscriptを書いていきます｡

# Scripts
- [setup.sh](./setup.sh)
    - minicondaで環境構築するためのscript

# 1. 事前ダウンロード
- webコーパスを事前にダウンロードしておきます｡
 - 一晩くらいはかかります
- download_scriptフォルダ内のscriptを実行すれば処理が進みます
    - コーパスごとに独立に実行できます
    - jsonl.gzで分割圧縮します
    - 700 GB程度
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
~~~


# 2. gzファイルの一覧取得
- gzファイルの一覧を[temp/gz_list.txt](./codes/temp/gz_list.txt)に書き出します。
~~~
conda activate textprocess
cd codes
python search_gz_list.py

~~~

# 自動実行
- 3,4,...を自動実行するscript
~~~
bash auto.sh
~~~

# 3. クラスタリングモデルの学習
- [教師なしクラスタリングのためのモデルを学習します](./codes/train_classifier.ipynb)
- dedupの計算時間を削減するため、クラスタ数は大きめ(100?)が良いかもしれません
    - 10-20分程度で終わります (学習データ数次第です。)

# 4. クリーン　&　クラスタリング
- クリーンしてクラスタリングします
- [categorized](./data/categorized)フォルダに生成されます。
    - 16並列処理で1日弱、かかりました。 (1プロセスあたり10gbほどramを消費します)
    - 700GB程度


~~~
rm -rf ../data/categorized #必要に応じて初期化
rm -rf temp/fin   #終了済みファイルリストを必要に応じて初期化
python clean_and_clustering.py 16 # 数学は並列処理の数
~~~

# 5. 重複削除
- カテゴリ別に重複削除をしていきます。
    - 計算コストが、naiveにはO(N^2)なので、時間がかかります。
    - Nを小さくするための策の一つとして、一つ前のstepでクラスタリングしています。
    - 処理が進むにつれ､使用メモリが増えていくので注意

~~~
python dedup.py 16 # 数値は並列処理の数
~~~
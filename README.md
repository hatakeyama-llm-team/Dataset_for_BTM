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

# 3. クラスタリングモデルの学習
- [教師なしクラスタリングのためのモデルを学習します](./codes/train_classifier.ipynb)

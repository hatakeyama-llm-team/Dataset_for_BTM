# 日本語のwebデータなどを統合するパイプラインのテスト

- とりあえず､畠山の方でBTMの練習が必要なので､たたき台のscriptを書いていきます｡

# Scripts
- [setup.sh](./setup.sh)
    - minicondaで環境構築するためのscript

# 事前ダウンロード
- webコーパスを事前にダウンロードしておきます｡
- download_scriptフォルダ内のscriptを実行すれば処理が進みます
    - コーパスごとに独立に実行できます
    - jsonl.gzで分割圧縮します
~~~
#はじめの処理
cd data
mkdir original_dump
cd ../download_script

#データベースのダウンロード (独立に実行可能。1日くらいかかるかも)
bash mc4_ja.sh
bash oscar.sh
bash cc100.sh
bash shisa.sh
~~~

# 日本語のwebデータなどを統合するパイプラインのテスト

- とりあえず､畠山の方でBTMの練習が必要なので､たたき台のscriptを書いていきます｡

# Scripts
- [setup.sh](./setup.sh)
    - minicondaで環境構築するためのscript

# 事前ダウンロード
- webコーパスを事前ダウンロードしておきます｡
~~~
cd data
mkdir original_dump
cd original_dump

#mc4-ja
GIT_LFS_SKIP_SMUDGE=1 git clone https://huggingface.co/datasets/allenai/c4
cd c4
git lfs pull --include "multilingual/c4-ja.*.json.gz"

#cc100
wget https://data.statmt.org/cc-100/ja.txt.xz

#shisa
wget https://huggingface.co/datasets/augmxnt/shisa-pretrain-en-ja-v1/resolve/main/dataset.parquet

mkdir oscar
#oscar
conda activate textprocess
#cd ../../
#python dump_oscar.py

~~~
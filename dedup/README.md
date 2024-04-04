# Dedupをするためのコード

# [こちら](https://github.com/if001/dedup_sentence)のrepoを参考に実装しました｡

## Setup
~~~
sudo apt install nlohmann-json3-dev
git clone https://github.com/aappleby/smhasher.git
git clone https://github.com/Tencent/rapidjson/
#compile
g++ -o deduplicate deduplicate.cpp smhasher/src/MurmurHash3.cpp -I./smhasher/src -I./rapidjson/include/rapidjson
~~~

### 設定
 [ソースファイル](./deduplicate.cpp)中のTHRESHOLDを変えることで､重複の基準を変更できます
- SIMILARITY_THRESHOLD 0.8

# 使用
- ./deduplicate {jsonが大量に入ったフォルダパス} {dedupしたjsonのフォルダ}

- 注意
    - jsonlの最後の行には空白行が必要

~~~
# コマンド例
./deduplicate ../data/categorized/2 ../data/dedup_test/2
~~~

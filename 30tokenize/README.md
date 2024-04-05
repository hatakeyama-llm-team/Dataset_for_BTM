# トークナイザーの学習とtokenize

## setup
- Docker
~~~
#image構築
sudo docker build -t llm .

#実行
sudo docker run --shm-size='1gb' -it -p 8899:8888 -v /data:/data -v .:/home/llm llm bash 

#初回はmegatron-deepspeedを入れる
sudo chmod -R 777 llm
sudo chmod -R 777 /data
cd llm
conda activate scr
git clone https://github.com/hotsuyuki/Megatron-DeepSpeed
cd Megatron-DeepSpeed/
git fetch origin && git checkout refs/tags/ucllm_nedo_dev_v20240205.1.0
python setup.py install
cd ../

#yq
pip install yq==3.2.3
sudo apt-get install jq -y

#apex
git clone https://github.com/NVIDIA/apex
cd apex
git fetch origin && git checkout refs/tags/23.08
pip install -v --disable-pip-version-check --no-cache-dir --no-build-isolation --config-settings "--build-option=--cpp_ext" --config-settings "--build-option=--cuda_ext" ./
cd ../


~~~

## [Config](./config.yaml)の編集
- jsonのパスなどを設定する

## トークナイザーの学習
- 6 gbのテキストに対して､ ramは30gbほど使いました｡
- でかすぎると､ramが足りなくなります
~~~
python 1_train_sentencepiece_tokenizer.py
~~~

## トークナイズ
~~~
bash 2_tokenize.sh
~~~


## トークン数の確認
- 本当は並列化した方が良い
~~~
python count_tokens.py
~~~


## ファイル分割と転送
- tokenizeしたファイルを､他のサーバーに転送する場合などに用いる

### 分割例
~~~
split -b 5000M tokenized_text_document.bin split-
~~~

## 転送例
~~~
cd /data/hatakeyama/python/llm_corpus/
split -b 1000M tokenized_text_document.bin split-

rsync -avz tokenized_text_document.idx 192.168.128.16:/home/hatakeyama/python/llm/data/text/tokenized_text_document.idx
rsync -avz split-* 192.168.128.16:/home/hatakeyama/python/llm/data/text/split-*


rsync -avz tokenizer 192.168.128.16:/home/hatakeyama/python/llm/models/tokenizers
~~~

## 統合
~~~
cat split-* > tokenized_text_document.bin
~~~


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
~~~
python 1_train_sentencepiece_tokenizer.py
~~~

## トークナイズ
~~~
bash 2_tokenize.sh
~~~

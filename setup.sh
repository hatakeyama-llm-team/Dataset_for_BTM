conda create -n textprocess -y
conda activate textprocess
conda install pip -y
pip install datasets==2.18.0

#mecab 日本語の解析に使います
sudo apt install mecab -y
sudo apt install libmecab-dev -y
sudo apt install mecab-ipadic-utf8 -y
pip install mecab==0.996.3 
pip install ja-sentence-segmenter==0.0.2
pip install hojichar==0.9.0

#text clustering
pip install gensim==4.3.2
pip install scikit-learn==1.4.1.post1 


#model download
cd data
mkdir model
cd model
wget https://dl.fbaipublicfiles.com/fasttext/vectors-crawl/cc.ja.300.bin.gz
gzip -d cc.ja.300.bin.gz
cd ../../
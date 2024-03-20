conda activate textprocess
cd codes

#分類モデルの訓練
python train_classifier.py

#分類モデルを用いてファイルを分類
rm -rf ../data/categorized #必要に応じて初期化
rm -rf temp/fin   #終了済みファイルリストを必要に応じて初期化
python clean_and_clustering.py 16 # 数学は並列処理の数

#dedup
rm -rf ../data/dedup_categorized #必要に応じて初期化
python dedup.py 16 # 数値は並列処理の数
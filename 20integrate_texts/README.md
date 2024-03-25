# データセットのロード
## ここでは､HuggingFaceのDatasetsライブラリなどを諸々loadして､一つのjsonlを書き出します
- [loader](./src/loaders.py)を定義しておきます｡
- 用いるDatasetは､dataset_dictに記入していきます｡

## データを決めます｡
- どのデータを用いるかについては､[dataset_dict](./dataset_dict.py)を直接いじって作業します｡
- [notebook](./check_distribution.ipynb)で分布なども確認出来ます｡

## 実行
~~~
python integrate_dataset.py
~~~


# クリーニングしたwebテキストをクラスタリングするモデルを作る
# このフェーズでのクラスタリングの主目的は､dedupの計算コスト(N^2)を下げること｡
# dedup用に､大きくしておくのが吉
from src.classify.Text2Vec import Text2Vec, texts2classes
import joblib
import random
import numpy as np
from tqdm import tqdm
from gensim.models.fasttext import load_facebook_model
from sklearn.cluster import KMeans, MiniBatchKMeans
from src.load_gz import read_gzip_json_file
from datasets import load_dataset
from src.cleaner.auto_cleaner import clean_text
from sklearn.metrics import pairwise_distances
n_clusters = 10000


print("imported libraries")


txt = "こんにちは､げんきですか?研究を "
clean_text(txt)

# gzファイルの一覧を取得
with open("temp/gz_list.txt", "r") as f:
    gz_list = f.readlines()

gz_list = [i for i in gz_list if i != "\n"]
gz_list = [i.replace("\n", "") for i in gz_list]
gz_list

lines = []
path = gz_list[0]
for article in read_gzip_json_file(path):
    text = article.get('text', '')  # 'text'キーからテキストデータを取得
    lines.append(text)

# %%
lines[:3]

# %%
random.shuffle(gz_list)

# クラスタリングに使うデータベースの数
n_gz = 100

train_datasets = gz_list[:n_gz]

# %%

# 各データセットごと､N件のデータを取得
max_articles = 1000
cleaned_text = []

for path in tqdm(train_datasets):
    lines = []
    print("loading ", path)
    for article in read_gzip_json_file(path):
        text = article.get('text', '')  # 'text'キーからテキストデータを取得
        lines.append(text)

    cnt = 0
    for text in (lines):
        # text=next(dataset_iter)["text"]
        text = clean_text(text)

        if text != "":
            cleaned_text.append(text)
            cnt += 1
            if cnt >= max_articles:
                break


t2v = Text2Vec(load_facebook_model('../data/model/cc.ja.300.bin'))

# %%
title_vecs = [t2v.text2vec(i) for i in tqdm(cleaned_text)]

# %%
title_vecs = np.array(title_vecs)
# k-meansクラスタリング
print("clustering...")
kmeans = MiniBatchKMeans(n_clusters=n_clusters, random_state=1).fit(title_vecs)


# 各データポイントが割り当てられたクラスタのインデックスを取得
labels = kmeans.labels_

# 各クラスタに含まれるデータポイントの数を計算
cluster_counts = dict((i, list(labels).count(i)) for i in range(n_clusters))

print(cluster_counts)

# %%
# クラスタのセントロイドを取得
# 仮に title_vecs がデータセットの特徴ベクトル、cleaned_text がそれに対応するクリーンなテキストデータを表すとします。
# n_clusters には、生成したいクラスタの数を指定します。
"""
centroids = kmeans.cluster_centers_

# 各クラスタに属するデータポイントのインデックスを取得
cluster_indices = {i: np.where(kmeans.labels_ == i)[
    0] for i in range(n_clusters)}

for cluster_id, indices in cluster_indices.items():
    # クラスタ内のデータポイントとセントロイドとの距離を計算
    distances = pairwise_distances(
        title_vecs[indices], [centroids[cluster_id]])
    # 距離が最も小さい上位5つのデータポイントを選択
    closest_indices = np.argsort(distances[:, 0])[:5]

    print(f"Cluster {cluster_id}:")
    for idx in closest_indices:
        # クラスタ内で選択されたデータポイントの実際のインデックス
        actual_idx = indices[idx]
        # テキストが長い場合は100文字に制限し、改行を削除
        short_txt = cleaned_text[actual_idx].replace('\n', '')[:100]
        print(f"{short_txt}")
    print("\n")
"""
# %%
# save model
joblib.dump(kmeans, "../data/model/kmeans.pkl")

# %%
# target_texts = cleaned_text[:10]


# print(texts2classes(target_texts, t2v, kmeans))

# %%

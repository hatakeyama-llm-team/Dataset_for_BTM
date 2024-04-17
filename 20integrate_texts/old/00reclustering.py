# %%
from sklearn.cluster import MiniBatchKMeans, KMeans
import pickle
import subprocess
import os
from gensim.models.fasttext import load_facebook_model
import numpy as np
from tqdm import tqdm
import random
import glob
import json
import sys
if True:
    sys.path.append("../01web_codes")

from src.classify.Text2Vec import Text2Vec
from loaders.CommonCrawlDataset import CommonCrawlDataset

# %% [markdown]
# # BTM用に､10000分割したテキストをre-clusteringするための分配処理

# %%
# loaderの設定などの練習

# %%
# 10000分割されたjsonlファイルのパスを取得


jsonl_path_list = glob.glob("../data/dedup_categorized/*/*.jsonl")
random.shuffle(jsonl_path_list)
cid_to_path_list = {}
for jsonl_path in jsonl_path_list:
    cid = jsonl_path.split("/")[-2]
    if cid not in cid_to_path_list:
        cid_to_path_list[cid] = []
    cid_to_path_list[cid].append(jsonl_path)

# %%
# 代表的な*件を取得
max_texts = 10
cid_to_texts = {}
for cid, path_list in tqdm(cid_to_path_list.items()):
    texts = []
    for path in path_list:
        cnt = 0
        with open(path) as f:
            for i, line in enumerate(f):
                t = json.loads(line)["text"]
                if len(t) < 10:
                    continue
                texts.append(t)
                cnt += 1
                if cnt > max_texts:
                    break
    cid_to_texts[cid] = texts

# %%

t2v = Text2Vec(load_facebook_model('../data/model/cc.ja.300.bin'))

# %%
# 各カテゴリのテキストをベクトル化
cid_to_vecs = {}
check_length = 100
for cid, texts in tqdm(cid_to_texts.items()):
    vecs = [t2v.text2vec(i[:check_length]) for i in texts]
    vecs = np.array(vecs)
    vecs = np.mean(vecs, axis=0)
    cid_to_vecs[cid] = vecs


# %%
vec_array = list(cid_to_vecs.values())
vec_array = [i for i in vec_array if i.shape == (300,)]
vecs.shape

# %%
n_clusters = 5
vec_array = np.array(vec_array).astype(np.double)
# k-meansクラスタリング
print("clustering...")
kmeans = KMeans(n_clusters=n_clusters, random_state=1).fit(vec_array)

# %%
cid_to_label = {}
for cid, vec in cid_to_vecs.items():
    try:
        label = kmeans.predict([vec])[0]
        cid_to_label[cid] = label
    except Exception as e:
        print(cid, e)

# %%
label_to_path_list = {}
for cid, label in cid_to_label.items():
    if str(label) not in label_to_path_list:
        label_to_path_list[str(label)] = []
    path = f"../data/dedup_categorized/{cid}/*.jsonl"
    label_to_path_list[str(label)].append(path)


# %%
with open("../data/clustered_path.json", "w") as f:
    json.dump(label_to_path_list, f, indent=4)

# %%
# 行数を数える

with open("../data/clustered_path.json") as f:
    label_to_path_list = json.load(f)


label_to_article_count = {}

for label, path_list in tqdm(label_to_path_list.items()):
    loader = CommonCrawlDataset(label_to_path_list[label])
    loader = iter(loader)
    while True:
        try:
            next(loader)
        except:
            records = loader.count
            label_to_article_count[label] = records
            break

label_to_article_count

# %%

with open("../data/clustered_n.json", "w") as f:
    json.dump(label_to_article_count, f, indent=4)

# %%
n_clusters = 5
for i in range(n_clusters):
    print("--------\ncluster: ", i)
    cc1_loader = CommonCrawlDataset(label_to_path_list[str(i)])
    cc1_iter = iter(cc1_loader)
    for i in range(10):
        print(next(cc1_iter))

# %%
# モデル保存
with open("../data/second_kmeans_model.pkl", "wb") as f:
    pickle.dump(kmeans, f)

# %%

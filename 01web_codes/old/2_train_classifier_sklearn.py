
# クリーニングしたwebテキストをクラスタリングするモデルを作る
# このフェーズでのクラスタリングの主目的は､dedupの計算コスト(N^2)を下げること｡
# dedup用に､大きくしておくのが吉
from src.classify.Text2Vec import Text2Vec
import joblib
from src.classify.TfidfClassifier import prepare_pileline
import json

# クラスタの数
n_clusters = 10000
n_clusters = 20


text_path = "temp/texts.jsonl"
with open(text_path, "r") as f:
    lines = f.readlines()
cleaned_text = [json.loads(i)["text"] for i in lines]
cleaned_text = list(set(cleaned_text))
# k-meansクラスタリング
print("clustering...")

kmeans = prepare_pileline(n_clusters).fit(cleaned_text)
labels = kmeans.named_steps['cluster'].labels_


# 各クラスタに含まれるデータポイントの数を計算
cluster_counts = dict((i, list(labels).count(i)) for i in range(n_clusters))

print(cluster_counts)

# save model
joblib.dump(kmeans, "../data/model/kmeans.pkl")

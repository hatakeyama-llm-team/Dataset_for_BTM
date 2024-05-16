# 必要なライブラリをインポート
from gensim.models import KeyedVectors
from gensim.models.fasttext import load_facebook_model
from sklearn.cluster import MiniBatchKMeans
import joblib
import numpy as np
import json

# ヘルパークラスと関数のインポート
from src.classify.Text2Vec import Text2Vec

# 定数の設定
N_CLUSTERS = 10000
TEXT_PATH = "temp/texts.jsonl"
MODEL_PATH = "../data/model/entity_vector/entity_vector.model.bin"
MODEL_SAVE_PATH = "../data/model/kmeans.pkl"

# テキストの読み込みと前処理
def load_and_clean_texts(path):
    with open(path, "r") as file:
        lines = file.readlines()
    cleaned_texts = list({json.loads(line)["text"] for line in lines})
    return cleaned_texts

# ベクトル表現の取得
def get_text_vectors(texts, model_path):
    model = KeyedVectors.load_word2vec_format(model_path, binary=True)
    t2v = Text2Vec(model=model, dim=200)
    text_vecs = np.array([t2v.text2vec(text) for text in texts])
    return text_vecs

# k-meansクラスタリングの実行
def cluster_texts(text_vecs, n_clusters):
    kmeans = MiniBatchKMeans(n_clusters=n_clusters, random_state=1)
    kmeans.fit(text_vecs)
    return kmeans

# クラスタ情報の保存
def save_model(kmeans, save_path):
    joblib.dump(kmeans, save_path)

# メインの実行部
if __name__ == "__main__":
    cleaned_texts = load_and_clean_texts(TEXT_PATH)
    text_vecs = get_text_vectors(cleaned_texts, MODEL_PATH)
    kmeans = cluster_texts(text_vecs, N_CLUSTERS)
    save_model(kmeans, MODEL_SAVE_PATH)

    # クラスタの情報を出力（省略可能）
    cluster_counts = {i: list(kmeans.labels_).count(i) for i in range(N_CLUSTERS)}
    print(cluster_counts)

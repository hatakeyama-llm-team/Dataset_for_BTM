from src.loaders import *
import json
# 出力パス
output_path = "/data/hatakeyama/python/llm_corpus/corpus.jsonl"
scale = 1  # 練習時はscaleを小さくする

# 自動でクラスタリングされたコーパス群の読み込み
n_clusters = 5
# クラスタリングされたweb系テキストのデータセット
with open("../data/clustered_path.json", "r") as f:
    label_to_path_list = json.load(f)

# データ数
with open("../data/clustered_n.json", "r") as f:
    label_to_article_count = json.load(f)

cc_loader_list = []
for label, path in label_to_path_list.items():
    loader = CommonCrawlDataset(label_to_path_list[label])
    cc_loader_list.append(loader)


# stage_ratioは､各レコードの､各stageごとのデータの振り分け具合を示す

dataset_dict = {

    # 英語のwikipedia
    "wiki(en)": {
        "loader": wiki_en_loader,
        "n_records": int(458000/scale),
        "stage_ratio": [0.05]*6,
    },
    #
    "ja0": {
        "loader": cc_loader_list[0],
        "n_records": int(label_to_article_count["0"]/scale),
        "stage_ratio": [0.05, 1, 0.05, 0.05, 0.05, 0.05],
    },
    "ja1": {
        "loader": cc_loader_list[1],
        "n_records": int(label_to_article_count["1"]/scale),
        "stage_ratio": [0.05, 0.05, 1, 0.05, 0.05, 0.05],
    },
    "ja2": {
        "loader": cc_loader_list[2],
        "n_records": int(label_to_article_count["2"]/scale),
        "stage_ratio": [0.05, 0.05, 0.05, 1, 0.05, 0.05],
    },
    "ja3": {
        "loader": cc_loader_list[3],
        "n_records": int(label_to_article_count["3"]/scale),
        "stage_ratio": [0.05, 0.05, 0.05, 0.05, 1, 0.05],
    },
    "ja4": {
        "loader": cc_loader_list[4],
        "n_records": int(label_to_article_count["4"]/scale),
        "stage_ratio": [0.05, 0.05, 0.05, 0.05, 0.05, 1],
    },







}

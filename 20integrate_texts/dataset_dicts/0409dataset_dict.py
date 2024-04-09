from loaders.loaders import *
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
print(label_to_article_count)
cc_loader_dict = {}
for label, path in label_to_path_list.items():
    loader = CommonCrawlDataset(label_to_path_list[label])
    cc_loader_dict[label] = loader


dataset_dict = {
    # ----------------------------
    # stage 1

    # 英語のwikipedia
    "wiki(en)": {
        "loader": wiki_en_loader,
        "n_records": int(6458000/scale),
        "stage_ratio": [0.05, 7, 0.05, 0.05, 0.05, 0.05, 0.05],
    },

    # 英語の雑多なテキスト: もっときれいなら他のものに変更する
    "culturaX(en)": {
        "loader": culturax_loader,
        "n_records": int(10**7/scale),
        "stage_ratio": [0.05, 7, 0.05, 0.05, 0.05, 0.05, 0.05],
    },

    # pythonの英語のcodeのinstructionを事前学習用に強引に突っ込む
    "PythonCodes": {
        "loader": python_code_loader,
        "n_records": int(49000/scale),
        "stage_ratio": [0.1, 7, 0.1, 0.1, 0.05, 0.05, 0.05],
    },
    "OpenMathJa": {
        "loader": open_math_loader,
        "n_records": int(1820000/scale),
        "stage_ratio": [0.1, 7, 0.1, 0.1, 0.05, 0.05, 0.05],
    },

    # ----------------------------
    # stage 2以降
    # 日本語の雑多な文章
    #
    "ja0": {
        "loader": cc_loader_dict["0"],
        "n_records": int(label_to_article_count["0"]/scale-1000),
        "stage_ratio": [0.05, 0.05, 1, 0.05, 0.05, 0.05, 0.05],
    },
    "ja1": {
        "loader": cc_loader_dict["1"],
        "n_records": int(label_to_article_count["1"]/scale-1000),
        "stage_ratio": [0.05, 0.05, 0.05, 1, 0.05, 0.05, 0.05],
    },
    "ja2": {
        "loader": cc_loader_dict["2"],
        "n_records": int(label_to_article_count["2"]/scale-1000),
        "stage_ratio": [0.05, 0.05, 0.05, 0.05, 1, 0.05, 0.05],
    },
    "ja3": {
        "loader": cc_loader_dict["3"],
        "n_records": int(label_to_article_count["3"]/scale-1000),
        "stage_ratio": [0.05, 0.05, 0.05, 0.05, 0.05, 1, 0.05],
    },
    "ja4": {
        "loader": cc_loader_dict["4"],
        "n_records": int(label_to_article_count["4"]/scale-1000),
        "stage_ratio": [0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 1],
    },





}

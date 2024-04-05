from src.loaders import *

# 出力パス
output_path = "/data/hatakeyama/python/llm_corpus/corpus.jsonl"
scale = 1  # 練習時はscaleを小さくする

# stage_ratioは､各レコードの､各stageごとのデータの振り分け具合を示す

dataset_dict = {

    # ----------------------------
    # stage 3
    # 上質なテキスト

    # 英語のwikipedia
    "wiki(en)": {
        "loader": wiki_en_loader,
        "n_records": int(1500000/scale),
        "stage_ratio": [1, ],
    },


    # wikipedia
    "wiki(ja)": {
        "loader": cleaned_wiki_loader,
        "n_records": int(1390000/scale),
        "stage_ratio": [1,],
    },

    # nhk news
    "NHK-news": {
        "loader": nhk_news_loader,
        "n_records": int(168800/scale),
        "stage_ratio": [1,],
    },

    # nhk school
    "NHK-school": {
        "loader": NHKSchool_loader,
        "n_records": int(6200/scale),
        "stage_ratio": [1,],
    },

    # 青空文庫
    "aozora-bunko": {
        "loader": aozora_bunko_loader,
        "n_records": int(16900/scale),
        "stage_ratio": [1,],
    },

    # 日本語の学術論文
    "japanese-ronbun": {
        "loader": j_research_loader,
        "n_records": int(3200/scale),
        "stage_ratio": [1,],
    },


}

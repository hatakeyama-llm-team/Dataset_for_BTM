from src.loaders import *

# 出力パス
output_path = "/data/hatakeyama/python/llm_corpus/corpus.jsonl"
scale = 10  # 練習時はscaleを小さくする

# stage_ratioは､各レコードの､各stageごとのデータの振り分け具合を示す

dataset_dict = {
    # ----------------------------
    # stage 1

    # 英語のwikipedia
    "wiki(en)": {
        "loader": wiki_en_loader,
        "n_records": int(6458000/scale),
        "stage_ratio": [0.05, 7, 0.05, 0.05],
    },

    # 英語の雑多なテキスト: もっときれいなら他のものに変更する
    "culturaX(en)": {
        "loader": culturax_loader,
        "n_records": int(10**7/scale),
        "stage_ratio": [0.05, 7, 0.05, 0.05],
    },

    # pythonの英語のcodeのinstructionを事前学習用に強引に突っ込む
    "PythonCodes": {
        "loader": python_code_loader,
        "n_records": int(49000/scale),
        "stage_ratio": [1, 7, 1, 0.1],
    },



    # cosmopedia
    # 自動合成されたデータセット｡文章のクオリティは低いが､日英の勉強にはなるかも?
    "Cosmopodia": {
        "loader": cosmo_loader,
        "n_records": int(79800/scale),
        "stage_ratio": [0.25, 7, 1, 0.25],
    },

    # ----------------------------
    # stage 2
    # 日本語の雑多な文章
    "CC(ja)": {
        "loader": CC_ja_loader,
        "n_records": int(46659000/scale),
        "stage_ratio": [0.1, 0.1, 8, 0.1],
    },

    # wikipediaから自動生成された質問集
    "wiki-qa": {
        "loader": wiki_qa_loader,
        "n_records": int(1113000/scale),
        "stage_ratio": [0.1, 0.1, 8, 0.1],
    },

    # ----------------------------
    # stage 3
    # 上質なテキスト

    # wikipedia
    "wiki(ja)": {
        "loader": cleaned_wiki_loader,
        "n_records": int(1390000/scale),
        "stage_ratio": [1, 1, 1, 8],
    },

    # nhk news
    "NHK-news": {
        "loader": nhk_news_loader,
        "n_records": int(168800/scale),
        "stage_ratio": [0.1, 0.1, 0.1, 0.8],
    },
    # nhk school
    "NHK-school": {
        "loader": NHKSchool_loader,
        "n_records": int(6200/scale),
        "stage_ratio": [0.1, 0.1, 0.1, 0.8],
    },
    # 青空文庫
    "aozora-bunko": {
        "loader": aozora_bunko_loader,
        "n_records": int(16900/scale),
        "stage_ratio": [0.1, 0.1, 0.1, 0.8],
    },

    # 日本語の学術論文
    "japanese-ronbun": {
        "loader": j_research_loader,
        "n_records": int(3200/scale),
        "stage_ratio": [0.1, 0.1, 0.1, 0.8],
    },


}

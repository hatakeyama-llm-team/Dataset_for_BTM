
from src.loaders import *

# 出力パス
output_path = "/data/hatakeyama/python/llm_corpus/corpus.jsonl"

dataset_dict = {
    "wiki(ja)": {
        # "loader": wiki_ja_loader, #日本語版のwikipediaのloaderを使います｡
        "loader": cleaned_wiki_loader,  # 日本語版のwikipediaのloaderを使います｡
        "n_records": 1200000,  # 最大件数
        "stage_ratio": [1, 1, 1, 8],  # 各ステージでのデータ配分
    },
    "wiki(en)": {
        "loader": wiki_en_loader,
        "n_records": 3600000,
        "stage_ratio": [0.25, 7, 1, 0.25],
    },
    "CC(ja)": {
        "loader": CC_ja_loader,
        "n_records": 10000000,
        "stage_ratio": [0.1, 0.1, 8, 0.1],  # 各ステージでのデータ配分
    },
}

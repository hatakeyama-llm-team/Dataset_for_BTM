from datasets import load_dataset
from .CleanedJapaneseWikiDataset import CleanedJapaneseWikiDataset
from .CommonCrawlDataset import CommonCrawlDataset
from .CosmopediaDataset import CosmopediaDataset
import os
with open(".env", "r") as f:
    for line in f:
        var = line.split("=")
        os.environ[var[0]] = var[1].strip()

streaming = True


def j_research_loader():
    return load_dataset("kunishou/J-ResearchCorpus", split="train").shuffle()


def aozora_bunko_loader():
    return load_dataset('globis-university/aozorabunko-clean',
                        split="train").shuffle()


def nhk_news_loader():
    # nhk news
    # 168839 records
    return load_dataset("hatakeyama-llm-team/nhk-news-170k", split="train",
                        use_auth_token=os.environ["hf_key"],
                        ).shuffle()


def CC_ja_loader():
    # 雑多なcommon crawl
    return CommonCrawlDataset(jsonl_dir="../data/dedup_categorized/**/*.jsonl",
                              preload_size=100,
                              )


"""
def wiki_ja_loader():
    return load_dataset("hpprc/wikipedia-20240101", split="train",
                        streaming=streaming
                        ).shuffle()
"""


def wiki_en_loader():
    # 英語
    return load_dataset("wikipedia", "20220301.en", split="train",
                        streaming=streaming,
                        ).shuffle()


def mc4_ja_part_loader():
    return load_dataset("izumi-lab/mc4-ja", split='train',
                        # data_files="data/train-00000-of-00416-a74a40664a952804.parquet",
                        streaming=streaming,
                        )


def cleaned_wiki_loader():
    # クリーンされたjapanese wikipedia
    return CleanedJapaneseWikiDataset(streaming=streaming)


def cosmo_loader():
    return CosmopediaDataset()

from datasets import load_dataset
from .loaders import wiki_en_loader
from .CleanedJapaneseWikiDataset import CleanedEngWikiDataset
from .OtherDatasets import *
from .PilePythonDataset import PilePythonDataset

dataset_list = [

    # pes2o: : 67.56M docs, ca. 47 b tokens
    load_dataset("allenai/peS2o", streaming=True, split="train"),

    # wikipedia: 6458000 docs
    CleanedEngWikiDataset(),

    # wikibook: 50k docs
    WikiBookEn(),

    # stack exchange 60k
    PileStackExchange(),
    PileStackExchange(mode="test"),

    # python code 49k
    PythonCodeDataset(),

    # openmathinstruct ja: 1820000 docs
    OpenMathInstructJa(),

    # the pile python dataset
    # 6,098.8 M ?
    PilePythonDataset("../data/original_dump/python/"),
]

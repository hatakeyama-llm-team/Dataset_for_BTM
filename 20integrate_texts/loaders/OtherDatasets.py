
import random
from datasets import load_dataset


class KokkaiDataset:
    def __init__(self, auth_token):
        self.dataset = load_dataset(
            "JINIAC/ParliamentaryProceedings-filtered",
            use_auth_token=auth_token,
            streaming=True,
            split="train")
        self.loader = iter(self.dataset)

    def __iter__(self):
        # イテレータは自分自身を返す
        return self

    def __len__(self):
        return len(self.dataset)

    def __next__(self):
        d = next(self.loader)
        if "発言内容" in d:
            d["text"] = d["発言内容"]
        else:
            d = ""
        return d


class PythonCodeDataset:
    def __init__(self, streaming=True):
        self.dataset = load_dataset(
            "flytech/python-codes-25k",
            split="train").shuffle()
        self.loader = iter(self.dataset)

    def __iter__(self):
        # イテレータは自分自身を返す
        return self

    def __len__(self):
        return len(self.dataset)

    def __next__(self):
        d = next(self.loader)
        out = d["output"].replace("```", "")
        d["text"] = d["instruction"] + d["input"]+"\n"+out
        d["text"] = d["text"].strip()
        return d


class OpenMathInstructJa:
    def __init__(self, ):
        self.dataset = load_dataset(
            "kunishou/OpenMathInstruct-1-1.8m-ja",
            split="train").shuffle()
        self.loader = iter(self.dataset)

    def __len__(self):
        return len(self.dataset)

    def __iter__(self):
        # イテレータは自分自身を返す
        return self

    def __next__(self):
        d = next(self.loader)
        j_q = d["question_ja"]
        j_a = d["generated_solution_ja"]
        txt = j_q+"\n\n"+j_a
        d["text"] = txt
        return d


class WikiBookEn:
    def __init__(self, streaming=True):
        self.dataset = load_dataset(
            "bigscience-data/roots_en_wikibooks",
            split="train", streaming=streaming)
        self.loader = iter(self.dataset)

    def __iter__(self):
        # イテレータは自分自身を返す
        return self

    def __len__(self):
        return len(self.dataset)

    def __next__(self):
        while True:
            d = next(self.loader)
            # UTCが含まれるデータはスキップ｡議論なので｡
            if d["text"].find("UTC") > 0:
                continue
            return d


class PileStackExchange:
    def __init__(self, streaming=True,
                 mode="validation"):
        self.dataset = load_dataset(
            "suolyer/pile_stackexchange",
            split=mode, streaming=streaming)
        self.loader = iter(self.dataset)

    def __iter__(self):
        # イテレータは自分自身を返す
        return self

    def __next__(self):
        d = next(self.loader)
        d["text"] = d["text"].strip()
        return d

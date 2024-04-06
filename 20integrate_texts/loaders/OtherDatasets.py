
import random
from datasets import load_dataset


class PythonCodeDataset:
    def __init__(self, streaming=True):
        self.dataset = load_dataset(
            "flytech/python-codes-25k",
            split="train").shuffle()
        self.loader = iter(self.dataset)

    def __iter__(self):
        # イテレータは自分自身を返す
        return self

    def __next__(self):
        # ランダムな順序で日英を返す
        d = next(self.loader)
        out = d["output"].replace("```", "")
        d["text"] = d["input"]+"\n"+out
        return d

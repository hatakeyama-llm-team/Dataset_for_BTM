import random
import glob
import json
# dedupしたjsonlのファイル群を読み込む

random.seed(1)


class CommonCrawlDataset:
    def __init__(self, jsonl_dir="../data/dedup_categorized/**/*.jsonl",
                 preload_size=100,
                 ):
        self.preload_size = preload_size

        self.web_jsonl_files = glob.glob(jsonl_dir, recursive=True)
        random.shuffle(self.web_jsonl_files)
        self.path_loader = iter(self.web_jsonl_files)
        self.stock_records = iter([])
        self.count = 0

    def __iter__(self):
        return self

    def __next__(self):
        try:
            self.count += 1
            return next(self.stock_records)
        except StopIteration:
            self.load_next_files()
            self.count += 1
            return next(self.stock_records)

    def load_next_files(self):
        # 一定数のファイルを一気に読み込んでおき､shuffleしておく
        self.stock_records = []
        for i in range(self.preload_size):
            with open(next(self.path_loader), "r") as f:
                lines = f.readlines()
                records = [json.loads(line) for line in lines]

            self.stock_records.extend(records)
        random.shuffle(self.stock_records)

        self.stock_records = iter(self.stock_records)

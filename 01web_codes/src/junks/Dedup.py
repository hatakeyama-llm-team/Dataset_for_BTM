import joblib
import os
from hojichar import deduplication, Document
import json
import glob
from tqdm import tqdm


def make_dir(path):
    if not os.path.exists(path):
        os.mkdir(path)


class Deduplicator:
    def __init__(self, hasher, cache_path, init=False):
        self.hasher = hasher
        self.cache_path = cache_path
        if init:
            self.seen = set()
        else:
            try:
                self.seen = joblib.load(self.cache_path)
            except FileNotFoundError:
                print("No cache found, initializing new cache.")
                self.seen = set()

    def is_duplicated(self, text):
        doc = Document(text)
        self.hasher.apply(doc)

        for lsh in doc.dedup_lsh:
            if lsh in self.seen:
                self.seen.add(lsh)
                return True

            self.seen.add(lsh)
        return False

    def save_state(self):
        joblib.dump(self.seen, self.cache_path)


class DedupManager:
    def __init__(self, batch_id, save_batch_size=10000) -> None:
        self.batch_id = batch_id
        self.target_dir = f"../data/categorized/{batch_id}/*.jsonl"
        self.dedup_cache_path = f"../data/cache/{batch_id}.joblib"
        self.manager_path = f"../data/cache/{batch_id}.manager.joblib"
        self.manager_dict = {
            "total_count": 0,
            "files": {},
        }
        self.total_count = 0
        self.save_batch_size = save_batch_size

        make_dir("../data/cache")
        make_dir("../data/dedup_categorized")

        if os.path.exists(self.manager_path):
            self.manager_dict = joblib.load(self.manager_path)

        self.deduplicator = Deduplicator(
            deduplication.GenerateDedupLSH(), self.dedup_cache_path)
        self.total_count = self.manager_dict["total_count"]

    def get_path_list(self):
        return glob.glob(self.target_dir)

    def process_dir(self):
        path_list = self.get_path_list()
        for path in tqdm(path_list):
            self.process_path(path)
        self.save_state()

    def process_path(self, path):
        # ファイルサイズを取得
        size = os.path.getsize(path)
        check_flag = False

        # 新規 or 更新されたファイルについて､dedupを実行するflagを立てる
        if path not in self.manager_dict["files"]:
            self.manager_dict["files"][path] = {
                "size": size,
            }
            check_flag = True
        else:
            if self.manager_dict["files"][path]["size"] != size:
                self.manager_dict["files"][path]["size"] = size
                check_flag = True

        if not check_flag:
            # print("skipped: ", path)
            pass
        else:
            with open(path, "r") as f:
                target_text_list = [json.loads(line)["text"] for line in f]

            cnt = self.total_count//self.save_batch_size
            save_path = f"../data/dedup_categorized/{self.batch_id}/{cnt}.jsonl"
            dir_name = os.path.dirname(save_path)

            make_dir(dir_name)

            for text in target_text_list:
                if not self.deduplicator.is_duplicated(text):
                    with open(save_path, "a") as f:
                        f.write(json.dumps({"text": text},
                                ensure_ascii=False)+"\n")
                        self.total_count += 1
                        self.manager_dict["total_count"] = self.total_count
                    # print("processed: ", path)

    def save_state(self):
        joblib.dump(self.manager_dict, self.manager_path)
        self.deduplicator.save_state()

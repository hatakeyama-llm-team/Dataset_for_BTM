# %%
import argparse
import json
import os
from datasets import load_dataset
from concurrent.futures import ThreadPoolExecutor, as_completed
from src.classify.Text2Vec import Text2Vec, texts2classes
from src.cleaner.auto_cleaner import clean_text
from gensim.models.fasttext import load_facebook_model
import joblib

streaming = True
base_dir = "../data/categorized"
length_threshold = 30  # 短い記事は捨てる

# load models
t2v = Text2Vec(load_facebook_model('../data/model/cc.ja.300.bin'))
kmeans = joblib.load("../data/model/kmeans.pkl")


def make_dir(path):
    if not os.path.exists(path):
        os.mkdir(path)


make_dir(base_dir)

# %%

# %%
batch_size = 10000

parser = argparse.ArgumentParser(
    description="Load a dataset based on the given database name.")
parser.add_argument('database_name', type=str,
                    help='The name of the database to load')
args = parser.parse_args()
database_name = args.database_name


if database_name == "mc4":
    dataset = load_dataset('mc4', 'ja', split='train', streaming=streaming)
elif database_name == "oscar":
    dataset = load_dataset(
        'oscar', 'unshuffled_deduplicated_ja', split='train', streaming=streaming)
elif database_name == "cc100":
    dataset = load_dataset(
        'cc100', lang='ja', split='train', streaming=streaming)
elif database_name == "shisa":
    dataset = load_dataset("augmxnt/shisa-pretrain-en-ja-v1",
                           split="train", streaming=streaming)
else:
    raise ValueError(f"unknown database name: {database_name}")


def proc(docs):
    # docsを処理する関数
    # ここに処理のロジックを実装します
    print(f"Processing {len(docs)} documents...")
    categories = texts2classes(docs, t2v, kmeans)

    for text, category in zip(docs, categories):
        save_dir = f"{base_dir}/{category}"
        make_dir(save_dir)

        data = json.dumps(
            {"db": database_name, "text": text}, ensure_ascii=False)
        with open(f"{save_dir}/{database_name}.jsonl", "a") as f:
            f.write(data+"\n")

    return len(docs)


def main():

    docs = []
    futures = []

    for doc in dataset:
        text = doc["text"]
        text = clean_text(text)
        if len(text) < length_threshold:
            continue

        docs.append(text)
        if len(docs) == batch_size:
            # docsのコピーを作成してprocに渡す
            proc(docs[:])
            # docsをリセット
            docs = []
    """
    with ThreadPoolExecutor(max_workers=5) as executor:
        for doc in dataset:
            text = doc["text"]
            text = clean_text(text)
            if len(text) < length_threshold:
                continue

            docs.append(text)
            if len(docs) == batch_size:
                # docsのコピーを作成してprocに渡す
                docs_copy = docs[:]
                # バッチをproc関数に非同期で渡す
                future = executor.submit(proc, docs_copy)
                futures.append(future)

                # docsをリセット
                docs = []
            # break

        # まだ処理されていないドキュメントがあれば、それも処理する
        if docs:
            futures.append(executor.submit(proc, docs))

        # すべての処理が完了するのを待つ
        for future in as_completed(futures):
            result = future.result()
            print(f"Batch processed with {result} documents.")

    """


if __name__ == "__main__":
    main()

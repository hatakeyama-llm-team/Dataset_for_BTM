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
from src.load_gz import read_gzip_json_file

streaming = True
base_dir = "../data/categorized"
length_threshold = 30  # 短い記事は捨てる
check_length=200 # はじめのlengthだけで分類する

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
parser.add_argument('database_path', type=str,
                    help='The path of the database to load')
args = parser.parse_args()
database_path = args.database_path


def proc(docs):
    # docsを処理する関数
    # ここに処理のロジックを実装します
    print(f"Processing {len(docs)} documents...")
    categories = texts2classes(docs, t2v, kmeans,length=check_length)

    for text, category in zip(docs, categories):
        save_dir = f"{base_dir}/{category}"
        make_dir(save_dir)
        database_name=database_path.split("/")[-1]#.split(".")[0]

        data = json.dumps(
            {"db": database_name, "text": text}, ensure_ascii=False)
        with open(f"{save_dir}/{database_name}.jsonl", "a") as f:
            f.write(data+"\n")

    return len(docs)


def main():

    docs = []
    futures = []

    lines=[]
    for article in read_gzip_json_file(database_path):
        text = article.get('text', '')  # 'text'キーからテキストデータを取得
        lines.append(text)



    for text in lines:
        text = clean_text(text)
        if len(text) < length_threshold:
            continue

        docs.append(text)
        if len(docs) == batch_size:
            # docsのコピーを作成してprocに渡す
            proc(docs[:])
            # docsをリセット
            docs = []

if __name__ == "__main__":
    main()

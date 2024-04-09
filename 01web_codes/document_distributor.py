# %%
import argparse
import json
import os
from src.classify.Text2Vec import Text2Vec, texts2classes
from src.cleaner.auto_cleaner import clean_text, ml_clean_text
from gensim.models.fasttext import load_facebook_model
import joblib
from src.load_gz import read_gzip_json_file
from src.distribute_jsonl import process_lines, make_dir
import pandas as pd

streaming = True
base_dir = "../data/categorized"
length_threshold = 30  # 短い記事は捨てる
check_length = 200  # はじめのlengthだけで分類する

# 機械学習で記事を選別する
do_ml_clean = True

# load models
t2v = Text2Vec(load_facebook_model('../data/model/cc.ja.300.bin'))
kmeans = joblib.load("../data/model/kmeans.pkl")


make_dir(base_dir)


def proc(docs, base_dir, database_path,
         check_length=check_length):
    return process_lines(docs, t2v, kmeans, base_dir, database_path, check_length=check_length)

# %%


# %%
batch_size = 100

parser = argparse.ArgumentParser(
    description="Load a dataset based on the given database name.")
parser.add_argument('database_path', type=str,
                    help='The path of the database to load')
args = parser.parse_args()
database_path = args.database_path


def main():

    docs = []

    # gzの場合
    if database_path.endswith('.gz'):
        lines = []
        for article in read_gzip_json_file(database_path):
            text = article.get('text', '')  # 'text'キーからテキストデータを取得
            lines.append(text)
    # parquetの場合
    elif database_path.endswith('.parquet'):
        df = pd.read_parquet(database_path)
        lines = df['text'].tolist()
    else:
        raise ValueError("Invalid database path", database_path)

    for text in lines:
        if do_ml_clean:
            text = ml_clean_text(text)
        else:
            text = clean_text(text)
        if len(text) < length_threshold:
            continue

        docs.append(text)
        if len(docs) == batch_size:
            proc(docs, base_dir, database_path,
                 check_length=check_length)

            # docsをリセット
            docs = []


if __name__ == "__main__":
    main()

import argparse
from src.classify.Text2Vec import Text2Vec
import joblib
from src.load_gz import load_gzip_or_parquet
from src.distribute_jsonl import process_lines, make_dir
from gensim.models import KeyedVectors
from src.cleaner.text_normalizer import normalize

streaming = True
base_dir = "../data/categorized"
length_threshold = 30  # 短い記事は捨てる
check_length = 200  # はじめのlengthだけで分類する


make_dir(base_dir)


def proc(docs, base_dir, database_path,
         check_length=check_length):
    return process_lines(docs, t2v, kmeans, base_dir,
                         database_path, check_length=check_length)


batch_size = 300

# argparseのセットアップ
parser = argparse.ArgumentParser(
    description="Load datasets based on the given database paths.")
# nargs='+'を使用して複数のデータベースパスをリストとして受け取る
parser.add_argument('database_path', type=str, nargs='+',
                    help='The paths of the databases to load')
args = parser.parse_args()
database_paths = args.database_path
print("\n\n-----\nDatabase paths: ", database_paths)

# load models
print("loading models...")
# t2v = Text2Vec(load_facebook_model('../data/model/cc.ja.300.bin'))
t2v = Text2Vec(model=KeyedVectors.load_word2vec_format(
    '../data/model/entity_vector/entity_vector.model.bin', binary=True),
    dim=200,
)


kmeans = joblib.load("../data/model/kmeans.pkl")
print("model loaded.")


def main():
    for database_path in database_paths:
        docs = []

        # gzの場合
        lines = load_gzip_or_parquet(database_path)
        old_text = ""
        for text in lines:
            # 純粋に同じテキストが続く場合はスキップ
            if text == old_text:
                continue
            old_text = text

            # text = clean_text(text)
            text = normalize(text)  # 正規化のみかけておく
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

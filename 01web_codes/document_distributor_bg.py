from typing import Dict

from src.classify.Text2Vec import Text2Vec
from src.cleaner.auto_cleaner import clean_text, ml_clean_text
import joblib
from gensim.models import KeyedVectors

streaming = True
length_threshold = 30  # 短い記事は捨てる
check_length = 100  # はじめのlengthだけで分類する

# 機械学習で記事を選別する
do_ml_clean = True


batch_size = 100

# load models
print("loading models...")
t2v = Text2Vec(model=KeyedVectors.load_word2vec_format(
    '../model/entity_vector/entity_vector.model.bin', binary=True),
    dim=200,
)




def cleaning_text(retrived_warc:Dict[str, str]):
    # 純粋に同じテキストが続く場合はスキップ
    print(retrived_warc)
    # trafilatura_content = retrived_warc['trafilatura_content']
    # if do_ml_clean:
    #     try:
    #         cleaned_text = ml_clean_text(trafilatura_content)
    #         return cleaned_text
    #     except Exception as e:
    #         print(e, trafilatura_content)
    # else:
    #     cleaned_text = clean_text(trafilatura_content)
    #     return cleaned_text
    #
    #
    return retrived_warc
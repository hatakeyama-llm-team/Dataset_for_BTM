import numpy as np
import MeCab
from functools import lru_cache
mecab = MeCab.Tagger("")


def extract_nouns(text):

    # 文章を形態素解析し、名詞を抽出
    nodes = mecab.parseToNode(text)
    nouns = []
    while nodes:
        features = nodes.feature.split(",")
        if features[0] == "名詞":
            nouns.append(nodes.surface)
        nodes = nodes.next

    return nouns


class Text2Vec:
    def __init__(self, model):
        self.model = model
        self.dim = 300

    @lru_cache(maxsize=10**4)  # 単語ベクトルの計算結果をキャッシュ
    def _word2vec_cached(self, word):
        try:
            return self.model.wv[word]
        except KeyError:
            return np.zeros(self.dim)

    def word2vec(self, word):
        return self._word2vec_cached(word)

    def text2vec(self, text):
        nouns = extract_nouns(text)
        vecs = [self.word2vec(n) for n in nouns]
        if len(vecs) == 0:
            return np.zeros(self.dim)
        else:
            return np.mean(vecs, axis=0)


def texts2classes(target_texts, t2v, kmeans, length=100):
    target_texts = [i[:length] for i in target_texts]
    vec = np.array([t2v.text2vec(i) for i in target_texts], dtype="float32")
    classes = kmeans.predict(vec)
    return classes

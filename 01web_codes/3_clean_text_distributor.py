# %%
#きれいなテキストを分配する

# %%
from src.cleaner.auto_cleaner import clean_text
from src.classify.Text2Vec import Text2Vec, texts2classes
from src.cleaner.auto_cleaner import clean_text, ml_clean_text
from gensim.models.fasttext import load_facebook_model
import joblib
from src.distribute_jsonl import process_lines,make_dir

# %%
streaming = True
base_dir = "../data/categorized"
length_threshold = 30  # 短い記事は捨てる
check_length = 200  # はじめのlengthだけで分類する


# load models
t2v = Text2Vec(load_facebook_model('../data/model/cc.ja.300.bin'))
kmeans = joblib.load("../data/model/kmeans.pkl")


# %%


def proc(docs,database_path):
    process_lines(docs, t2v, kmeans, 
                  base_dir, 
                  database_path,
                  check_length=check_length)




# %%
import sys
sys.path.append("../20integrate_texts/")
from loaders.loaders import *
length_threshold = 100
batch_size=100

loader_dict={
    "NHK_School":NHKSchool_loader(),
    "WikiQA":wiki_qa_loader(),
    "Wiki":cleaned_wiki_loader(),
    "NHK_News":nhk_news_loader(),
    "aozora":aozora_bunko_loader(),
    "j_ronbun":j_research_loader(),
    #"cosmo":cosmo_loader(),
}

# %%



for doc_name,loader in loader_dict.items():
    docs = []
    lines = []
    for record in iter(loader):
        lines.append(record["text"])

    cnt=0
    for text in lines:
        text = clean_text(text)
        if len(text) < length_threshold:
            continue

        docs.append(text)
        if len(docs) == batch_size:
            # docsのコピーを作成してprocに渡す
            proc(docs[:],doc_name+str(cnt))
            # docsをリセット
            docs = []
            #cnt+=1

    proc(docs[:],doc_name+str(cnt))



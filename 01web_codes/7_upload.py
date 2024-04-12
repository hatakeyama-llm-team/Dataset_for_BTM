# %%
import os
import glob
import json
import pandas as pd
from tqdm import tqdm
# os.environ["HF_ENDPOINT"] = "http://localhost:5564"
os.environ["HF_HUB_ENABLE_HF_TRANSFER"] = "1"
from huggingface_hub import HfApi, logging
logging.set_verbosity_debug()
hf = HfApi()

# %%
n_clusters=10000

done_list_path="../data/temp/done_list.txt"

done_list=[]
if os.path.exists(done_list_path):
    with open(done_list_path, "r") as f:
        done_list=f.read().split("\n")

def upload(cluster_id):
    if str(cluster_id) in done_list:
        return
    files=glob.glob(f"../data/dedup_categorized/{cluster_id}/*.jsonl")
    if len(files)==0:
        return
    text_list=[]
    for file in files:
        with open(file, "r") as f:
            for line in f:
                text_list.append(json.loads(line)["text"])
    df=pd.DataFrame(text_list, columns=["text"])
    df.to_parquet(f"../data/temp/temp.parquet")

    
    hf.upload_file(path_or_fileobj="../data/temp/temp.parquet",
    path_in_repo=f"parquet_files/{cluster_id}.parquet",
    repo_id="kanhatakeyama/TanukiCorpus", repo_type="dataset")

    done_list.append(str(cluster_id))
    with open(done_list_path, "w") as f:
        f.write("\n".join(done_list))

for cluster_id in tqdm(range(n_clusters)):
    try:
        upload(cluster_id)
    except Exception as e:
        print(e)





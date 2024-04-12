import glob
from tqdm import tqdm
import time
import os
path_list = glob.glob("../data/categorized/*/*.jsonl")
# フォルダを巡回して、重複を削除する

for path in tqdm(path_list):

    # タイムスタンプを確認し、3分以上前のファイルのみ処理する
    if os.path.getmtime(path) < time.time()-60*3:
        continue

    with open(path, "r") as f:
        lines = f.readlines()

    old_len = len(lines)
    lines = list(set(lines))
    if old_len != len(lines):
        with open(path, "w") as f:
            f.writelines(lines)
        print("Deduped: ", path)

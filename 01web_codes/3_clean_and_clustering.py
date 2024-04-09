# %%
import glob
import sys
import os
from concurrent.futures import ThreadPoolExecutor
import argparse
import random

parser = argparse.ArgumentParser(
    description="Process files")
parser.add_argument('max_workers', type=str,
                    help='Number of parallel workers')
args = parser.parse_args()

# 並列プロセスの数
max_workers = int(args.max_workers)
print("Max workers: ", max_workers)

# %%
with open("temp/gz_list.txt", "r") as f:
    gz_list = f.read().splitlines()

# gz_list = [i for i in gz_list if i.endswith('.gz')]
print(len(gz_list), " files found")

random.shuffle(gz_list)

# %%

dirs = ["temp/fin", "../data/categorized"]
for d in dirs:
    if not os.path.exists(d):
        os.makedirs(d)


# %%
def process_file(gz_path):
    gz_name = gz_path.split("/")[-1]  # .split(".")[0]

    if os.path.exists("temp/fin/" + gz_name):
        print("File already processed")
    else:
        print("Processing ", gz_name)
        os.system(f"python document_distributor.py {gz_path}")
        print("File processed")
        with open("temp/fin/" + gz_name, "w") as f:
            f.write("")


# ThreadPoolExecutorを使って並列化
with ThreadPoolExecutor(max_workers=max_workers) as executor:
    executor.map(process_file, gz_list)


# %%

# 特定のクラスタの
# 行数を数える
import json
from tqdm import tqdm
from loaders.CommonCrawlDataset import CommonCrawlDataset

with open("../data/clustered_path.json") as f:
    label_to_path_list = json.load(f)


label_to_article_count = {}
count = 0
label = "4"
loader = CommonCrawlDataset(label_to_path_list[label])
loader = (iter(loader))
while (True):
    try:
        next(loader)
        count += 1

        if count % 100000 == 0:
            print(count)
    except:
        records = loader.count
        label_to_article_count[label] = records
        print("error")
        break
records = loader.count
label_to_article_count[label] = records

with open("../data/sizes.txt", "a") as f:
    f.write(f"{label}: {records}\n")

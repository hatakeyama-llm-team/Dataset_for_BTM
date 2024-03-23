from src.loaders import *
from dataset_dict import dataset_dict, output_path
import random
from src.RecordDistributor import RecordDistributor
import json
import os
from tqdm import tqdm
import yaml
import os


def make_dir(path):
    if not os.path.exists(path):
        os.mkdir(path)


# %%
distributor = RecordDistributor(dataset_dict)
distributor.load_datasets()

# %%
distributor.dataset_dict, distributor.n_records_per_stage, distributor.n_records_per_stage

# %%
distributor.write_jsonl(output_path, overwrite=True)

# %%

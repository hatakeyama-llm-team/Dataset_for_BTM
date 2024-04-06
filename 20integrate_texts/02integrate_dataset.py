from src.loaders import *
from dataset_dict import dataset_dict, output_path
import random
from loaders.RecordDistributor import RecordDistributor
import json
import os
from tqdm import tqdm
import yaml
import os


distributor = RecordDistributor(dataset_dict)
distributor.load_datasets()
distributor.write_jsonl(output_path, overwrite=True)

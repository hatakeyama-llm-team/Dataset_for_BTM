from loaders.loaders import *
from dataset_dict import dataset_dict, output_path
from loaders.RecordDistributor import RecordDistributor


distributor = RecordDistributor(dataset_dict)
distributor.load_datasets()
distributor.write_jsonl(output_path, overwrite=True)

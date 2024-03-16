from datasets import load_dataset

# download HF datasets for cache
cache_dir = "../data/hf_cache"


def load_c4():
    return load_dataset('allenai/c4', 'ja', split='train', cache_dir=cache_dir)


def load_oscar():
    return load_dataset('oscar', 'unshuffled_deduplicated_ja',
                        split='train', cache_dir=cache_dir)


def load_cc100():
    return load_dataset('cc100', 'ja', split='train', cache_dir=cache_dir)


def load_shisa():
    return load_dataset("augmxnt/shisa-pretrain-en-ja-v1",
                        split='train', cache_dir=cache_dir)

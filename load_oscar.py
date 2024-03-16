from datasets import load_dataset

# download HF datasets for cache
cache_dir = "data/hf_cache"


def load_oscar():
    return load_dataset('oscar', 'unshuffled_deduplicated_ja',
                        split='train', cache_dir=cache_dir)


load_oscar()

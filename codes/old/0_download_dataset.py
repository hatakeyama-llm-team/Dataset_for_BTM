from codes.old.loaders import load_c4, load_oscar, load_cc100, load_shisa

load_c4()
load_oscar()
load_cc100()
load_shisa()

"""
# download HF datasets for cache
cache_dir = "../data/hf_cache"
dataset = load_dataset('allenai/c4', 'ja', split='train', cache_dir=cache_dir)

dataset = load_dataset('oscar', 'unshuffled_deduplicated_ja',
                       split='train', cache_dir=cache_dir)

dataset = load_dataset('cc100', 'ja', split='train', cache_dir=cache_dir)

dataset = load_dataset("augmxnt/shisa-pretrain-en-ja-v1",
                       split='train', cache_dir=cache_dir)
"""

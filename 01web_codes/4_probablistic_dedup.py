from src.RapidFuzzDedup import dedup_lines, dedup_dir
from tqdm import tqdm
import concurrent.futures
import random

def main():
    indices = list(range(10000))  # 処理するインデックスの範囲
    random.shuffle(indices)
    check_lengths = [100] * len(indices)
    check_ns = [10000] * len(indices)
    n_workers = [16] * len(indices)
    thresholds = [50] * len(indices)
    save_batch_sizes = [1000] * len(indices)
    repetitions = [1] * len(indices)

    #for i in indices:
    #    dedup_dir(i, check_lengths[i], check_ns[i], n_workers[i], thresholds[i], save_batch_sizes[i], repetitions[i])
    #return
    # ThreadPoolExecutorを使った並列処理
    with concurrent.futures.ThreadPoolExecutor(max_workers=40) as executor:
        # tqdmを使って進捗を表示
        list(tqdm(executor.map(dedup_dir, indices, check_lengths, check_ns,
             n_workers, thresholds, save_batch_sizes, repetitions), total=len(indices)))


if __name__ == "__main__":
    main()

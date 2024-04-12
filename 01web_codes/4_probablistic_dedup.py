from src.RapidFuzzDedup import dedup_lines, dedup_dir
from tqdm import tqdm
import concurrent.futures


def main():
    indices = range(10000)  # 処理するインデックスの範囲
    check_lengths = [100] * len(indices)
    check_ns = [500] * len(indices)
    n_workers = [8] * len(indices)
    thresholds = [35] * len(indices)
    save_batch_sizes = [1000] * len(indices)
    repetitions = [2] * len(indices)

    # ThreadPoolExecutorを使った並列処理
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
        # tqdmを使って進捗を表示
        list(tqdm(executor.map(dedup_dir, indices, check_lengths, check_ns,
             n_workers, thresholds, save_batch_sizes, repetitions), total=len(indices)))


if __name__ == "__main__":
    main()

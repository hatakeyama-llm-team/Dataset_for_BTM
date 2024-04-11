import argparse
from multiprocessing import Pool
from src.Dedup import DedupManager

n_clusters = 10000


def process_batch(batch_id):
    manager = DedupManager(batch_id)
    manager.process_dir()


def main(parallelism):
    batch_ids = range(n_clusters)  # 処理したいバッチIDの範囲
    with Pool(parallelism) as pool:
        pool.map(process_batch, batch_ids)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('--parallelism', type=int, default=2,
                        help='Number of processes to use for parallel processing')

    args = parser.parse_args()

    main(args.parallelism)

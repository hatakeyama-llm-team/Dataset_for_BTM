import os
import json
import random
from concurrent.futures import ThreadPoolExecutor
from tqdm import tqdm


def process_cluster(cluster_id):
    path = f"../data/categorized/{cluster_id}/dump.jsonl"
    try:
        with open(path, "r") as f:
            lines = f.readlines()
        lines = list(set(lines))
        with open(path, "w") as f:
            for line in lines:
                f.write(line)
    except Exception as e:
        return f"Error processing {cluster_id}: {e}"
    return f"Cluster {cluster_id} processed successfully"


def main():
    n_clusters = 10000
    cluster_list = list(range(n_clusters))
    random.shuffle(cluster_list)

    # Setting up the ThreadPoolExecutor
    # You can adjust the number of workers based on your system's capabilities
    with ThreadPoolExecutor(max_workers=4) as executor:
        results = list(
            tqdm(executor.map(process_cluster, cluster_list), total=len(cluster_list)))

    # Handling errors or success messages
    for result in results:
        print(result)


if __name__ == "__main__":
    main()



from datetime import datetime, timedelta


def get_deduped_ids(similarity_scores, threshold=90):
    deduped_ids = []
    ignore_indices = set()  # 類似度が高く無視すべき行のインデックス
    # 類似度閾値

    # 各行についてチェック
    for i in range(len(similarity_scores)):
        if i not in ignore_indices:  # この行がまだ処理されていない場合
            deduped_ids.append(i)
            # 類似度が閾値以上のすべての行を無視リストに追加
            for j in range(len(similarity_scores)):
                if similarity_scores[i][j] >= threshold and i != j:
                    ignore_indices.add(j)
    return deduped_ids


def dedup_lines(check_lines, check_length=100, n_workers=16, threshold=90):
    check_lines = [i[:check_lengh] for i in check_lines]
    similarity_scores = cdist(
        check_lines[:check_n], check_lines[:check_n], workers=16)
    deduped_ids = get_deduped_ids(similarity_scores, threshold=threshold)
    deduped_lines = [all_lines[i] for i in deduped_ids]
    return deduped_lines

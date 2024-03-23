import gzip
import json

def read_gzip_json_file(file_path):
    """GZIP圧縮されたJSONファイルから順にテキストデータを読み込むイテレータを生成します。"""
    with gzip.open(file_path, 'rt', encoding='utf-8') as f:
        for line in f:
            yield json.loads(line)


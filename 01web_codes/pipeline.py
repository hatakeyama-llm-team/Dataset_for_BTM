import base64
import json
import pickle
from typing import Dict

import joblib
import numpy as np
from apache_beam import typehints
from gensim.models import KeyedVectors
from sklearn.cluster import MiniBatchKMeans

from src.classify.Text2Vec import Text2Vec

from document_distributor_bg import cleaning_text
import subprocess
import apache_beam as beam
import trafilatura
from uuid import uuid4
from apache_beam.options.pipeline_options import PipelineOptions
from pydantic import BaseModel
import logging
from datetime import datetime
# 定数の設定
#FixMe: プロジェクトに応じて

class Configuration(object):
    PROJECT = 'annotation-app-418113'
    REGION = 'asia-northeast1'
    TABLE = 'warcs_download'
    BUCKET = 'big_query_db'
    N_CLUSTERS = 10

    # PROJECT='hatakeyamallm'
    # REGION='us-east1'
    # TABLE='warcs'
    # BUCKET='cloudrun_save_data'
    #

config = Configuration()
datetime_now = datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
# 一時ファイルの保存先
TEMP_LOCATION = f'gs://{config.BUCKET}/temp/{datetime_now}'
OPTIONS = {
    'project': config.PROJECT,
    'region': config.REGION,
    'temp_location': TEMP_LOCATION
}
logging.basicConfig(level=logging.INFO)

class Warcs(BaseModel):
    record_id: int
    url: str
    title: str
    warc_path: str
    pre_cleaned_text: str
    html_text: str
    batch_number: int
    trafilatura_content: str

def read_from_bigquery():
    """
    BigQueryからデータを読み込むための関数。
    """
    query = f'SELECT * FROM `{config.PROJECT}.cc_dataset.{config.TABLE}` LIMIT 2000'
    return beam.io.ReadFromBigQuery(query=query, use_standard_sql=True)

def prepare_warcs(warcs: dict):
    """
    Warcsデータを整形し、trafilaturaを使ってコンテンツを抽出する関数。

    Args:
        warcs (dict): Warcsデータの辞書。

    Returns:
        dict: 整形後のデータ。
    """
    warcs_dump = Warcs(**warcs)
    trafilatura_content = warcs_dump.trafilatura_content
    content = warcs_dump.html_text

    if trafilatura_content is None:
        trafilatura_content = trafilatura.extract(content.decode("utf-8", errors="ignore"), include_formatting=True)

    retrived_warc = {'trafilatura_content': trafilatura_content, 'original_content': content,
                     }
    return retrived_warc

class WriteToTempFile(beam.DoFn):
    def process(self, element):
        """
        データを一時ファイルに書き込むクラス。

        Args:
            element (dict): パイプラインからの入力データ。

        Yields:
            str: 一時ファイルのパス。
        """
        try:
            # generate uuid
            uuid_str = str(uuid4())

            temp_file_path = f'{TEMP_LOCATION}/{uuid_str}.txt'
            with beam.io.filesystems.FileSystems.create(temp_file_path, mime_type='text/plain') as file:
                file.write(element['trafilatura_content'].encode('utf-8'))
            logging.info(f'Written to temp file: {temp_file_path}')
            yield temp_file_path
        except Exception as e:
            logging.error(f"Error writing to temp file: {e}")

def deduplication(input_file_path):
    """
    指定されたファイルパスを使って重複除去を行う関数。

    Args:
        input_file_path (str): ファイルパス。

    Returns:
        str: 重複除去後のファイルパス。
    """
    try:
        # deduplicateコマンドを直接実行
        output_file_path = f'{input_file_path}.output.txt'
        cmd = f'../dedup/deduplicate {input_file_path} {output_file_path}'
        subprocess.run(cmd, shell=True, check=True)
        return output_file_path
    except subprocess.CalledProcessError as e:
        logging.error(f"Error in deduplication: {e}")
        return None
def remove_num_lines(record:Dict[str,str],key:str="text"):
    lines = record["trafilatura_content"].split("\n")
    new_lines = []
    for line in lines:
        if len(line) == 0:
            continue
        check_line = line[:20]
        count = sum(c.isdigit() for c in check_line)
        # num_ratio=count/len(check_line)
        num_ratio = count
        # print(num_ratio)
        ratio = 5
        if num_ratio > ratio and check_line.find(":") > 0:
            continue
        if num_ratio > ratio and check_line.find("日") > 0:
            continue
        if num_ratio > ratio and check_line.find("年") > 0:
            continue
        if num_ratio > ratio and check_line.find("-") > 0:
            continue
        if num_ratio > ratio and check_line.find("/") > 0:
            continue
        if num_ratio > ratio and check_line.find("／") > 0:
            continue
        if num_ratio > ratio and check_line.find("月") > 0:
            continue

        new_lines.append(line)
    record["text"] = "\n".join(new_lines)
    # 不要なキーを削除
    del record["trafilatura_content"]  # remove
    del record["original_content"]  # remove

    return json.dumps(record,ensure_ascii=False)

def prepare_cluster_list(record,cluster_id:int):
    data = json.loads(record)

    cleaned_text = cleaning_text(data["text"])

    # write json file to gcs
    with open(f'../data/categorized/{cluster_id}/{uuid4()}.jsonl', 'w') as f:
        f.write(json.dumps(data))
    return cleaned_text
# 定数の設定
# FixMe: プロジェクトに応じて 本来は10000
MODEL_PATH = "../data/model/entity_vector/entity_vector.model.bin"
MODEL_SAVE_PATH = "../data/model/kmeans.pkl"
class GetTextVectors(beam.DoFn):
    def __init__(self, model_path):
        self.model_path = model_path

    def setup(self):
        self.model = KeyedVectors.load_word2vec_format(self.model_path, binary=True)
        self.t2v = Text2Vec(model=self.model, dim=200)

    def process(self, text):
        vector = self.t2v.text2vec(text)
        yield np.array(vector)

class ClusterTexts(beam.DoFn):
    def __init__(self, n_clusters):
        self.n_clusters = n_clusters

    def setup(self):
        self.kmeans = MiniBatchKMeans(n_clusters=self.n_clusters, random_state=1)

    #命名はprocessでなければいけない
    def process(self, batch):
        vectors = np.stack(batch)
        self.kmeans.fit(vectors)
        for label in self.kmeans.labels_:
            yield label

def run():
    """
    パイプラインを実行する関数。
    """
    options = PipelineOptions(**OPTIONS, **{'streaming': True})
    # options = PipelineOptions(**OPTIONS, **{'streaming': True},**{'runner': 'DataflowRunner'})

    with beam.Pipeline(options=options) as p:

        # テキストの読み込みと前処理
        cleaned_texts = (
                p
                | 'Read' >> read_from_bigquery()
                | 'PrepareWarcs' >> beam.Map(prepare_warcs)
                | 'RemoveNumLinesText' >> beam.Map(remove_num_lines)  # json.dumps(record,ensure_ascii=False)
                | 'Print' >> beam.Map(print)
        )

        '''
        cleand_textの出力例
        
        {"text": "## すたじおみりす\n### 青空がっこのせんせい君。\n### いただきじゃんがりあんR\n"}

        '''

        # テキストの読み込みと前処理
        text_vectors = (
                cleaned_texts
                | "Get Text Vectors" >> beam.ParDo(GetTextVectors(MODEL_PATH))
                | "Batch Elements" >> beam.BatchElements(min_batch_size=500, max_batch_size=1000)
        )

        # クラスタリングの実行
        clustered_texts = (
            text_vectors
            | 'Cluster Texts' >> beam.ParDo(ClusterTexts(n_clusters=config.N_CLUSTERS))
        )

        # クラスタラベルのカウント
        cluster_counts = (
            clustered_texts
            | 'Map Labels to KV' >> beam.Map(lambda label: (int(label), 1)).with_output_types(typehints.KV[int, int])
            | 'Count by Cluster' >> beam.CombinePerKey(sum)
        )
        '''
          cluster_countsの出力例
          (3, 23)
          (1, 10)
          (4, 9)
          (7, 6)
          (2, 9)
          (0, 13)
          (8, 15)
          (9, 6)
          (5, 3)
          (6, 6)
          '''

        #GCSに保存した一時ファイルを読み込んでcppで記述したdedupで重複除去を行う
        deduplicated_files = (
                cleaned_texts
                | "Write to Temp File" >> beam.ParDo(WriteToTempFile())
                | "Deduplicate" >> beam.Map(deduplication)
        )


        # 重複削除したテキストをjsonlファイルに保存
        # clustered_texts = (
        #         deduplicated_files
        # )
        #



if __name__ == '__main__':
    run()
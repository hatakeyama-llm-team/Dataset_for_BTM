
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
PROJECT = 'annotation-app-418113'
REGION = 'asia-northeast1'
TABLE = 'warcs_download'
BUCKET = 'big_query_db'
datetime_now = datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
# 一時ファイルの保存先
TEMP_LOCATION = f'gs://{BUCKET}/temp/{datetime_now}'
OPTIONS = {
    'project': PROJECT,
    'region': REGION,
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
    query = f'SELECT * FROM `{PROJECT}.cc_dataset.{TABLE}` LIMIT 10'
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

    retrived_warc = {'trafilatura_content': trafilatura_content, 'original_content': content}
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

def deduplication(file_path):
    """
    指定されたファイルパスを使って重複除去を行う関数。

    Args:
        file_path (str): ファイルパス。

    Returns:
        str: 重複除去後のファイルパス。
    """
    try:
        # deduplicateコマンドを直接実行
        cmd = f'../dedup/deduplicate {file_path}'
        logging.info(f'Running deduplication command: {cmd}')
        subprocess.run(cmd, shell=True, check=True)
        logging.info(f'Deduplication complete for: {file_path}')
        return file_path
    except subprocess.CalledProcessError as e:
        logging.error(f"Error in deduplication: {e}")
        return None

def run():
    """
    パイプラインを実行する関数。
    """
    options = PipelineOptions(**OPTIONS, **{'streaming': True})

    with beam.Pipeline(options=options) as p:
        (
            p
            | 'Read' >> read_from_bigquery()
            | 'PrepareWarcs' >> beam.Map(prepare_warcs)
            | 'Write to temp file' >> beam.ParDo(WriteToTempFile())
            # | 'Deduplication' >> beam.Map(deduplication)
            | 'CleanedText' >> beam.Map(cleaning_text)
            | 'Write' >> beam.io.WriteToText('../test.txt')
        )

if __name__ == '__main__':
    run()

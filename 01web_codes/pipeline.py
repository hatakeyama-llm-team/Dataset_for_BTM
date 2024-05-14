import datetime
import os

import apache_beam.pipeline as pipeline
import trafilatura

from apache_beam.options.pipeline_options import PipelineOptions
import apache_beam as beam
from document_distributor_bg import cleaning_text
PROJECT = 'annotation-app-418113'
REGION = 'asia-northeast1'
table='warcs_download'
OPTIONS = {
    'project': PROJECT,
    'region': REGION
}


# REGION = 'us-central1'
# def read_from_gcs():
#     return beam.io.ReadFromText('gs://dataflow-samples/shakespeare/kinglear.txt')
#
def read_from_bigquery():
    query = f'SELECT * FROM `{PROJECT}.cc_dataset.{table}` limit 10'
    return beam.io.ReadFromBigQuery(query=query,use_standard_sql=True)

# pre_cleaned_text, html_text,
# trafilatura_content
from pydantic import BaseModel
class Warcs(BaseModel):
    record_id: int
    url: str
    title: str
    warc_path: str
    pre_cleaned_text: str
    html_text: str
    batch_number: int
    trafilatura_content: str



def prepare_warcs(warcs:Warcs):

    warcs_dump = Warcs(**warcs)
    trafilatura_content = warcs_dump.trafilatura_content
    content = warcs_dump.html_text
    # trafilatura_content がnullとなっているものがあるのでcontentから取得する
    if trafilatura_content is None:
        trafilatura_content = trafilatura.extract(content.decode("utf-8", errors="ignore"),
                                                                 include_formatting=True)

    '''
    trafilatura_contentを使ってclusteringの処理を記述
    '''


    retrived_warc =  {'trafilatura_content': trafilatura_content, 'original_content': content}
    print(retrived_warc)
    return retrived_warc
class WriteToTempFile(beam.DoFn):
    def process(self, element):
        temp_file_path = f'gs://big_query_db/temp/{datetime.datetime.now().strftime("%Y%m%d%H%M%S%f")}.txt'
        # ここでデータを一時ファイルに書き込む
        print(element)
        with beam.io.filesystems.FileSystems.create(temp_file_path, mime_type='text/plain') as file:
            file.write('test')
        yield temp_file_path



def deduplication(file_path):

    # ファイルをgcsにアップロード
    # DataFlowからファイルを読み込む
    # 重複を除外する


    cmd = f"../dedup_sentence/deduplicate {file_path}"

    os.system(cmd)
    return file_path
def run():

    options = PipelineOptions(**OPTIONS, **{'streaming': True},flags=['--temp_location=gs://big_query_db/temp'])

    # Add your pipeline code here
    with pipeline.Pipeline(options=options) as p:
        (p |'Read' >> read_from_bigquery() #BigQueryに保存した抽出済みデータを読み込む
         |'PrepareWarcs'>> beam.Map(lambda warc:prepare_warcs(warc)) #加工できる形に整形する
         | "Write to temp file" >> beam.ParDo(WriteToTempFile()) # 一時ファイルとしてDedupできるようにGoogle Cloud Storageに書き込む
         | 'Deduplication' >> beam.Map(lambda file_path: deduplication(file_path)) #FixMe:dedumplicate.cppでファイルパスを読み込む　
         | 'CleanedText' >> beam.Map(lambda retrived_warc: cleaning_text(retrived_warc)) #FixMe:クリーニング処理を行う
         | 'Write' >> beam.io.WriteToText('../test.txt') #結果をファイルに書き込む Todo:BigQueryに書き込む処理に修正する
        )
    p.run()

if __name__ == '__main__':
    run()
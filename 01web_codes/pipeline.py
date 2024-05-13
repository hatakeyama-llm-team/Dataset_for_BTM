
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


def deduplication(texts):
    return texts
def run():

    options = PipelineOptions(**OPTIONS, **{'streaming': True},flags=['--temp_location=gs://big_query_db/temp'])

    # Add your pipeline code here
    with pipeline.Pipeline(options=options) as p:
        (p |'Read' >> read_from_bigquery()
         |'PrepareWarcs'>> beam.Map(lambda warc:prepare_warcs(warc))
         | 'Deduplication' >> beam.Map(lambda x: deduplication(x)) #3_clean_and_cluster.pyはなし
         | 'CleanedText' >> beam.Map(lambda retrived_warc: cleaning_text(retrived_warc))
         | 'Write' >> beam.io.WriteToText('../test.txt')
        )
    p.run()

if __name__ == '__main__':
    run()


    # [
    #     {
    #       "name": "id",
    #       "type": "STRING",
    #     },
    #     {
    #       "name": "record_id",
    #       "type": "INTEGER"
    #     },
    #     {
    #       "name": "url",
    #       "type": "STRING",
    #       "description": "Unique URL"
    #     },
    #     {
    #       "name": "title",
    #       "type": "STRING"
    #     },
    #     {
    #       "name": "timestamp",
    #       "type": "STRING"
    #     },
    #     {
    #       "name": "path",
    #       "type": "STRING"
    #     },
    #     {
    #       "name": "pre_cleaned_text",
    #       "type": "STRING"
    #     },
    #     {
    #       "name": "html_text",
    #       "type": "STRING"
    #     },
    #     {
    #       "name": "batch_number",
    #       "type": "INTEGER"
    #     },
    #     {
    #         "name":"trafirature",
    #       "type": "STRING"
    #     }
    # ]
import argparse
import boto3

from google.api_core.client_options import ClientOptions
from google.cloud import documentai_v1 as documentai


"""
usage: python detect_languages.py -d gp_8.jpeg
"""

# Google Document AI configs
PROJECT_ID = 'ocr-poc-367209'
LOCATION = 'us'
PROCESSOR_ID = 'b48864073314b'


parser = argparse.ArgumentParser()
parser.add_argument('-d', '--document-path')
args = parser.parse_args()
FILE_PATH = f'medical_receipts/{args.document_path}'
MIME_TYPE_MAPPING = {
    'jpg': 'image/jpeg',
    'jpeg': 'image/jpeg',
    'png': 'image/png',
    'pdf': 'application/pdf',
}
MIME_TYPE = MIME_TYPE_MAPPING.get(FILE_PATH.split('.')[-1])


comprehend = boto3.client('comprehend')
docai_client = documentai.DocumentProcessorServiceClient(
    client_options=ClientOptions(api_endpoint=f'{LOCATION}-documentai.googleapis.com')
)

def detect_dominant_language(amazon_comprehend_client, text):
    response = amazon_comprehend_client.detect_dominant_language(Text=text)
    languages = response['Languages']
    dominant_language = max(languages, key=lambda lang: lang['Score'])
    return dominant_language['LanguageCode'], dominant_language['Score']


def extract_texts(google_docai_client, file_path):
    # The full resource name of the processor, e.g.:
    # projects/project-id/locations/location/processor/processor-id
    # Need to create new processors in the Cloud Console first
    RESOURCE_NAME = google_docai_client.processor_path(PROJECT_ID, LOCATION, PROCESSOR_ID)

    with open(file_path, 'rb') as image:
        image_content = image.read()

    raw_document = documentai.RawDocument(content=image_content, mime_type=MIME_TYPE)

    request = documentai.ProcessRequest(name=RESOURCE_NAME, raw_document=raw_document)

    result = google_docai_client.process_document(request=request)
    document_object = result.document
    text = document_object.text.replace('\n', '')

    return text


# text = '''博姓名:Name:號碼Number正式收據 Official Receipt博愛醫院流動中醫專科診所(24)---坑口地址:郵寄地址: 沙田大圍文禮路2號 沙田(大圍)診所地下電話:61024538B:Date: 2022-11-04RE31202211040006RC31202211040039RC31202211040040備註:Remarks:診斷:Diagnosis: 濕瘡項目Item藥費診金主診醫師:Name of RCMP:潘晶暉打印時間: 2022-11-04 12:14類別:Category:標準科別:Division: 普通科繳費方式Payment methodMASTERMASTER合計/Total:註冊編號:Registration收費員: 翁嘉俊No.005814金額Price165.00110.00$275.00院中李停警專夜EXPRE(8)主任醫師/授權收款人簽署及印章'''

text = extract_texts(docai_client, FILE_PATH)
lang, score = detect_dominant_language(comprehend, text)

print(lang, score)

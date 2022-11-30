import argparse
import requests


"""usage: python formx.py -d id_0.png"""

url = 'https://worker.formextractorai.com/extract'
ACCESS_TOKEN = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoiYzcwNzFkYmItM2E4My00ZWM0LTlmNDctNzEyNzdlYzQ4M2QzIn0.orWOWPUdozU1HtPwtw9fnuU6AvLdw8OQam6ByL6xEec'
FORM_ID = '15fe10b4-2d88-4be1-886d-48e3f213a43d'

parser = argparse.ArgumentParser()
parser.add_argument('-d', '--document-path')
args = parser.parse_args()
FILE_PATH = f'medical_receipts/hkid/{args.document_path}'
MIME_TYPE_MAPPING = {
    'jpg': 'image/jpeg',
    'jpeg': 'image/jpeg',
    'png': 'image/png',
    'pdf': 'application/pdf',
}
MIME_TYPE = MIME_TYPE_MAPPING.get(FILE_PATH.split('.')[-1])

payload = open(FILE_PATH, 'rb')
headers = {
    'X-WORKER-TOKEN': ACCESS_TOKEN,
    'X-WORKER-FORM-ID': FORM_ID,
    'Content-Type': MIME_TYPE,
}

response = requests.request('POST', url, headers=headers, data=payload)
parsed = response.json()

for field in parsed['fields']:
    print(field['name'], field['value'])

import argparse
import boto3
from textractcaller import call_textract
from textractprettyprinter.t_pretty_print import get_string, Textract_Pretty_Print


parser = argparse.ArgumentParser()
parser.add_argument('-d', '--document-path')
args = parser.parse_args()
FILE_PATH = f'medical_receipts/comprehend/{args.document_path}'


with open(FILE_PATH, 'rb') as f:
    image_bytes = bytearray(f.read())

response = call_textract(input_document=image_bytes)
lines = get_string(textract_json=response, output_type=[Textract_Pretty_Print.LINES])
text = lines.replace('\n', ' ')

# Amazon Comprehend Custom Entity Recognizer
comprehend = boto3.client('comprehend')
response = comprehend.detect_entities(
    Text=text,
    EndpointArn='arn:aws:comprehend:ap-southeast-1:603504217906:entity-recognizer-endpoint/extract-patient',
)

for entity in response['Entities']:
    print(entity['Type'], entity['Text'], entity['Score'])
    
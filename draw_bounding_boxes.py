import argparse
from PIL import Image, ImageDraw
from textractcaller import call_textract
from textractcaller.t_call import Textract_Types
from textractoverlayer.t_overlay import DocumentDimensions, get_bounding_boxes


"""
usage: python detect_languages.py -d gp_8.jpeg
"""

parser = argparse.ArgumentParser()
parser.add_argument('-d', '--document-path')
args = parser.parse_args()
FILE_PATH = f'medical_receipts/{args.document_path}'


image = Image.open(FILE_PATH).convert('RGB')
draw = ImageDraw.Draw(image)
document_dimension = DocumentDimensions(doc_width=image.size[0], doc_height=image.size[1])
overlay = [Textract_Types.LINE]

with open(FILE_PATH, 'rb') as f:
    image_bytes = bytearray(f.read())

response = call_textract(input_document=image_bytes)

print('Getting bounding boxes')
bounding_box_list = get_bounding_boxes(
    textract_json=response,
    document_dimensions=[document_dimension],
    overlay_features=overlay,
)

print('Drawing bounding boxes')
for bbox in bounding_box_list:
    # detection box
    draw.rectangle(
        xy=[bbox.xmin, bbox.ymin, bbox.xmax, bbox.ymax],
        outline='red',
        width=5,
    )
    # detected text + confidence
    draw.text(
        xy=[bbox.xmin, bbox.ymin - 10],
        fill='green',
        text=f'{bbox.text} {bbox.confidence}',
    )

print('Showing image')
image.show()

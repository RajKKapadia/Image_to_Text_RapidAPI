from typing import Dict, List
import re

import matplotlib.pyplot as plt
from doctr.io import DocumentFile
from doctr.models import ocr_predictor
import cv2 as cv
from doctr.utils.visualization import visualize_page

from config import Config

DOWNLOAD_FOLDER = Config.DOWNLOAD_FOLDER
BASE_DIRECTORY = Config.BASE_DIRECTORY

predictor = ocr_predictor(pretrained=True)

def get_text_from_image(image_path: str) -> List:
    '''This function returns list of text identified from each line\n
       ----------\n
       Parameters:\n
       image_path (str) - path to the image\n
       ----------\n
       Returns:\n
       list of detected text 
    '''
    single_img_doc = DocumentFile.from_images(image_path)
    result = predictor(single_img_doc)

    result = result.export()

    blocks = result['pages'][0]['blocks']
    lines = []
    for block in blocks:
        lines.append(block['lines'])

    words = []

    for line in lines:
        for l in line:
            words.append(l['words'])

    word_lines = []
    
    for word in words:
        w = ''
        for value in word:
            w += value['value']
            w += ' '
            w = re.sub('[^A-Za-z0-9 ]+', '', w)
            
        word_lines.append(w.strip())

    word_lines = list(filter(None, word_lines))

    return word_lines

def get_annotated_image(image_path: str, download_image_path: str) -> str:
    '''This function returns annotated image of the identified text\n
       ----------\n
       Parameters:\n
       image_path (str) - path to the image\n
       download_image_path (str) - path to save the image
       ----------\n
       Returns:\n
       path to the annotated image
    '''
    single_img_doc = DocumentFile.from_images(image_path)
    result = predictor(single_img_doc)

    result = result.export()

    visualize_page(result['pages'][0], cv.imread(image_path))
    plt.savefig(download_image_path)
    return download_image_path
    

def get_raw_data_from_image(image_path: str) -> Dict:
    '''This function returns list of text identified from each line\n
       ----------\n
       Parameters:\n
       image_path (str) - path to the image\n
       ----------\n
       Returns:\n
       raw object of the text detected 
    '''
    single_img_doc = DocumentFile.from_images(image_path)
    result = predictor(single_img_doc)

    result = result.export()
    return result
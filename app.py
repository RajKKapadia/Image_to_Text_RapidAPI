import os
from typing import Dict
import logging
from datetime import datetime

from flask import Flask, jsonify, request, send_file, send_from_directory
from flask_cors import CORS
from werkzeug.utils import secure_filename
import cv2 as cv

import text_detection
import edge_detection
from config import Config

ALLOWED_EXTENSION = Config.ALLOWED_EXTENSIONS
BASE_DIRECTORY = Config.BASE_DIRECTORY
UPLOAD_FOLDER = Config.UPLOAD_FOLDER
DOWNLOAD_FOLDER = Config.DOWNLOAD_FOLDER
APP_LOG = Config.APP_LOG

date = datetime.now()

log_file_name = f'{date.strftime("%H_%M_%d_%m_%y")}_log'

logging.basicConfig(
    filename=f'{BASE_DIRECTORY}/{APP_LOG}/{log_file_name}.log',
    filemode='w',
    format='%(asctime)s %(levelname)s -> %(message)s', datefmt='%d-%b-%y %H:%M:%S',
    level=logging.INFO
)

app = Flask(__name__)

CORS(app)

def get_formated_response(
    status,
    data,
    message
) -> Dict:
    ''' Get formated response for the API\n
        Takes -> status, message, and base64\n
        Returns -> jsonified response
    '''
    return jsonify(
        {
            'status': status,
            'data': data,
            'message': message
        }
    )


def allowed_file(filename):
    flag = '.' in filename and filename.rsplit(
        '.', 1)[1].lower() in ALLOWED_EXTENSION
    return flag


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/favicon.png')


@app.route('/', methods=['GET'])
def home():
    return 'Hello World'


@app.route('/api/image_to_text', methods=['GET', 'POST'])
def api_text_to_image():
    logging.info('/api/image_to_text route called.')
    if 'image' not in request.files:
        return get_formated_response(
            400,
            None,
            'Make sure file name is image in the request data.'
        )
    file = request.files['image']
    if file.filename == '':
        return get_formated_response(
            400,
            None,
            'Make sure file name is image in the request data.'
        )
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        ori_image_path = f'{BASE_DIRECTORY}/{UPLOAD_FOLDER}/{filename}'
        file.save(ori_image_path)
        try:
            cropped_img = edge_detection.get_cropped_image(ori_image_path)
            crop_image_path = f'{BASE_DIRECTORY}/{UPLOAD_FOLDER}/crop_{filename}'
            cv.imwrite(crop_image_path, cropped_img)
            data = text_detection.get_text_from_image(crop_image_path)
            os.unlink(ori_image_path)
            os.unlink(crop_image_path)
            return get_formated_response(
                200,
                data,
                'Image to text success.'
            )
        except:
            try:
                os.unlink(ori_image_path)
                os.unlink(crop_image_path)
            except:
                pass
            return get_formated_response(
                400,
                None,
                'Some error occured at text extraction.'
            )
    else:
        return get_formated_response(
            400,
            None,
            'Allowed file types are png, jpg, jpeg.'
        )


@app.route('/api/annotate_image', methods=['GET', 'POST'])
def annotate_image():
    logging.info('/api/annotate_image route called.')
    if 'image' not in request.files:
        return get_formated_response(
            400,
            None,
            'Make sure file name is image in the request data.'
        )
    file = request.files['image']
    if file.filename == '':
        return get_formated_response(
            400,
            None,
            'Make sure file name is image in the request data.'
        )
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        ori_image_path = f'{BASE_DIRECTORY}/{UPLOAD_FOLDER}/{filename}'
        file.save(ori_image_path)
        try:
            cropped_img = edge_detection.get_cropped_image(ori_image_path)
            crop_image_path = f'{BASE_DIRECTORY}/{UPLOAD_FOLDER}/crop_{filename}'
            cv.imwrite(crop_image_path, cropped_img)
            annotated_image_path = f'{BASE_DIRECTORY}/{DOWNLOAD_FOLDER}/annotate_{filename}'
            download_image_path = text_detection.get_annotated_image(
                crop_image_path, annotated_image_path)
            os.unlink(ori_image_path)
            os.unlink(crop_image_path)
            return send_file(download_image_path)
        except:
            try:
                os.unlink(ori_image_path)
                os.unlink(crop_image_path)
            except:
                pass
            return get_formated_response(
                400,
                None,
                'Some error occured at text extraction.'
            )
    else:
        return get_formated_response(
            400,
            None,
            'Allowed file types are png, jpg, jpeg.'
        )


@app.route('/api/raw_image_data', methods=['GET', 'POST'])
def raw_image_data():
    logging.info('/api/raw_image_data route called.')
    if 'image' not in request.files:
        return get_formated_response(
            400,
            None,
            'Make sure file name is image in the request data.'
        )
    file = request.files['image']
    if file.filename == '':
        return get_formated_response(
            400,
            None,
            'Make sure file name is image in the request data.'
        )
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        ori_image_path = f'{BASE_DIRECTORY}/{UPLOAD_FOLDER}/{filename}'
        file.save(ori_image_path)
        try:
            cropped_img = edge_detection.get_cropped_image(ori_image_path)
            crop_image_path = f'{BASE_DIRECTORY}/{UPLOAD_FOLDER}/crop_{filename}'
            cv.imwrite(crop_image_path, cropped_img)
            raw_data = text_detection.get_raw_data_from_image(crop_image_path)
            os.unlink(ori_image_path)
            os.unlink(crop_image_path)
            return get_formated_response(
                200,
                raw_data,
                'Image to text success.'
            )
        except:
            try:
                os.unlink(ori_image_path)
                os.unlink(crop_image_path)
            except:
                pass
            return get_formated_response(
                400,
                None,
                'Some error occured at text extraction.'
            )
    else:
        return get_formated_response(
            400,
            None,
            'Allowed file types are png, jpg, jpeg.'
        )

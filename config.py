import os

class Config:
    ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])
    BASE_DIRECTORY = os.getcwd()
    UPLOAD_FOLDER = 'upload'
    DOWNLOAD_FOLDER = 'download'
    APP_LOG = 'applog'
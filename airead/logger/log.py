import logging
from logging.handlers import RotatingFileHandler

def init_logger(app):
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

    #stream_handler = logging.StreamHandler()
    #stream_handler.setLevel(logging.INFO)
    #stream_handler.setFormatter(formatter)
    #app.logger.addHandler(stream_handler)

    file_handler = RotatingFileHandler(app.config['LOG_FILE'], maxBytes=10000,
            backupCount=1)
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(formatter)
    app.logger.addHandler(file_handler)

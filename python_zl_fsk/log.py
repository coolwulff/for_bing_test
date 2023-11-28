import datetime
import logging

def generate_log(log_level=logging.ERROR):
    logger = logging.getLogger(__name__)
    logger.setLevel(level=log_level)
    time_today = datetime.datetime.now().strftime('%Y-%m-%d')
    log_name = "log-" + time_today + ".txt"
    log_path = "./log/" + log_name
    file_handler = logging.FileHandler(log_path,encoding='UTF-8')
    file_handler.setLevel(level=log_level)
    file_formatter = logging_format = logging.Formatter(
                '%(asctime)s - %(levelname)s - %(threadName)s -%(filename)s - %(funcName)s - %(lineno)s - %(message)s')
    file_handler.setFormatter(file_formatter)
    logger.addHandler(file_handler)

    return logger

import logging
import sys
def setup_logger():
    logger = logging.getLogger("MyIu")
    logger.setLevel(logging.INFO)
    if not logger.hasHandlers():
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        # Use a consistent log file name
        file_handler = logging.FileHandler("myiu_system.log", encoding='utf-8')
        file_handler.setFormatter(formatter)
        stream_handler = logging.StreamHandler(sys.stdout)
        stream_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
        logger.addHandler(stream_handler)
    return logger
log = setup_logger()
import logging


def log_set(Log_level=logging.INFO):
    logger = logging.getLogger()
    logger.setLevel(Log_level)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s: - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
    ch = logging.StreamHandler()
    ch.setLevel(Log_level)
    ch.setFormatter(formatter)
    logger.addHandler(ch)

import logging
import os
import requests


def log_set(Log_level=logging.INFO):
    logger = logging.getLogger()
    logger.setLevel(Log_level)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s: - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
    ch = logging.StreamHandler()
    ch.setLevel(Log_level)
    ch.setFormatter(formatter)
    logger.addHandler(ch)


def download_img(url, save_path="./"):
    if os.path.isdir(save_path):
        save_path = os.path.join(save_path, "img.png")
    with open(save_path, "wb") as f:
        f.write(requests.get(url).content)

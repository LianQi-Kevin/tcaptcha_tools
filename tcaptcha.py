import io
import logging
import os
import time
import shutil
import urllib.parse

import PIL
import requests

from PIL import Image
# from selenium import webdriver
from seleniumwire import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from typing import Tuple

from utils.utils import log_set
from utils.selenium_tools import set_driver, web_wait


def crop_tcaptcha(uncropped_img: bytes, corp_area: tuple) -> PIL.Image:
    """
    * 使用Image.open()读取二进制数据并剪切图像
    :param uncropped_img: 二进制图片
    :param corp_area: 截取缺口图片的区域, (x1, y1, x2, y2)
    :return: cropped img, PIL.Image
    """
    return Image.open(io.BytesIO(uncropped_img)).crop(corp_area)


def save_tcaptcha_img(img_index: str, img_url: str, save_path: str = "tcaptcha_img") -> Tuple[str, bytes]:
    """
    * 下载tcaptcha图片并保存
    :param img_index: 图片的编号
    :param img_url: img url path
    :param save_path: 保存tcaptcha图片的文件夹
    :returns: 存储的路径, 二进制img对象
    """
    img_name = {"0": "uncropped", "1": "background", "2": "notch"}
    logging.info(f"{img_name[img_index]} img url: {img_url}")
    img = requests.get(img_url).content
    img_path = os.path.join(save_path, f"{img_name[img_index]}.png")
    with open(img_path, "wb") as f:
        logging.info(f"Save {img_name[img_index]} image to {img_path}")
        f.write(img)
    return img_path, img


def get_tcaptcha_img(driver: webdriver, cache_path: str = "tcaptcha_img"):
    """
    * 获取iframe内的背景图和缺口图
    """
    background_path, notch_path, uncropped_path = None, None, None
    # get url and download
    for request in driver.requests:
        if request.response and request.response.headers['Content-Type'] != "application/json" and request.headers[
            'Sec-Fetch-Dest'] == "image" and "t.captcha.qq.com" in request.url:
            query: dict = dict(urllib.parse.parse_qsl(urllib.parse.urlsplit(request.url).query))
            if query["img_index"] == "1":
                background_path, background_img = save_tcaptcha_img(query["img_index"], request.url, cache_path)
            elif query["img_index"] == "2":
                notch_path, notch_img = save_tcaptcha_img(query["img_index"], request.url, cache_path)
            elif query["img_index"] == "0":
                uncropped_path, uncropped_img = save_tcaptcha_img(query["img_index"], request.url, cache_path)
                notch_img = crop_tcaptcha(uncropped_img, corp_area=(140, 490, 260, 610))
                notch_path = os.path.join(cache_path, "notch.png")
                logging.info(f"Save notch image to {notch_path}")
                notch_img.save(notch_path)
            else:
                logging.error("Tcaptcha image not found, ERROR!")
                raise Exception("Tcaptcha image not found, ERROR!")
    return background_path, notch_path, uncropped_path


def open_tcaptcha(captcha_mode: str = "体验用户") -> webdriver:
    """
    * 打开tcaptcha官网并打开iframe
    :param captcha_mode: ["体验用户", "可疑用户"]
    """
    # set driver
    driver = set_driver(headless_mode=False)

    # go site
    tcaptcha_url = "https://007.qq.com/"  # 腾讯防水墙官网
    logging.info(f"Start open: {tcaptcha_url}")
    driver.get(tcaptcha_url)
    logging.info(f"Successful open: {tcaptcha_url}")

    # show iframe
    web_wait(driver, By.XPATH, f"//a[text()='{captcha_mode}']", 20)
    driver.find_element(By.XPATH, f"//a[text()='{captcha_mode}']").click()
    web_wait(driver, By.XPATH, "//button[text()='体验验证码']", 20)
    driver.find_element(By.XPATH, "//button[text()='体验验证码']").click()
    return driver


def get_tcaptcha_iframe(driver: webdriver) -> webdriver:
    """
    * 从browser中寻找tcaptcha iframe并切换到iframe内
    """
    web_wait(driver, By.CSS_SELECTOR, "iframe[id*='tcaptcha']", 20)
    driver.switch_to.frame(driver.find_element(By.CSS_SELECTOR, "iframe[id*='tcaptcha']"))
    time.sleep(3)
    logging.info("Successful go into tcaptcha iframe")
    return driver


def tcaptcha(driver: webdriver, clean_up: bool = True) -> webdriver:
    """
    * 在driver内寻找tcaptcha iframe, 并基于图鉴进行打码
    :param driver: webdriver
    :param clean_up: 是否在执行结束后删除tcaptcha图片缓存文件夹
    """
    # basic var
    cache_path = "./tcaptcha_img"
    os.makedirs(cache_path, exist_ok=True)
    # switch to tcaptcha iframe
    driver = get_tcaptcha_iframe(driver)
    # save tcaptcha img
    background_path, notch_path, _ = get_tcaptcha_img(driver, cache_path)
    print(background_path, notch_path)
    # get ttshitu result

    # clean up
    if clean_up:
        shutil.rmtree(cache_path, ignore_errors=True)
    driver.switch_to.default_content()
    return driver


if __name__ == '__main__':
    # set logging
    log_set(Log_level=logging.INFO)

    # init and go site
    for mode in ["体验用户", "可疑用户"]:
        browser = open_tcaptcha(captcha_mode=mode)
        browser = tcaptcha(browser, False)
        browser.quit()

import logging
import os
import time
import base64
import json
import urllib.parse
import requests

# from selenium import webdriver
from seleniumwire import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By

from utils.utils import log_set
from utils.selenium_tools import set_driver, web_wait, check_element_exists


def get_tcaptcha_img(driver: webdriver, img_save_path: str = None):
    bg_img, notch_img, uncropped_img = None, None, None
    if img_save_path is not None:
        assert os.path.isdir(img_save_path), f"{img_save_path} not a dir"
        os.makedirs(img_save_path, exist_ok=True)
    for request in driver.requests:
        if request.response and request.response.headers['Content-Type'] != "application/json" and request.headers['Sec-Fetch-Dest'] == "image" and "t.captcha.qq.com" in request.url:
            query = dict(urllib.parse.parse_qsl(urllib.parse.urlsplit(request.url).query))
            # ---- basic msg ----
            print("Url:", request.url)
            print("Code:", request.response.status_code)
            print("Content-Type:", request.response.headers['Content-Type'])
            print("Sec-Fetch-Dest:", request.headers['Sec-Fetch-Dest'])
            print("Img_index:", query['img_index'])
            # ---- basic msg ----
            if query["img_index"] == "1":
                logging.info("Background img url: {}".format(request.url))
                bg_img = requests.get(request.url).content
                if img_save_path is not None:
                    save_path = os.path.join(img_save_path, "background.png")
                    with open(save_path, "wb") as f:
                        logging.info("Save background image to {}".format(save_path))
                        f.write(bg_img)
            elif query["img_index"] == "2":
                logging.info("Notch img url: {}".format(request.url))
                notch_img = requests.get(request.url).content
                if img_save_path is not None:
                    save_path = os.path.join(img_save_path, "notch.png")
                    with open(save_path, "wb") as f:
                        logging.info("Save notch image to {}".format(save_path))
                        f.write(notch_img)
            elif query["img_index"] == "0":
                logging.info("Uncropped notch img url: {}".format(request.url))
                uncropped_img = requests.get(request.url).content
                if img_save_path is not None:
                    save_path = os.path.join(img_save_path, "uncropped.png")
                    with open(save_path, "wb") as f:
                        logging.info("Save notch image to {}".format(save_path))
                        f.write(uncropped_img)
            else:
                logging.error("Tcaptcha image not found, ERROR!")
                exit()
    return bg_img, notch_img


# 打开tcaptcha官网并打开iframe
def open_tcaptcha(captcha_mode: str = "体验用户") -> webdriver.Chrome:
    """
    :param captcha_mode: ["体验用户", "可疑用户", "恶意用户"]
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


if __name__ == '__main__':
    # set logging
    log_set(Log_level=logging.INFO)

    # init and go site
    # browser = open_tcaptcha(captcha_mode="体验用户")
    browser = open_tcaptcha(captcha_mode="可疑用户")

    # switch to tcaptcha iframe
    web_wait(browser, By.CSS_SELECTOR, "iframe[id*='tcaptcha']", 20)
    browser.switch_to.frame(browser.find_element(By.CSS_SELECTOR, "iframe[id*='tcaptcha']"))
    # web_wait(browser, By.CSS_SELECTOR, "div[id='slideBgWrap']", 20)
    time.sleep(3)
    logging.info("Successful go into tcaptcha iframe")

    # ---- save sourcecode -----
    # time.sleep(30)
    # source_code = browser.page_source
    # source_code = browser.execute_script("return document.body.innerHTML;")
    # logging.info("Write source code to test.html")
    # with open("test.html", "w") as html_f:
    #     html_f.write(source_code)
    # ---- save sourcecode -----

    get_tcaptcha_img(browser, img_save_path="./tcaptcha_img")

    # do out of frame
    browser.switch_to.default_content()

    browser.close()  # time.sleep(999)

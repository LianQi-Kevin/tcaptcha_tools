import logging
import time

from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By

from utils.utils import log_set
from utils.selenium_tools import set_driver, web_wait, check_element_exists


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
    driver.maximize_window()
    logging.info(f"Successful open: {tcaptcha_url}")

    # show iframe
    web_wait(driver, By.XPATH, f"//*[text()='{captcha_mode}']", 20)
    driver.find_element(By.XPATH, f"//*[text()='{captcha_mode}']").click()
    web_wait(driver, By.XPATH, "//*[text()='体验验证码']", 20)
    driver.find_element(By.XPATH, "//*[text()='体验验证码']").click()
    return driver


if __name__ == '__main__':
    # set logging
    log_set(Log_level=logging.INFO)

    # init and go site
    browser = open_tcaptcha(captcha_mode="体验用户")

    # switch to tcaptcha iframe
    web_wait(browser, By.CSS_SELECTOR, "iframe[id*='tcaptcha']", 20)
    browser.switch_to.frame(browser.find_element(By.CSS_SELECTOR, "iframe[id*='tcaptcha']"))
    logging.info("Successful go into tcaptcha iframe")

    # ---- save sourcecode -----
    # source_code = browser.page_source
    # source_code = browser.execute_script("return document.body.innerHTML;")
    # with open("test.html", "w") as html_f:
    #     html_f.write(source_code)
    # ---- save sourcecode -----

    # todo: 打印源码后发现，iframe内实际并没有有效的<img>，疑似是iframe加载后用js脚本替换的，待解决
    # web_wait(browser, By.CSS_SELECTOR, "div[id='slideBgWrap']")
    # bg_img = browser.find_element(By.CSS_SELECTOR, "div[id='slideBgWrap']").screenshot("test.png")
    web_wait(browser, By.CSS_SELECTOR, "img[id='slideBg']")
    bg_img = browser.find_element(By.CSS_SELECTOR, "img[id='slideBg']").get_attribute("src")
    inside_img = browser.find_element(By.CSS_SELECTOR, "img[id='slideBlock']").get_attribute("src")

    # do out of frame
    browser.switch_to.default_content()

    time.sleep(999)

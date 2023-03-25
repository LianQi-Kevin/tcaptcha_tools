import random
import logging

# from selenium import webdriver
from seleniumwire import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager

AgentsList = [
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/29.0.1547.57 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.71 Safari/537.36",
    "Mozilla/5.0 (Linux; Android 4.0.4; Galaxy Nexus Build/IMM76B) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.133 Mobile Safari/535.19", ]


# 检查元素是否存在
def check_element_exists(driver: webdriver.Chrome, element: str, condition: By):
    # noinspection PyBroadException
    try:
        driver.find_element(condition, element)
        return True
    except Exception as _:
        return False


# download chrome driver and use it
def set_driver(headless_mode: bool = True) -> webdriver.Chrome:
    """
    :param headless_mode: Whether to use headless mode
    """
    # init options
    options = Options()
    # User Agent
    user_agent = random.choice(AgentsList)
    logging.debug("User agent: {}".format(user_agent))
    # options.add_argument("user-agent={}".format(user_agent))
    # headless
    if headless_mode:
        logging.info("Use headless mode")
        options.add_argument('headless')
    return webdriver.Chrome(options=options, service=ChromeService(ChromeDriverManager().install()))


# 简写WebDriverWait
def web_wait(driver: webdriver, by: By, element: str, until_sec: int = 20):
    WebDriverWait(driver, until_sec).until(EC.presence_of_element_located((by, element)))

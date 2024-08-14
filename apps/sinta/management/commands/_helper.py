"""Module for instantiate selenium driver"""

from selenium import webdriver


def get_browser():
    """instantiate a chrome drive"""
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('window-size=1920,1080')  # resolusi browser

    return webdriver.Chrome(options=chrome_options)

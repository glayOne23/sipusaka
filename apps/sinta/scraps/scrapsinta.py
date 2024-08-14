"""Module for parent scrapt"""

import logging

from django.db.models import Model
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait

logger = logging.getLogger(__name__)

class ScrapSinta():
    """Module for parent scrapt"""
    browser = None

    def __init__(
        self,
        browser: webdriver,
    ) -> None:
        self.browser = browser

    def get_data(self) -> list:
        """get data from scrapt"""
        return []

    def go_next(self):
        """go next"""
        url_next = self.browser.find_element(By.LINK_TEXT, "Next")
        parent_url_next = url_next.find_element(By.XPATH, "..").get_attribute("class")
        if 'disabled' in parent_url_next:
            logger.info("selesai scrap ketika sampai di %s", self.browser.current_url)
            return False
        self.browser.execute_script("arguments[0].click();", url_next)
        return True

    def save_to_db(self, model:Model, data_list: list):
        """save to db"""
        univ_to_create = [model(**data) for data in data_list]
        model.objects.bulk_create(univ_to_create)

    def scrap(self, model: Model = None):
        """Scrap all universities in general"""
        while True:
            try:
                logger.info(
                    "proses url: %s",
                    self.browser.current_url
                )
                WebDriverWait(driver=self.browser, timeout=5).until(
                    expected_conditions.presence_of_all_elements_located((By.TAG_NAME, "body"))
                )
                data_list = self.get_data()
            except TimeoutException:
                logger.warning(
                    "ada error timeout ketika sampai di %s",
                    self.browser.current_url
                )
                break
            except ConnectionRefusedError:
                logger.warning(
                    "ada error Connection refused timeout ketika sampai di %s",
                    self.browser.current_url
                )
                break
            if model:
                self.save_to_db(model, data_list)
            if not self.go_next():
                break


class ScrapSintaDetail():
    """Module for parent scrapt"""
    browser = None

    def __init__(
        self,
        browser: webdriver,
    ) -> None:
        self.browser = browser

    def get_data(self) -> list:
        """get data from scrapt"""
        return []

    def scrap(self):
        """Scrap detail university"""
        self.browser.switch_to.window(self.browser.window_handles[1])
        WebDriverWait(driver=self.browser, timeout=5).until(
            expected_conditions.presence_of_all_elements_located((By.TAG_NAME, "body"))
        )
        data_list = self.get_data()
        self.browser.close()
        self.browser.switch_to.window(self.browser.window_handles[0])
        return data_list

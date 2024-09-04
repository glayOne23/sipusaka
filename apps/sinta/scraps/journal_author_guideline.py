"""Scrap Author Guideline"""

import logging

from urllib.parse import unquote

from django.db.models import Model
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from apps.sinta.scraps.scrapsinta import Scrap

logger = logging.getLogger(__name__)

class ScrapAuthorGuideline(Scrap):
    """Scrap Author Guideline"""

    def scrap(self, model: Model = None):
        """Scrap all in general"""
        while True:
            try:
                logger.info(
                    f"proses url: %s - {self.browser.current_url}", self.data_values['journal'].id
                )
                self.run_webdriverwait()
                # get data
                author_guidelines = self.browser.find_elements(
                    By.XPATH, "//a[contains(translate(@href, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'authorguidelines')]"
                )
                if not author_guidelines:
                    author_guidelines = self.browser.find_elements(
                        By.XPATH, """
                        //a[contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'author guideline')]
                        """
                    )
                if not author_guidelines:
                    author_guidelines = self.browser.find_elements(
                        By.XPATH, """
                        //a[contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'authors guideline')]
                        """
                    )
                if not author_guidelines:
                    author_guidelines = self.browser.find_elements(
                        By.XPATH, """
                        //a[contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'guide for author')]
                        """
                    )
                if not author_guidelines:
                    author_guidelines = self.browser.find_elements(
                        By.XPATH, """
                        //a[contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'guidelines for author')]
                        """
                    )
                if not author_guidelines:
                    author_guidelines = self.browser.find_elements(
                        By.XPATH, """
                        //a[contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'panduan')]
                        """
                    )
                if not author_guidelines:
                    author_guidelines = self.browser.find_elements(
                        By.XPATH, """
                        //a[contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'guideline for author')]
                        """
                    )


                if author_guidelines:
                    author_guideline_url = author_guidelines[0].get_attribute('href').strip()
                    self.data_values['journal'].author_guideline_url = author_guideline_url
                    self.data_values['journal'].save()
                    logger.info(
                        f"Sukses scrap author guideline: %s", self.data_values['journal'].id
                    )
                break
            except TimeoutException:
                logger.warning(
                    f"ada error timeout ketika sampai di: %s - {self.browser.current_url}", self.data_values['journal'].id
                )
                break
            except ConnectionRefusedError:
                logger.warning(
                    f"ada error Connection refused timeout ketika sampai di: %s - {self.browser.current_url}", self.data_values['journal'].id
                )
                break
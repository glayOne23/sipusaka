"""Module fror scrapping list of universities"""

import logging
from urllib.parse import unquote

from apps.sinta.scraps.scrapsinta import ScrapSinta
from selenium.webdriver.common.by import By

logger = logging.getLogger(__name__)

class ScrapArticle(ScrapSinta):
    """Scrap all article in general"""

    def get_data(self, data_values:dict = None) -> list:

        exclamation = self.browser.find_elements(
            By.XPATH, """
            //h1[contains(@class,'ui icon header red')]//i[contains(@class,'exclamation icon orange')]
            """
        )
        if exclamation:
            return {}

        total_document = self.browser.find_element(
            By.XPATH, """
            //div[contains(@class,'ui segment padded article-box')]//div[contains(@class,'ui top attached label')]
            """
        ).text.replace('Articles', '').replace('Documents', '').strip()

        articles = self.browser.find_elements(
            By.XPATH, """
            //div[contains(@class,'ui segment padded article-box')]//div[contains(@class,'article-item')]
            """
        )
        data_list = []
        for article in articles:
            title = article.find_element(
                    By.XPATH, ".//a[contains(@class,'title-article')]"
                    )
            garuda_url = title.get_attribute('href').strip()
            garuda_id = title.get_attribute('href').replace(
                'https://garuda.kemdikbud.go.id/documents/detail/', ''
            )
            volume, publisher = article.find_elements(
                    By.XPATH, ".//xmp[contains(@class,'subtitle-article')]"
                    )
            _, file, source, gsholar, _ = article.find_elements(
                    By.XPATH, ".//p[contains(@class,'action-article')]//a[contains(@class,'title-citation')]"
                    )
            # abstract = article.find_element(
            #         By.XPATH, ".//xmp[contains(@class,'abstract-article')]"
            #         )
            # data = {
            #     "garuda_id": int(garuda_id),
            #     "garuda_url": garuda_url,
            #     "title": title.text.strip(),
            #     "volume": volume.text.strip(),
            #     "publisher": publisher.text.strip(),
            #     "file_url": file.get_attribute('href').strip() if file else None,
            #     "source_url": source.get_attribute('href').strip() if source else None,
            #     "gsholar_url": unquote(gsholar.get_attribute('href').strip()) if gsholar else None,
            #     # "abstract": abstract.text.strip(),
            #     "total_journal_document": int(total_document)
            # }
            data = {}
            data_list.append(data)
            data.update(data_values)
            logger.info(data)
        return data_list


    def go_next(self):
        """go next"""

        exclamation = self.browser.find_elements(
            By.XPATH, """
            //h1[contains(@class,'ui icon header red')]//i[contains(@class,'exclamation icon orange')]
            """
        )
        if exclamation:
            return False

        links = self.browser.find_elements(
            By.XPATH, """
            //div[contains(@class,'ui segment padded article-box')]
            //div[contains(@class,'column right aligned')]
            //a
            """
        )
        link_active = self.browser.find_element(
            By.XPATH, """
            //div[contains(@class,'ui segment padded article-box')]
            //div[contains(@class,'column right aligned')]
            //a[contains(@class,'red')]
            """
        )

        if link_active.get_attribute('href').strip() == links[-1].get_attribute('href').strip():
            logger.info("selesai scrap ketika sampai di %s", self.browser.current_url)
            return False

        _, page = link_active.get_attribute('href').split('?page=')
        next_page = int(page)+1
        next_url = self.browser.find_element(
            By.XPATH, f"""
            //div[contains(@class,'ui segment padded article-box')]
            //div[contains(@class,'column right aligned')]
            //a[contains(@href, '?page={next_page}')]
            """
        )
        next_url.click()
        return True

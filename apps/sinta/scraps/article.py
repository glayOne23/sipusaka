"""Module fror scrapping list of universities"""

import logging
from urllib.parse import unquote

from apps.sinta.scraps.scrapsinta import ScrapSinta
from selenium.webdriver.common.by import By

logger = logging.getLogger(__name__)

class ScrapArticle(ScrapSinta):
    """Scrap all article in general"""

    def get_data(self, data_values:dict = None) -> list:
        logger.info(
            f"proses url: %s - {self.browser.current_url}", data_values['journal'].id
        )

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
        ).text.replace('Articles', '').replace('Documents', '').replace(',','').strip()

        if int(total_document) == 0:
            return {}

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

            actions = article.find_elements(
                    By.XPATH, ".//p[contains(@class,'action-article')]//a[contains(@class,'title-citation')]"
                    )
            file_url, source_url, gsholar_url, pdf_url, doi_url = None, None, None, None, None
            for action in actions[1:]:
                if 'Download Original' in action.text:
                    file_url = action.get_attribute('href').strip()
                elif 'Original Source' in action.text:
                    source_url = action.get_attribute('href').strip()
                elif 'Google Scholar' in action.text:
                    gsholar_url = unquote(action.get_attribute('href').strip())
                elif 'Full PDF' in action.text:
                    pdf_url = unquote(action.get_attribute('href').strip())
                elif 'DOI'in action.text:
                    doi_url = action.get_attribute('href').strip()

            author_list = []
            authors = article.find_elements(
                    By.XPATH, ".//a[contains(@class,'author-article')]"
                    )
            for author in authors:
                author_list.append({
                    "name": author.text,
                    "url": author.get_attribute('href').strip()
                })
            data = {
                "garuda_id": int(garuda_id),
                "garuda_url": garuda_url,
                "title": title.text.strip(),
                "author": author_list,
                "volume": volume.text.strip(),
                "publisher": publisher.text.strip(),
                "file_url": file_url,
                "source_url": source_url,
                "gsholar_url": gsholar_url,
                "pdf_url": pdf_url,
                "doi_url": doi_url,
                "total_journal_document": int(total_document)
            }
            data_list.append(data)
            data.update(data_values)
            # logger.info(data)
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

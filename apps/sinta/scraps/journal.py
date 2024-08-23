"""Module fror scrapping list of universities"""

import logging

from apps.sinta.scraps.scrapsinta import ScrapSinta, ScrapSintaDetail
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

logger = logging.getLogger(__name__)

class ScrapJournal(ScrapSinta):
    """Scrap all journal in general"""

    def get_data(self, data_values:dict = None) -> list:
        journals = self.browser.find_elements(By.CLASS_NAME, "list-item")
        data_list = []
        for journal in journals:
            affil_name = journal.find_element(
                    By.XPATH, ".//div[contains(@class,'affil-name')]//a"
                    )
            gsholar_url, website_url, editor_url = journal.find_elements(
                    By.XPATH, ".//div[contains(@class,'affil-abbrev')]//a"
                    )
            profile_id = journal.find_element(
                    By.XPATH, ".//div[contains(@class,'profile-id')]"
                    ).text.strip()
            pissn, eissn, subject = None, None, None
            if 'P-ISSN :' in profile_id:
                pissn = profile_id.split(" | ")[0].split('P-ISSN :')[1].strip()
            if 'E-ISSN :' in profile_id:
                eissn = profile_id.split(" | ")[1].split('E-ISSN :')[1].strip()
                if 'Subject Area :' in eissn:
                    eissn = eissn.split("Subject Area : ")[0].strip()
            if 'Subject Area :' in profile_id:
                subject = profile_id.split("Subject Area :")[1].strip()

            accredited = journal.find_elements(By.XPATH, ".//span[contains(@class,'accredited')]")
            accredited = accredited[0].text if accredited else None
            scopus = journal.find_elements(By.XPATH, ".//span[contains(@class,'scopus-indexed')]")
            scopus = scopus[0].text if scopus else None
            garuda = journal.find_elements(
                By.XPATH, ".//a[contains(@href,'garuda.kemdikbud.go.id/journal/view')]"
                )
            garuda_url = garuda[0].get_attribute('href') if garuda else None
            impact, h5_index, citation_5y, citation = journal.find_elements(
                    By.XPATH, ".//div[contains(@class,'no-gutters')]//div[contains(@class,'col-4 col-lg col-sm-4 col-md-4')]"
                    )
            image = journal.find_element(
                    By.XPATH, ".//div[contains(@class,'profile-side journal-profile')]//img"
                    )
            data = {
                "sinta_id": int(
                    affil_name.get_attribute('href').strip()
                    .split("https://sinta.kemdikbud.go.id/journals/profile/")[1]
                ),
                "name": affil_name.text.strip(),
                "url": affil_name.get_attribute('href').strip(),
                "gsholar_url": gsholar_url.get_attribute('href').strip(),
                "website_url": website_url.get_attribute('href').strip(),
                "editor_url": editor_url.get_attribute('href').strip(),
                "pissn": pissn,
                "eissn": eissn,
                "subject": subject,
                "accredited": accredited,
                "scopus": scopus,
                "garuda_url": garuda_url,
                "impact": impact.text.replace("Impact", "").strip(),
                "h5_index": h5_index.text.replace("H5-index", "").strip(),
                "citation_5y": citation_5y.text.replace("Citations 5yr", "").strip(),
                "citation": citation.text.replace("Citations", "").strip(),
                "image_url": image.get_attribute('src').strip()
            }
            if garuda:
                garuda[0].send_keys(Keys.CONTROL + Keys.ENTER)
                detail = ScrapJournalGaruda(self.browser).scrap()
                data.update(detail)
            data.update(data_values)
            data_list.append(data)
            # logger.info(data)

        return data_list


class ScrapJournalGaruda(ScrapSintaDetail):
    """Scrap detail journal from garuda"""

    def get_data(self, data_values:dict = None) -> list:
        exclamation = self.browser.find_elements(
            By.XPATH, """
            //h1[contains(@class,'ui icon header red')]//i[contains(@class,'exclamation icon orange')]
            """
        )
        if exclamation:
            return {}

        description = self.browser.find_elements(
            By.XPATH, """
            //div[contains(@class,'j-meta-desc')]
            """
        )
        garuda_image = self.browser.find_element(
            By.XPATH, """
            //div[contains(@class,'j-meta-img')]//img
            """
        )
        garuda_subject = self.browser.find_element(
            By.XPATH, """
            //div[contains(@class,'j-info-box')]
            //div[contains(text(),'Core Subject :')]
            """
        )
        arjuna_subject = self.browser.find_element(
            By.XPATH, """
            //div[contains(@class,'j-info-box')]
            //div[contains(text(),'Arjuna Subject :')]
            """
        )
        _, doi, _, _ = self.browser.find_elements(
            By.XPATH, """
            //div[contains(@class,'j-info-box')]
            //div[contains(@class,'j-meta-pub')]
            """
        )
        detail = {
            "garuda_description": description[0].text.strip() if description else None,
            "garuda_image_url": garuda_image.get_attribute('src').strip(),
            "garuda_subject": garuda_subject.text.replace('Core Subject :', '').strip(),
            "aruna_subject": arjuna_subject.text.replace('Core Subject :', '').strip(),
            "doi_url": doi.text.split('DOI :')[1].strip()
        }
        return detail

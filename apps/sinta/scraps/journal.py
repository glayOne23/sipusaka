"""Module fror scrapping list of universities"""

import logging

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from apps.sinta.models.university import University

logger = logging.getLogger(__name__)


def scrap_university(browser):
    """Scrap all universities in general"""

    while True:
        try:
            logger.info("proses url: %s", browser.current_url)

            WebDriverWait(driver=browser, timeout=5).until(
                expected_conditions.presence_of_all_elements_located((By.TAG_NAME, "body"))
            )

            universities = browser.find_elements(By.CSS_SELECTOR, ".content-list > .list-item")

            data_list = []
            for univ in universities:
                sinta_id, sinta_code = univ.find_element(
                        By.XPATH, ".//div[contains(@class,'profile-id')]"
                        ).text.strip().split("ID : ")[1].split(" | CODE :")
                affil_name = univ.find_element(
                        By.XPATH, ".//div[contains(@class,'affil-name')]//a"
                        )
                abbrev = univ.find_element(
                        By.XPATH, ".//div[contains(@class,'affil-abbrev')]"
                        ).text.strip()
                total_department = int(
                            univ.find_element(
                            By.XPATH, ".//span[contains(@class,'num-stat')]//a"
                            ).text.strip().split(' Department')[0]
                        )
                total_author = int(
                            univ.find_element(
                            By.XPATH, ".//span[contains(@class,'num-stat ml-3')]"
                            ).text.strip().split(' Authors')[0].replace(",", '')
                        )

                data = {
                    "sinta_id": int(sinta_id),
                    "sinta_code": sinta_code,
                    "name": affil_name.text.strip(),
                    "url": affil_name.get_attribute('href').strip(),
                    "abbrev": abbrev,
                    "total_department": total_department,
                    "total_author": total_author
                }

                affil_name.send_keys(Keys.CONTROL + Keys.ENTER)
                detail = scrap_detail_university(browser)
                data.update(detail)

                data_list.append(data)
                # logger.info(data)

        except TimeoutException:
            logger.warning("ada error timeout ketika sampai di %s", browser.current_url)
            break
        except ConnectionRefusedError:
            logger.warning(
                "ada error Connection refused timeout ketika sampai di %s", browser.current_url
                )
            break

        url_next = browser.find_element(By.LINK_TEXT, "Next")
        if not url_next:
            logger.info("selesai scrap ketika sampai di %s", browser.current_url)
            break
        browser.execute_script("arguments[0].click();", url_next)
        # url_next.click()



def scrap_detail_university(browser):
    """Scrap detail university"""

    browser.switch_to.window(browser.window_handles[1])

    WebDriverWait(driver=browser, timeout=5).until(
        expected_conditions.visibility_of_element_located((By.XPATH, """
        //table[contains(@class,'table table-borderless table-sm text-center stat-table')]
        """))
    )

    author, department, journal = browser.find_elements(
        By.XPATH, """
        //div[contains(@class,'row stat-card affil-profile-card')]
        //div[contains(@class,'col-md mb-2')]
        //div[contains(@class,'stat-num')]
        """
    )

    article_total = browser.find_elements(
        By.XPATH, """
        //table[contains(@class,'table table-borderless table-sm text-center stat-table')]
        //td
        """
    )

    # for idx, td in enumerate(article_total):
    #     print(idx, td.get_attribute('innerHTML'), td.text)

    def change_to_int(obj):
        return  int(obj.get_attribute('innerHTML').strip().replace('.', ''))

    detail = {
        "total_author": int(author.text.strip().replace('.', '')),
        "total_department": int(department.text.strip().replace('.', '')),
        "total_journal": int(journal.text.strip().replace('.', '')),
        "total_document_scopus": change_to_int(article_total[1]),
        "total_document_gsholar": change_to_int(article_total[2]),
        "total_document_wos": change_to_int(article_total[3]),
        "total_document_garuda": change_to_int(article_total[4]),
        "total_citation_scopus": change_to_int(article_total[6]),
        "total_citation_gsholar": change_to_int(article_total[7]),
        "total_citation_wos": change_to_int(article_total[8]),
        "total_citation_garuda": change_to_int(article_total[9]),
    }

    browser.close()
    browser.switch_to.window(browser.window_handles[0])
    return detail

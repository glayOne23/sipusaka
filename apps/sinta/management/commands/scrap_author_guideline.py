"""Module command fror scrapping list of universities"""

import logging

from apps.sinta.models.journal import Journal
from apps.sinta.scraps._helper import get_browser
from selenium.common.exceptions import WebDriverException
from apps.sinta.scraps.journal_author_guideline import ScrapAuthorGuideline
from django.core.management.base import BaseCommand

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    """command fror scrapping list of universities"""

    browser = None
    help = 'Untuk Scraping data Universitas di sinta'

    # def __init__(self):
    #     super().__init__()
    #     self.browser = get_browser()

    def handle(self, *args, **options):
        logger.info("mulai scrap Author Guideline")
        journals = Journal.objects.filter(website_url__isnull=False, author_guideline_url__isnull=True, id__gt=14, university__gt=131)
        for journal in journals:
            browser = get_browser()
            try:
                browser.get(journal.website_url)
            except WebDriverException as e:
                # print(e)
                if "ERR_CONNECTION_REFUSED" in str(e):
                    logger.warning(
                        f"ada error ERR_CONNECTION_REFUSED di: %s", journal.website_url
                    )
                browser.quit()
                continue
            ScrapAuthorGuideline(browser, data_values={'journal': journal}).scrap(Journal)
            browser.quit()

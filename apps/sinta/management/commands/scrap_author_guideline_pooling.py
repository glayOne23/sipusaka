"""Module command fror scrapping list of universities"""

import logging

import multiprocessing
from django.db import close_old_connections
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
        journals = list(Journal.objects.filter(website_url__isnull=False, id__gt=415, author_guideline_url__isnull=True))

        # Start multiprocessing
        with multiprocessing.Pool(processes=5) as pool:
            pool.map(scrape_author_guideline, journals)


def scrape_author_guideline(journal):
    """Function to scrape articles for a single journal. This will run in a separate process."""
    # Ensure the connection is clean for each process
    close_old_connections()
    browser = get_browser()
    try:
        try:
            browser.get(journal.website_url)
        except WebDriverException as e:
            # print(e)
            if "ERR_CONNECTION_REFUSED" in str(e):
                logger.warning(
                    f"ada error ERR_CONNECTION_REFUSED di: %s", journal.website_url
                )
            browser.quit()
        ScrapAuthorGuideline(browser, data_values={'journal': journal}).scrap(Journal)
        browser.quit()
    finally:
        # Close the connection after scraping to prevent connection leaks
        close_old_connections()
"""Module command fror scrapping list of universities"""

import logging

from apps.sinta.management.commands._helper import get_browser
from apps.sinta.scraps.university import scrap_university
from django.core.management.base import BaseCommand

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    """command fror scrapping list of universities"""

    browser = None
    help = 'Untuk Scraping data Universitas di sinta'

    def __init__(self):
        super().__init__()
        self.browser = get_browser()

    def handle(self, *args, **options):
        logger.info("mulai scrap University")
        url_start = "https://sinta.kemdikbud.go.id/affiliations"
        self.browser.get(url_start)
        scrap_university(browser=self.browser)  # untuk scrap data ums pada umumnya dari sinta

        # try:
        #     while True:
        #         time.sleep(10)  # Keep the command running
        # except KeyboardInterrupt:
        #     logger.info("sudah selesai scrap University")
        #     self.browser.quit()

"""Module command fror scrapping list of journals"""

import logging

from apps.sinta.models.university import University
from apps.sinta.models.journal import Journal
from apps.sinta.scraps._helper import get_browser
from apps.sinta.scraps.journal import ScrapJournal
from django.core.management.base import BaseCommand

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    """command fror scrapping list of journals"""

    browser = None
    help = 'Untuk Scraping data jurnal di sinta'

    def __init__(self):
        super().__init__()
        self.browser = get_browser()

    def handle(self, *args, **options):
        logger.info("mulai scrap journal")
        # universities = University.objects.all()
        universities = University.objects.filter(id__gt=389)
        for univ in universities:
            if univ.total_journal:
                url_start = f"https://sinta.kemdikbud.go.id/journals/index/{univ.sinta_id}"
                self.browser.get(url_start)
                ScrapJournal(self.browser, data_values={'university': univ}).scrap(Journal)

        # try:
        #     while True:
        #         time.sleep(10)  # Keep the command running
        # except KeyboardInterrupt:
        #     logger.info("sudah selesai scrap University")
        #     self.browser.quit()

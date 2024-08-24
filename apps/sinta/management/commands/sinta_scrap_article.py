"""Module command fror scrapping list of universities"""

import logging

from apps.sinta.models.journal import Journal
from apps.sinta.scraps._helper import get_browser
from apps.sinta.scraps.article import ScrapArticle
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
        logger.info("mulai scrap Article")
        journals = Journal.objects.filter(garuda_url__isnull=False)
        for journal in journals:
            self.browser.get(journal.garuda_url)
            ScrapArticle(self.browser, data_values={'journal': journal}).scrap()

"""Module command fror scrapping list of universities"""

import logging

from apps.sinta.models.article import Article
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
        journals = Journal.objects.filter(garuda_url__isnull=False, id__gte=5563)
        for journal in journals:
            if journal.garuda_url == 'https://garuda.kemdikbud.go.id/journal/view/27281':
                self.browser.get('https://garuda.kemdikbud.go.id/journal/view/27281?page=4')
            else:
                self.browser.get(journal.garuda_url)
            # self.browser.get(journal.garuda_url)
            ScrapArticle(self.browser, data_values={'journal': journal}).scrap(Article)

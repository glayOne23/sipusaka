"""Module command fror scrapping list of universities"""

import logging
import multiprocessing

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

    def handle(self, *args, **options):
        logger.info("Mulai scrap Article")
        journals = list(Journal.objects.filter(garuda_url__isnull=False))

        # Start multiprocessing
        with multiprocessing.Pool(processes=6) as pool:
            pool.map(scrape_journal, journals)

def scrape_journal(journal):
    """Function to scrape articles for a single journal. This will run in a separate process."""
    browser = get_browser()

    browser.get(journal.garuda_url)
    ScrapArticle(browser, data_values={'journal': journal}).scrap()

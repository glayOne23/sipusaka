"""Module command fror scrapping list of universities"""

import logging

from apps.sinta.models.article import Article
from django.core.management import call_command
from django.core.management.base import BaseCommand
from django.db.models import Max

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Dump data article in chunks of 100_000 records.'

    def handle(self, *args, **kwargs):
        batch_size = 100_000
        max_id = Article.objects.aggregate(max_id=Max('id'))['max_id']

        for start_id in range(1, max_id + 1, batch_size):
            end_id = min(start_id + batch_size - 1, max_id)
            output_file = f'dump_{start_id}_{end_id}.json'
            print(f'Dumping records {start_id} to {end_id} into {output_file}...')

            articles = list(Article.objects.filter(id__gte=start_id, id__lte=end_id).values_list('id', flat=True))
            article_str = ','.join(map(str, articles))
            article_str = article_str[:-1]

            with open(output_file, 'w', encoding="utf-8") as f:
                call_command('dumpdata', 'sinta.article', '--pks', article_str, stdout=f)

        print('Data dumping complete.')

"""Module fror scrapping list of universities"""

import logging

from apps.sinta.scraps.scrapsinta import ScrapSinta

logger = logging.getLogger(__name__)

class ScrapJournal(ScrapSinta):
    """Scrap all journal in general"""

    def get_data(self) -> list:
        return []

import datetime

import logger
from adhan import adhan
from adhan.methods import ISNA, ASR_STANDARD

log = logger.get_logger(__name__)


def get_prayer_times(method, lat, long):
    params = {}
    params.update(ISNA)
    params.update(ASR_STANDARD)

    return adhan(
        day=datetime.date.today(),
        location=(lat, long),
        parameters=params,
        timezone_offset=-7,
    )

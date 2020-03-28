import datetime
import time
import logger
import time

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
        timezone_offset=get_timezone_offset(),
    )


def get_timezone_offset():
	ts = time.time()
	utc_offset = (datetime.datetime.fromtimestamp(ts) - datetime.datetime.utcfromtimestamp(ts)).total_seconds()
	return utc_offset / 3600

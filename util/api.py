import datetime
import requests
import json
import config
import logger

from adhan import adhan
from adhan.methods import ISNA, ASR_STANDARD

log = logger.get_logger(__name__)

class InvalidRequestError(Exception):
    pass


def get_prayer_times_api(city, state, country, month, year):
    payload = {
        'city': city,
        'country': country,
        'state': state,
        'month': month,
        'year': year,
        'method': config.default['method']
    }
    response = requests.get(config.default['azan_end_point'], params=payload)

    if response.status_code != requests.codes.ok:
        raise InvalidRequestError('Oops something went wrong here!')
    log.info('got response from azan api')
    prayers = response.json()['data']
    current_date = (datetime.datetime.now() + datetime.timedelta(days=1)).date()

    for prayer in prayers:
        prayer_date = datetime.datetime.strptime(
            prayer['date']['gregorian']['date'], '%d-%m-%Y')

        if prayer_date.date() == current_date:
            return prayer['timings']

    raise InvalidRequestError('Oops, something went wrong, could not find the correct date')

def get_prayer_times(lat, long):
    params = {}
    params.update(ISNA)
    params.update(ASR_STANDARD)

    return adhan(
        day=datetime.date.today(),
        location=(lat, long),
        parameters=params,
        timezone_offset=-7,
    )

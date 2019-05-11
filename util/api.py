import datetime
import requests
import json
import config
import logger

log = logger.get_logger(__name__)

class InvalidRequestError(Exception):
    pass


def get_prayer_times(city, state, country, month, year):
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

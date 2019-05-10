import datetime
import os
import sys
import logger

log = logger.get_logger(__name__)


def play(name=None):
    if not name:
        name = 'azan.mp3'
    path = os.path.dirname(os.path.abspath(__file__))
    file_path = '{}/../assets/{}'.format(path, name)
    log.info('Calling Azan now')
    log.info(file_path)
    os.system('cvlc --play-and-exit {}'.format(file_path))


def format_azan_time(azan_time):
    azan = azan_time.split(' ')[0]
    azan = datetime.datetime.strptime(azan, "%H:%M")
    azan = datetime.datetime.now().replace(hour=azan.hour, minute=azan.minute)
    return azan

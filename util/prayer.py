import datetime
import os
import sys
import logger
import simpleaudio 

log = logger.get_logger(__name__)


def play(name=None, azan_name=None):
    if not name:
        name = 'azan.wav'

    path = os.path.dirname(os.path.abspath(__file__))
    file_path = '{}/../assets/{}'.format(path, name)
    log.info('Calling {} azan now'.format(azan_name))

    wave_obj = simpleaudio.WaveObject.from_wave_file(file_path)
    play_obj = wave_obj.play()
    play_obj.wait_done()  

import datetime
import os
import sys
import logger
import pygame

log = logger.get_logger(__name__)


def play(name=None):
    if not name:
        name = 'azan.mp3'
    path = os.path.dirname(os.path.abspath(__file__))
    file_path = '{}/../assets/{}'.format(path, name)
    log.info('Calling Azan now')
    pygame.init()
    pygame.mixer.music.load(file_path)
    pygame.mixer.music.play(0)

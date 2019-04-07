import datetime
import os
import playsound
import sys


def play(name=None):
    if not name:
        name = 'azan.mp3'
    path = os.path.abspath(f'assets/{name}')
    print('Calling azan now.')
    playsound.playsound(path)


def format_azan_time(azan_time):
    azan = azan_time.split(' ')[0]
    azan = datetime.datetime.strptime(azan, "%H:%M")
    azan = datetime.datetime.now().replace(hour=azan.hour, minute=azan.minute)
    return azan

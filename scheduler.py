import config
import datetime
import sched
import time
import util.prayer
import util.api

AZAN_ENUM = ['Fajr', 'Dhuhr', 'Asr', 'Maghrib', 'Isha']

scheduler = sched.scheduler(time.time, time.sleep)
now = datetime.datetime.now()

azan_times = util.api.get_prayer_times(
    config.default['city'],
    config.default['state'],
    config.default['country'],
    now.date().month,
    now.date().year)

for azan_name in AZAN_ENUM:
    azan_time = util.prayer.format_azan_time(azan_times[azan_name])

    if now > azan_time:
        continue
    
    print(f'Schedule {azan_name} at {azan_time}')
    scheduler.enterabs(azan_time.timestamp(), 1, util.prayer.play)

scheduler.run()

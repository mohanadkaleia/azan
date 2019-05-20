import config
import datetime
import sched
import time
import util.prayer
import util.api
import logger
import schedule


log = logger.get_logger(__name__)

AZAN_ENUM = ['fajr', 'zuhr', 'asr', 'maghrib', 'isha']
LAT = config.default['lat']
LONG = config.default['long']
METHOD = config.default['method']


def main():
    scheduler = sched.scheduler(time.time, time.sleep)
    now = datetime.datetime.now()
    log.info('Sending a request to azan API')
    azan_times = util.api.get_prayer_times(METHOD, LAT, LONG)

    for azan_name in AZAN_ENUM:
        now = datetime.datetime.now()
        azan_time = azan_times[azan_name]

        if now > azan_time:
            continue

        log.info('{} is scheduled at {}'.format(azan_name, azan_time))
        scheduler.enterabs(float(azan_time.strftime('%s')), 1, util.prayer.play, ({azan_time:azan_name}))

    scheduler.run()


if __name__ == '__main__':
    try:
        main()
        schedule.every().day.at("01:00").do(main)
        while True:
            schedule.run_pending()
            time.sleep(60)  # wait one minute
    except Exception:
        log.exception('Oops something went wrong')
        raise

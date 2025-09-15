import config
import datetime
import sched
import time
import util.prayer
import util.api
import logger
import schedule
import sys


log = logger.get_logger(__name__)

AZAN_ENUM = ['fajr', 'zuhr', 'asr', 'maghrib', 'isha']
LAT = config.default['lat']
LONG = config.default['long']
METHOD = config.default['method']

def display_pioled(azan_schedule):
    from util.display import Display
    pioled = util.display.Display()
    pioled.draw_text(azan_schedule)

def safe_prayer_call(azan_name):
    """Safely execute prayer call with error handling"""
    try:
        log.info(f'Playing {azan_name} prayer call...')
        util.prayer.play(azan_name=azan_name)
        log.info(f'{azan_name} prayer call completed')
    except Exception as e:
        log.error(f'Failed to play {azan_name} prayer: {e}')

def main():
    scheduler = sched.scheduler(time.time, time.sleep)
    now = datetime.datetime.now()
    azan_times = util.api.get_prayer_times(METHOD, LAT, LONG)

    azan_schedule_disp = []
    for azan_name in AZAN_ENUM:
        now = datetime.datetime.now()
        azan_time = azan_times[azan_name]
        
        # Skip if the azan time is passed or if the azan is muted
        if now > azan_time or not config.default[azan_name]:
            continue

        log.info('{} is scheduled at {}'.format(azan_name, azan_time))
        azan_schedule_disp.append('{} at {}'.format(azan_name, azan_time.strftime("%H:%M")))
        scheduler.enterabs(float(azan_time.strftime('%s')), 1, safe_prayer_call, argument=(azan_name,))

    if config.default['pioled']:
        display_pioled(azan_schedule_disp)


    scheduler.run()

if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'test':
        util.prayer.play()     
    else:
        # Schedule main to run at 1:00 AM every day
        schedule.every().day.at("01:00").do(main)
        
        # Run main once initially to schedule today's prayers
        try:
            main()
        except Exception:
            log.exception('Error in initial prayer scheduling')
        
        # Main loop to check for daily rescheduling
        while True:
            try:
                schedule.run_pending()
                time.sleep(60)  # Check every minute
            except Exception:
                log.exception('Oops something went wrong')
                time.sleep(60)  # Continue running even if error occurs

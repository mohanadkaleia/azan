from crontab import CronTab
import logger 

log = logger.get_logger(__name__)

log.info("Start the cron job")
cron = CronTab(user=True)
job = cron.new(command='python /home/pi/workspace/azan/scheduler.py', comment='Azan Job')
job.hour.on(1)  
cron.write()

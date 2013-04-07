from apscheduler.scheduler import Scheduler
from worker import add_update_task
from airead.models import FeedSite

import logging
import datetime
import os


SCHED_LOG_FILE = "clocklog.log"

sched = Scheduler()

@sched.cron_schedule(hour='0')
#@sched.interval_schedule(minutes=1)
def clock_task():
    # update all sites
    sites = FeedSite.query.all()
    for s in sites:
        add_update_task(s.id)

#@sched.interval_schedule(seconds=1)
#def test():
#    #init_sched_log()
#    print FeedSite.query.count()


sched.start()
while True:
    pass

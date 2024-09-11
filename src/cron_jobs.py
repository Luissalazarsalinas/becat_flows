import os
from pathlib import Path
from crontab import CronTab

# Base path
BASE_PATH = Path(__file__).resolve(strict=True).parent


# Create a instance of cron job to current user
cron = CronTab(user=True)

# Create a new cron job
job = cron.new(command=f'python  {BASE_PATH}{os.sep}main.py', comment='Becat flows jobs')


# Set schedule in this case the jobs going to run at 5:15 PM from monday to friday
job.setall('15 17 * * 1-5') # munites, hours, day (months) , month, days of weeks   

# saved job 
# cron.write()

print('Cron job created!')
import os
from pathlib import Path
from crontab import CronTab

# Base path
BASE_PATH = Path(__file__).resolve(strict=True).parent


# Create a instance of cron job to current user
cron = CronTab(user=True)

# Create a new cron job
job = cron.new(command=f'python3  {BASE_PATH}{os.sep}main.py >> {BASE_PATH}{os.sep}var{os.sep}log{os.sep}out.log >> {BASE_PATH}{os.sep}var{os.sep}log{os.sep}cron.log', comment='Becat flows jobs')


# Set schedule in this case the jobs going to run at 5:15 PM from monday to friday
job.setall('50 12 * * 1-5') # munites, hours, day (months) , month, days of weeks   

# saved job 
cron.write()

print('Cron job created!')
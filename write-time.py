from crontab import CronTab
from datetime import datetime


with open('./dataInfo.txt', 'a') as outFile:
  outFile.write('\n' + str(datetime.now()))

cron = CronTab(user='peterle')
job = cron.new(command='sudo python3 ./test.py \n loc123456')

job.minute.every(1/60)

cron.write()
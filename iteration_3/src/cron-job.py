from crontab import CronTab
import os, sys
import subprocess
from config import DevConfig
import json
import time

my_cron = CronTab(user='pi')
configured = False
job = None

for _job in my_cron:
    if _job.comment == 'proc_mon':
        configured = True
        job = _job

if len(sys.argv)>1:
    if 'r' in sys.argv[1]:
        if job == None:
            exit(0)
        my_cron.remove(job)
        my_cron.write()
        exit(0)

if not configured:
    path = os.path.realpath(__file__)
    cmd = "python {0}".format(path)
    job = my_cron.new(command=cmd, comment='proc_mon')
    job.minute.every(1)
    my_cron.write()

process_ids = []
scripts = ["device.py"]
for module_name in scripts:
    res = subprocess.check_output("pgrep -lf device.py", shell=True).split()
    idx = res.index("python")
    if idx > 0:
        process_ids += [res[idx-1]]

cron_result = dict()
cron_result['time'] = time.time()

for key, value in zip(scripts, process_ids):
    cron_result[key] = value

with open("{0}{1}{2}".format(DevConfig.STATUS_DIR, os.sep, "proc_mon.json") , 'w') as outfile:
    json.dump(cron_result, outfile)
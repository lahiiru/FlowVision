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

cron_result = dict()
cron_result['timestmp'] = time.time()

scripts = ["device.py", "processor_1.py", "processor_2.py"]
for module_name in scripts:
    res = subprocess.check_output("pgrep -lf {0}".format(module_name), shell=True).split()
    if "python" in res:
        idx = res.index("python")
        if idx > 0:
            cron_result[module_name] = res[idx-1]
        else:
            cron_result[module_name] = "0"

with open("{0}{1}{2}".format(DevConfig.STATUS_DIR, os.sep, "proc_mon.json") , 'w') as outfile:
    json.dump(cron_result, outfile)

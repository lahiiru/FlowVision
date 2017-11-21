from crontab import CronTab
import os, sys
import subprocess
from config import DevConfig
import json
import time
import os

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

kill_flag = "{0}{1}{2}".format(DevConfig.STATUS_DIR, os.sep, "kill")
if os.path.exists(kill_flag):
    try:
        res = subprocess.check_output("killall python")
    except:
        pass
    finally:
        os.remove(kill_flag)

cron_result = dict()
cron_result['timestmp'] = time.time()

scripts = ["device.py", "processor_1.py", "processor_2.py"]
for module_name in scripts:
    found = False
    res = subprocess.check_output("pgrep -lf {0}".format(module_name), shell=True).split()
    if "python" in res:
        idx = res.index("python")
        if idx > 0:
            found = True
            cron_result[module_name] = res[idx-1]
        else:
            cron_result[module_name] = "0"
    if not found:
        subprocess.Popen(['nohup', 'python -u /var/www/html/FlowVision/iteration_3/src/{0}'.format(module_name)],
                         stdout=open('/var/www/html/FlowVision/iteration_3/src/device.log', 'w'),
                         stderr=open('/var/www/html/FlowVision/iteration_3/src/device.log', 'a'),
                         preexec_fn=os.setpgrp
                         )
        subprocess.Popen(['python', '/var/www/html/FlowVision/iteration_3/src/{0}'.format(module_name), '0'], close_fds=True)

with open("{0}{1}{2}".format(DevConfig.STATUS_DIR, os.sep, "proc_mon.json") , 'w') as outfile:
    json.dump(cron_result, outfile)

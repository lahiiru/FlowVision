from sensor_process import SensorProcess
import logging
from logging.config import fileConfig
import os

path = os.path.realpath(__file__)
if '.zip' in path:
    cur_dir = path.rsplit(os.sep, 2)[0]
else:
    cur_dir = path.rsplit(os.sep, 1)[0]

log_path = cur_dir + os.sep + 'logging.ini'

if __name__ in ['__main__']:
    fileConfig(log_path)

logger = logging.getLogger()

logger.debug("Processor 2 initializing from, {0}".format(path))

p = SensorProcess(0)
p.run()

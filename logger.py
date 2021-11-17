import logging.handlers
import datetime
import os

if not os.path.exists('logs/'):
    os.mkdir('logs/')
all_logname = 'logs/all.log'
err_logname = 'logs/error.log'

mylogger = logging.getLogger('mylogger')
mylogger.setLevel(logging.INFO)

rf_handler = logging.handlers.TimedRotatingFileHandler(all_logname, when='midnight', interval=1, backupCount=7, atTime=datetime.time(0, 0, 0, 0))
rf_handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))

f_handler = logging.FileHandler(err_logname)
f_handler.setLevel(logging.ERROR)
f_handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(filename)s[:%(lineno)d] - %(message)s"))

mylogger.addHandler(rf_handler)
mylogger.addHandler(f_handler)

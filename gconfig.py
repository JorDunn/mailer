from mailer.config import Config
import multiprocessing
import os

# General
bind = "{0}:{1}".format(Config.HOST, Config.PORT)
backlog = 2048
proc_name = "mailer"

# Workers
workers = multiprocessing.cpu_count() * 2 + 1
worker_class = "sync"
timeout = 30
keepalive = 2

# Logging
errorlog = "{0}/log/error.txt".format(os.getcwd())
accesslog = "{0}/log/access.txt".format(os.getcwd())
loglevel = "info"
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s"'

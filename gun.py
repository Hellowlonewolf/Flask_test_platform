# coding=utf-8
# test
import multiprocessing
import os
import sys

path_of_current_file = os.path.abspath(__file__)
path_of_current_dir = os.path.split(path_of_current_file)[0]

_file_name = os.path.basename(__file__)

sys.path.insert(0, path_of_current_dir)

worker_class = 'sync'
# workers = multiprocessing.cpu_count() * 1 + 1
workers = 2
chdir = path_of_current_dir

worker_connections = 1000
timeout = 30000
max_requests = 2000
graceful_timeout = 30000

loglevel = 'info'

reload = True
debug = False

bind = "%s:%s" % ("0.0.0.0", 5000)
pidfile = '%s/run/%s.pid' % (path_of_current_dir, _file_name)
errorlog = '%s/logs/%s_error.log' % (path_of_current_dir, _file_name)
accesslog = '%s/logs/%s_access.log' % (path_of_current_dir, _file_name)

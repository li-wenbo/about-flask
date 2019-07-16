import multiprocessing
from time import time


# server_hook  http://docs.gunicorn.org/en/stable/settings.html#server-hooks
def handler_on_starting(server):
    print("i am starting %s" % time())

def handler_when_ready(server):
    print("i am ready %s" % time())


# server
pidfile = 'gun.pid'
backlog = 512
bind = "127.0.0.1:8888"
daemon = True
reload = True

# log
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s" %(L)s ' \
                    '"%({X-Forwarded-Proto}i)s" "%({X-Forwarded-For}i)s" "%({X-Real-IP}i)s"'
accesslog = 'logs/access.log'

errorlog = 'logs/error.log'
loglevel = 'debug'

# worker
workers = multiprocessing.cpu_count() * 2 + 1
worker_class = "gevent"
worker_connections = 1024

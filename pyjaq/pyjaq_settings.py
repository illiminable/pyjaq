
###### The number of child worker processes that will exist.
# Note that there will be one additional parent supervisor 
# process. Also if START_NEW_PROCESS_PER_ITEM is True then
# the worker processes will spawn a further child process 
# for the lifetime of each item.
WORKER_COUNT = 2

##### The way child processes are handled.
# 'process' - worker process for each child worker (recommended)
# 'thread' - all run in one process. DON'T USE WITH WORKER_COUNT > 1. Only for testing.
WORKER_MODE = 'process'

BACKENDS = {
    "default": {
        "backend": "redis",
        "host": "192.168.141.128",
        "port": 6379,
    }
}

DEFAULT_QUEUE_SETTINGS = {

}

QUEUES = {
    "hello_queue": {
        "handler": "pyjaq.queue_handlers.HelloHandler",
    },

    "bye_queue": {
        "handler": "pyjaq.queue_handlers.GoodbyeHandler",
    }
}
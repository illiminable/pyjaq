
###### The number of child worker processes that will exist.
# Note that there will be one additional parent supervisor 
# process. Also if START_NEW_PROCESS_PER_ITEM is True then
# the worker processes will spawn a further child process 
# for the lifetime of each item.
WORKER_COUNT = 1

QUEUES = ["name_queue"]
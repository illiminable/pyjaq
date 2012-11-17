import pyjaq.queue_handlers as handlers
from pyjaq.core import RedisQueue

class WorkerQueue(object):
    def __init__(self, queue_name, handler):
        self._q = RedisQueue(queue_name, host="192.168.141.128")
        self._handler = handler

    def length(self):
        return self._q.length()

    def pop(self):
        return self._q.pop()

    def handle_item(self, item):
        self._handler.perform(item)

class QueueManager(object):
    """
    The queue manager handles the mapping of queue names to handler classes.
    When multiple queues are being operated on it also handles which queue
    the worker will work on for each iteration. Derived classes may
    change the way queues are selected. eg. priority list, round-robin, other.
    """
    def __init__(self):
        self._queue_map = {}

        self._map_queues()

    def _map_queues(self):
        # TODO: Unhard code this
        self._queue_map['name_queue'] = WorkerQueue('name_queue', handlers.HelloHandler())

    def get_queue(self):
        """
        Returns a queue for the worker to act on.
        """
        return self._queue_map['name_queue']

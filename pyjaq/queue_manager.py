import pyjaq.queue_handlers as handlers
from pyjaq.backend_loader import create_backend_queue
from pyjaq.reflection import get_class_by_name
import pyjaq.pyjaq_settings as settings

class WorkerQueue(object):
    def __init__(self, queue_name, handler):
        self._q = create_backend_queue(queue_name)
        self._handler = handler

    def length(self):
        return self._q.length()

    def pop(self):
        return self._q.pop()

    def handle_item(self, item):
        self._handler.perform(item)

class WorkerQueueManager(object):
    """
    The queue manager handles the mapping of queue names to handler classes.
    When multiple queues are being operated on it also handles which queue
    the worker will work on for each iteration. Derived classes may
    change the way queues are selected. eg. priority list, round-robin, other.
    """
    def __init__(self):
        self._queue_map = {}
        self._upto_queue = 0

    def load_queues(self):
        # TODO: Make this safer. Check for dupes.
        for queue_name, queue_config in settings.QUEUES.items():
            print "Loading a queue"
            queue_handler_name = queue_config['handler']
            handler_cls = get_class_by_name(queue_handler_name)
            handler = handler_cls()
            queue = WorkerQueue(queue_name, handler)
            self._queue_map[queue_name] = queue

    def get_worker_queue(self):
        """
        Returns a queue for the worker to act on or None if there are none
        or there's nothing to do.
        """
        queue = None
        # TODO: Use an iterator
        if len(self._queue_map) > 0:
            queue_name = self._queue_map.keys()[self._upto_queue]
            queue = self._queue_map[queue_name]
            self._upto_queue = (self._upto_queue + 1) % len(self._queue_map)

        return queue

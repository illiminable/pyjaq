import Queue as memq
import simplejson
from redis import StrictRedis

class QueueItem(object):
    def __init__(self, queue_name, id, data):
        self.queue_name = queue_name
        self.id = id
        self.data = data

class BaseQueue(object):
    def __init__(self, queue_name):
        self.queue_name = queue_name

    def clear(self):
        raise NotImplementedError('clear not implemented on BaseQueue')

    def length(self):
        raise NotImplementedError('length not implemented on BaseQueue')

    def push(self, item):
        raise NotImplementedError('push not implemented on BaseQueue')

    def pop(self):
        raise NotImplementedError('pop not implemented on BaseQueue')



class InMemoryQueue(BaseQueue):
    def __init__(self, queue_name):
        super(InMemoryQueue, self).__init__(queue_name)

        self.q = memq.Queue()

    def clear(self):
        self.q.empty()

    def length(self):
        return self.q.qsize()

    def push(self, data):
        item = QueueItem(self.queue_name, 1234, data)
        self.q.put(item)

    def pop(self):
        return self.q.get()

class RedisQueue(BaseQueue):
    def __init__(self, queue_name, host, port=6379):
        super(RedisQueue, self).__init__(queue_name)
        self._redis = StrictRedis(host=host, port=port)

    def _key_name(self):
        return "pyjaq_%s" % self.queue_name

    def clear(self):
        self._redis.delete(self._key_name())

    def length(self):
        return self._redis.llen(self._key_name())

    def push(self, data):
        item_dict = {
            "id": 1234,
            "data": data
        }

        item_str = simplejson.dumps(item_dict)
        self._redis.rpush(self._key_name(), item_str)

    def pop(self):
        item = None
        item_str = self._redis.lpop(self._key_name())
        item_dict = simplejson.loads(item_str)

        if item_dict:
            item = QueueItem(self.queue_name, item_dict['id'], item_dict['data'])

        return item

class SimpleQueue(InMemoryQueue):
    pass


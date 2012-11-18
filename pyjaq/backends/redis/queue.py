import simplejson
from pyjaq.core import BaseQueue, BaseMeta, QueueItem
from redis import StrictRedis
import traceback

class RedisMeta(BaseMeta):
    def __init__(self, redis):
        self._redis = redis

    def _id_key_name(self):
        return "pyjaq.meta.id"

    def get_item_id(self):
        return self._redis.incr(self._id_key_name())

class RedisQueue(BaseQueue):
    def __init__(self, queue_name, host, port=6379):
        super(RedisQueue, self).__init__(queue_name)
        self._redis = StrictRedis(host=host, port=port)
        self._meta = RedisMeta(self._redis)

    def _key_name(self):
        return "pyjaq.queues.%s.active" % self.queue_name

    def clear(self):
        self._redis.delete(self._key_name())

    def length(self):
        return self._redis.llen(self._key_name())

    def push(self, data):
        item_dict = {
            "id": self._meta.get_item_id(),
            "data": data
        }

        item_str = simplejson.dumps(item_dict)
        self._redis.rpush(self._key_name(), item_str)

    def pop(self):
        item = None
        try:
            item_str = self._redis.lpop(self._key_name())
            if item_str:
                item_dict = simplejson.loads(item_str)
                item = QueueItem(self.queue_name, item_dict['id'], item_dict['data'])
        except:
            print traceback.format_exc()
            raise

        return item
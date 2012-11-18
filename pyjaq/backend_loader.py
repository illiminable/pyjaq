
import pyjaq.pyjaq_settings as settings
from pyjaq.backends.redis.queue import RedisQueue

def create_backend_queue(queue_name, backend_key='default'):
    backend_info = settings.BACKENDS.get(backend_key)

    if not backend_info:
        raise Exception("No backend settings defined for key %s" % backend_key)

    backend_name = backend_info.get("backend")

    if backend_name == 'redis':
        host = backend_info.get("host", "localhost")
        port = backend_info.get("port", 6379)
        return RedisQueue(
                    queue_name,
                    host, 
                    port)

    raise Exception("Key %s requests an unknown backend %s" % (backend_key, backend_name))
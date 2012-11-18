from pyjaq.core import SimpleQueue
from pyjaq.backends.redis.queue import RedisQueue

def sync_in_process():
    q = SimpleQueue("name_queue")
    q.clear()

    for i in range(0, 25):
        q.push(i)

    while q.length() > 0:
        print q.pop()


def push_names_to_redis():
    hello = RedisQueue("hello_queue", host="192.168.141.128")
    bye = RedisQueue("bye_queue", host="192.168.141.128")

    for i in range(0,10):
        hello.push( { "name": "person %s" % i })
        bye.push( { "name": "person %s" % i })

#sync_in_process()
push_names_to_redis()





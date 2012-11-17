from pyjaq.core import SimpleQueue, RedisQueue

def sync_in_process():
    q = SimpleQueue("name_queue")
    q.clear()

    for i in range(0, 25):
        q.push(i)

    while q.length() > 0:
        print q.pop()


def push_names_to_redis():
    q = RedisQueue("name_queue", host="192.168.141.128")

    for i in range(0,10):
        q.push( { "name": "person %s" % i })

#sync_in_process()
push_names_to_redis()





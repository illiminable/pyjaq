import Queue as memq

class QueueItem(object):
    def __init__(self, queue_name, id, data):
        self.queue_name = queue_name
        self.id = id
        self.data = data

class BaseMeta(object):
    def get_item_id(self):
        raise NotImplementedError('get_item_id not implemented on BaseMeta')

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

class SimpleQueue(InMemoryQueue):
    pass


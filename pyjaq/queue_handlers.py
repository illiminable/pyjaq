

class HelloHandler(object):
    supported_queues = ["name_queue"]

    def perform(self, item):
        print "Hello %s" % item.data.get("name")

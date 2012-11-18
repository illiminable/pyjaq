

class HelloHandler(object):
    queue = "hello_queue"

    def perform(self, item):
        print "Hello %s" % item.data.get("name")

class GoodbyeHandler(object):
    queue = "bye_queue"

    def perform(self, item):
        print "Goodbye %s" % item.data.get("name")

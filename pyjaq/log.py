
class pyjaq_log(object):
    """
    TODO: Make thread safe.
    """
    def debug(self, msg):
        print "DEBUG: %s" % msg

    def info(self, msg):
        print "INFO: %s" % msg

    def warning(self, msg):
        print "WARNING: %s" % msg

    def error(self, msg):
        print "ERROR: %s" % msg
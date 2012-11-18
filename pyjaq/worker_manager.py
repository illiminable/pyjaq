import os
import time
from multiprocessing import Process
from threading import Thread

class WorkerManager(object):
    def __init__(self, worker_count, log, queue_manager, mode):
        self._worker_count = worker_count
        self._log = log
        self._queue_manager = queue_manager
        self._workers = []
        self._mode = mode

    @classmethod
    def _worker_func(cls, log, queue_manager):
        log.info("Worker here! pid=%s" % (os.getpid()))

        log.info("Loading queues...")
        queue_manager.load_queues()

        while True:
            log.info("Getting queue...")
            q = queue_manager.get_worker_queue()

            if q:
                item = q.pop()

                if item:
                    log.info("Handling item id=%s" % item.id)
                    q.handle_item(item)
                else:
                    log.info("Queue was empty")

            log.info("Sleeping...")
            time.sleep(1)



        # forever:
        #   select a queue q to act on
        #   if q is not empty:
        #       pop an item from q
        #       pass the item to the handler
        #
        #       if the handler fails:
        #           ???
    def _start_worker_process(self):
        p = Process(target=WorkerManager._worker_func, args=(self._log, self._queue_manager))
        p.start()
        self._workers.append(p)

    def _start_worker_thread(self):
        class WorkerThread(Thread):
            def __init__(self, log, queue_manager):
                super(WorkerThread, self).__init__()
                self._log = log
                self._queue_manager = queue_manager

            def run(self):
                WorkerManager._worker_func(self._log, self._queue_manager)

        t = WorkerThread(self._log, self._queue_manager)
        t.start()
        self._workers.append(t)

    def _start_worker(self):
        if self._mode == 'process':
            self._start_worker_process()
        elif self._mode == 'thread':
            self._start_worker_thread()
        else:
            raise Exception('%s is not a valid worker mode' % self._mode)

    def start(self):
        for i in range(0, self._worker_count):
            self._log.info("Starting worker %s of %s" % (i + 1, self._worker_count))
            self._start_worker()

    def wait(self):
        i = 0
        for worker in self._workers:
            self._log.info("Waiting for worker %s of %s" % (i + 1, self._worker_count))
            i += 1
            worker.join()

        self._workers = []

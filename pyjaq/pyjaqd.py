import pyjaq.pyjaq_settings as settings
from pyjaq.log import pyjaq_log
from pyjaq.worker_manager import WorkerManager
from pyjaq.queue_manager import QueueManager

if __name__ == '__main__':
    log = pyjaq_log()
    log.info("Starting Main Process")

    queue_manager = QueueManager()
    manager = WorkerManager(settings.WORKER_COUNT, log, queue_manager=queue_manager, mode='thread')
    log.info("Main process starting workers")
    manager.start()

    log.info("Main process waiting for workers")
    manager.wait()

    log.info("Main process exiting gracefully")
    


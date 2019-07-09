import logging
import signal
import threading
from datetime import datetime
import multiprocessing
import time

import pyttsx3

logger = logging.getLogger("FAPSTTS")
logger.setLevel(logging.DEBUG)
logging.basicConfig(format='[%(asctime)s][%(name)s]%(levelname)s: %(message)s', datefmt='%Y-%m-%d %H:%M:%S')


class FAPSTTS(multiprocessing.Process):
    def __init__(self, text_queue, interrupt_callback=lambda: False):
        multiprocessing.Process.__init__(self)
        self.text_queue = text_queue
        self.interrupt_callback = interrupt_callback

    def run(self):
        engine = pyttsx3.init()
        engine.startLoop(False)
        while True:
            if self.interrupt_callback():
                logger.debug("detect program interruption... returning")
                return

            next_text = self.text_queue.get()
            if next_text is None:
                time.sleep(0.03)
                continue

            engine.say(next_text, 'text')
            logger.info('FAPS TTS --> "{}"'.format(next_text))
            engine.iterate()

        return


interrupted = False


def myinterrupt_callback():
    global interrupted
    return interrupted


def signal_handler(signal, frame):
    global interrupted
    interrupted = True


def sendIt(queue):
    queue.put("I need a new text")
    threading.Timer(5.0, sendIt, [queue]).start()


if __name__ == '__main__':
    # capture SIGINT signal, e.g., Ctrl+C
    signal.signal(signal.SIGINT, signal_handler)

    # Establish communication queues
    txtInputQueue = multiprocessing.JoinableQueue()
    sstProcess = FAPSTTS(txtInputQueue, myinterrupt_callback)
    sstProcess.start()

    # Timer
    sendIt(txtInputQueue)

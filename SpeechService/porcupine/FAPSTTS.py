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
        self.isBusy = False

    def run(self):
        engine = pyttsx3.init()
        engine.setProperty('volume', 1.0)
        voices = engine.getProperty('voices')
        engine.setProperty('voice', voices[0].id)
        while True:
            if self.interrupt_callback():
                logger.debug("detect program interruption... returning")
                return

            if self.isBusy is True:
                time.sleep(0.03)
                continue

            next_text = self.text_queue.get()
            if next_text is None:
                time.sleep(0.03)
                continue

            engine.say(next_text, 'text')
            logger.info('FAPS TTS --> "{}"'.format(next_text))
            engine.runAndWait()
        return

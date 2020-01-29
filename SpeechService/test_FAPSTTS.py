#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import logging
import multiprocessing
import signal
import threading

from SpeechService.FAPSDeepSpeechConverter import FAPSDeepSpeechConverter
from SpeechService.FAPSTTS import FAPSTTS

try:
    from shhlex import quote
except ImportError:
    from pipes import quote

logger = logging.getLogger("TEST FAPSDeepSpeechConverter")
logger.setLevel(logging.DEBUG)
logging.basicConfig(format='[%(asctime)s][%(name)s]%(levelname)s: %(message)s', datefmt='%Y-%m-%d %H:%M:%S')


interrupted = False


def myinterrupt_callback():
    global interrupted
    return interrupted


def signal_handler(signal, frame):
    global interrupted
    interrupted = True


def sendIt(queue):
    queue.put("I need a new text")
    threading.Timer(10.0, sendIt, [queue]).start()


if __name__ == '__main__':
    # capture SIGINT signal, e.g., Ctrl+C
    signal.signal(signal.SIGINT, signal_handler)

    # Establish communication queues
    textQueue = multiprocessing.JoinableQueue()
    sstProcess = FAPSTTS(textQueue, myinterrupt_callback)
    sstProcess.start()

    # Timer
    sendIt(textQueue)
    logger.info("Exit\n")

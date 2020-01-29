#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import logging
import multiprocessing
import signal
import threading

from SpeechService.FAPSDeepSpeechConverter import FAPSDeepSpeechConverter

try:
    from shhlex import quote
except ImportError:
    from pipes import quote

logger = logging.getLogger("FAPSDeepSpeechConverter")
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
    queue.put("./output/output_audio.wav")
    threading.Timer(10.0, sendIt, [queue]).start()
    logger.info("Timer Event")


if __name__ == '__main__':
    # capture SIGINT signal, e.g., Ctrl+C
    signal.signal(signal.SIGINT, signal_handler)

    # Establish communication queues
    audioInputQueue = multiprocessing.JoinableQueue()
    textOutputQueue = multiprocessing.JoinableQueue()
    sstProcess = FAPSDeepSpeechConverter(audioInputQueue, textOutputQueue, myinterrupt_callback, use_google=False)
    sstProcess.start()

    # Timer
    sendIt(audioInputQueue)
    logger.info("Exit\n")

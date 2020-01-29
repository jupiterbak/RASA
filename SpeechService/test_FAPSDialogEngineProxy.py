import multiprocessing
import signal
import threading

from SpeechService.FAPSDialogEngineProxy import FAPSDialogEngineProxy

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
    txtOutputQueue = multiprocessing.JoinableQueue()
    sstProcess = FAPSDialogEngineProxy(txtInputQueue, txtOutputQueue, myinterrupt_callback)
    sstProcess.start()

    # Timer
    sendIt(txtInputQueue)
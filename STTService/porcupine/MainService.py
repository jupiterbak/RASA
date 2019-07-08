import multiprocessing
import signal

from STTService.porcupine.FAPSDeepSpeechConverter import FAPSDeepSpeechConverter
from STTService.porcupine.FAPSHotWordRecorder import FAPSHotWordRecorder

interrupted = False


def myinterrupt_callback():
    return interrupted


def signal_handler(signal, frame):
    global interrupted
    interrupted = True


if __name__ == '__main__':
    # capture SIGINT signal, e.g., Ctrl+C
    signal.signal(signal.SIGINT, signal_handler)
    # Establish communication queues
    audioOutputQueue = multiprocessing.JoinableQueue()
    audioInputQueue = audioOutputQueue

    hotwordRecorder = FAPSHotWordRecorder(audioOutputQueue, myinterrupt_callback)
    hotwordRecorder.start()

    # Establish communication queues
    sstProcess = FAPSDeepSpeechConverter(audioInputQueue, myinterrupt_callback)
    sstProcess.start()

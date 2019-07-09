import signal
import multiprocessing
from SpeechService.snowboy.modules.KeywordsDetector.FAPSKeyWordDetector import FAPSKeyWordDetector
from SpeechService.snowboy.modules import FAPSSST

interrupted = False


def myinterrupt_callback():
    global interrupted
    return interrupted


def signal_handler(signal, frame):
    global interrupted
    interrupted = True


if __name__ == '__main__':
    # capture SIGINT signal, e.g., Ctrl+C
    signal.signal(signal.SIGINT, signal_handler)

    # Establish communication queues
    audioQueue = multiprocessing.JoinableQueue()

    # Initialize the processes
    hotwordRecorder = FAPSKeyWordDetector(audioQueue, myinterrupt_callback)
    sstProcess = FAPSSST(audioQueue, myinterrupt_callback)

    # Start the processes in order
    sstProcess.start()
    hotwordRecorder.start()

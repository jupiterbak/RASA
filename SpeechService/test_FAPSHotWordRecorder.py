import multiprocessing
import signal

from SpeechService.FAPSHotWordRecorder import FAPSHotWordRecorder

USE_GOOGLE = True
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
    audioQueue = multiprocessing.JoinableQueue()
    userUtteredQueue = multiprocessing.JoinableQueue()
    botUtteredQueue = multiprocessing.JoinableQueue()

    # Hotword Decoder
    hotwordRecorder = FAPSHotWordRecorder(audioQueue, myinterrupt_callback)
    hotwordRecorder.start()


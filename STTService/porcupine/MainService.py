import multiprocessing
import signal
from pyfiglet import Figlet

from SpeechService.porcupine.FAPSDeepSpeechConverter import FAPSDeepSpeechConverter
from SpeechService.porcupine.FAPSHotWordRecorder import FAPSHotWordRecorder
from SpeechService.porcupine.FAPSTTS import FAPSTTS

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
    audioOutputQueue = multiprocessing.JoinableQueue()
    audioInputQueue = audioOutputQueue
    textOutputQueue = multiprocessing.JoinableQueue()
    textInputQueue = textOutputQueue

    f = Figlet(font='standard')
    print("###################################################\n")
    print(f.renderText('FAPS NLU'))
    print("###################################################\n")

    # TTS
    sstProcess = FAPSTTS(textInputQueue, myinterrupt_callback)
    sstProcess.start()

    # Deep Speech
    sstProcess = FAPSDeepSpeechConverter(audioInputQueue, textOutputQueue, myinterrupt_callback, use_google=USE_GOOGLE)
    sstProcess.start()

    # Hotword Decoder
    hotwordRecorder = FAPSHotWordRecorder(audioOutputQueue, myinterrupt_callback)
    hotwordRecorder.start()


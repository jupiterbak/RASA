import multiprocessing
import signal
from pyfiglet import Figlet

from SpeechService.porcupine.FAPSDeepSpeechConverter import FAPSDeepSpeechConverter
from SpeechService.porcupine.FAPSDialogEngineProxy import FAPSDialogEngineProxy
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
    audioQueue = multiprocessing.JoinableQueue()
    userUtteredQueue = multiprocessing.JoinableQueue()
    botUtteredQueue = multiprocessing.JoinableQueue()

    f = Figlet(font='standard')
    print("###################################################\n")
    print(f.renderText('FAPS NLU'))
    print("###################################################\n")

    # TTS
    TTSProcess = FAPSTTS(botUtteredQueue, myinterrupt_callback)
    TTSProcess.start()

    # Dialog Engine Proxy
    DialogProcess = FAPSDialogEngineProxy(userUtteredQueue, botUtteredQueue, myinterrupt_callback)
    DialogProcess.start()

    # Deep Speech STT
    STTProcess = FAPSDeepSpeechConverter(audioQueue, userUtteredQueue, myinterrupt_callback, use_google=USE_GOOGLE)
    STTProcess.start()

    # Hotword Decoder
    hotwordRecorder = FAPSHotWordRecorder(audioQueue, myinterrupt_callback)
    hotwordRecorder.start()


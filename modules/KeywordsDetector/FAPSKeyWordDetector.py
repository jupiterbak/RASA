import modules.KeywordsDetector.FAPSdecoder as snowboydecoder
import signal
import speech_recognition as sr
import os
import multiprocessing

interrupted = False
TOP_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_FILE = os.path.join(TOP_DIR, "resources/Tobi.pmdl")


class FAPSKeyWordDetector(multiprocessing.Process):
    def __init__(self, audio_queue, interrupt_callback=lambda: False):
        multiprocessing.Process.__init__(self)
        self.result_queue = audio_queue
        self.model = MODEL_FILE
        self.interrupt_callback = interrupt_callback

    def audioRecorderCallback(self, fname):
        print("converting audio to text")
        # self.result_queue.put(fname)

        r = sr.Recognizer()
        with sr.AudioFile(fname) as source:
            audio = r.record(source)  # read the entire audio file
        # recognize speech using Google Speech Recognition
        try:
            # for testing purposes, we're just using the default API key
            # to use another API key, use `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
            # instead of `r.recognize_google(audio)`
            print(r.recognize_google(audio))
        except sr.UnknownValueError:
            print("Google Speech Recognition could not understand audio")
        except sr.RequestError as e:
            print("Could not request results from Google Speech Recognition service; {0}".format(e))

        # os.remove(fname)

    def detectedCallback(self):
        print('recording audio...', end='', flush=True)

    def run(self):
        detector = snowboydecoder.HotwordDetector(self.model, sensitivity=0.58)
        print('Listening... Press Ctrl+C to exit')

        # main loop
        detector.start(detected_callback=self.detectedCallback,
                       audio_recorder_callback=self.audioRecorderCallback,
                       interrupt_check=self.interrupt_callback,
                       sleep_time=0.01)

        detector.terminate()
        return


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
    audioOutputQueue = multiprocessing.JoinableQueue()
    hotwordRecorder = FAPSKeyWordDetector(audioOutputQueue, myinterrupt_callback)
    hotwordRecorder.start()
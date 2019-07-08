import platform
import signal
import speech_recognition as sr
import os
import multiprocessing

from STTService.porcupine.FAPSListener import FAPSListener

interrupted = False


def _default_library_path():
    system = platform.system()
    machine = platform.machine()

    if system == 'Darwin':
        return os.path.join(os.path.dirname(__file__), './library/mac/%s/libpv_porcupine.dylib' % machine)
    elif system == 'Linux':
        if machine == 'x86_64' or machine == 'i386':
            return os.path.join(os.path.dirname(__file__), './library/linux/%s/libpv_porcupine.so' % machine)
        else:
            raise Exception('cannot autodetect the binary type. Please enter the path to the shared object using '
                            '--library_path command line argument.')
    elif system == 'Windows':
        if platform.architecture()[0] == '32bit':
            return os.path.join(os.path.dirname(__file__), '.\\library\\windows\\i686\\libpv_porcupine.dll')
        else:
            return os.path.join(os.path.dirname(__file__), '.\\library\\windows\\amd64\\libpv_porcupine.dll')
    raise NotImplementedError('Porcupine is not supported on %s/%s yet!' % (system, machine))


class FAPSHotWordRecorder(multiprocessing.Process):
    def __init__(self, audio_queue, interrupt_callback=lambda: False):
        multiprocessing.Process.__init__(self)
        self.result_queue = audio_queue
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
            txt = r.recognize_google(audio)
            print(txt)
            self.result_queue.put(txt)
        except sr.UnknownValueError:
            print("Google Speech Recognition could not understand audio")
        except sr.RequestError as e:
            print("Could not request results from Google Speech Recognition service; {0}".format(e))

        # os.remove(fname)

    def detectedCallback(self):
        print('recording audio... ', end='', flush=True)

    def run(self):
        model_file_path = "./library/common/porcupine_params.pv"
        output_path = "./output/output_audio.wav"
        keyword_file_paths = ["./ressources/keyword_files/windows/Alex_windows.ppn",
                              "./ressources/keyword_files/windows/Matthew_windows.ppn",
                              "./ressources/keyword_files/windows/Jupiter_windows.ppn",
                              "./ressources/keyword_files/windows/Florian_windows.ppn",
                              "./ressources/keyword_files/windows/Lincoln_windows.ppn",
                              "./ressources/keyword_files/windows/Tobias_windows.ppn"]
        sensitivities = [0.5] * len(keyword_file_paths)
        input_audio_device_index = 1
        show_audio_devices_info = True

        if show_audio_devices_info:
            FAPSListener.show_audio_devices_info()

        if not keyword_file_paths:
            raise ValueError('keyword file paths are missing')

        FAPSListener(
            library_path=_default_library_path(),
            model_file_path=model_file_path,
            keyword_file_paths=keyword_file_paths,
            sensitivities=sensitivities,
            output_path=output_path,
            input_device_index=input_audio_device_index,
            detected_callback=self.detectedCallback,
            audio_recorder_callback=self.audioRecorderCallback,
            interrupt_check=self.interrupt_callback).run()
        return

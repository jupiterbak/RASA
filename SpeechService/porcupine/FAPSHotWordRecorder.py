import logging
import multiprocessing
import os
import platform

from SpeechService.porcupine.FAPSListener import FAPSListener

logger = logging.getLogger("FAPSHotWordRecorder")
logger.setLevel(logging.DEBUG)
logging.basicConfig(format='[%(asctime)s][%(name)s]%(levelname)s: %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

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
        pass

    def audioRecorderCallback(self, fname):
        logger.info("converting audio to text")
        self.result_queue.put(fname)
        # os.remove(fname)

    def detectedCallback(self):
        logger.info('recording audio... ')

    def run(self):
        model_file_path = "./library/common/porcupine_params.pv"
        output_path = "./output/output_audio.wav"
        keyword_file_paths = ["./ressources/keyword_files/windows/Jupiter_windows.ppn",
                              "./ressources/keyword_files/windows/Florian_windows.ppn",
                              "./ressources/keyword_files/windows/Tobias_windows.ppn",
                              "./ressources/keyword_files/windows/demonstrator_windows.ppn"]
        # keyword_file_paths = ["./ressources/keyword_files/windows/Alex_windows.ppn",
        #                       "./ressources/keyword_files/windows/Matthew_windows.ppn",
        #                       "./ressources/keyword_files/windows/Jupiter_windows.ppn",
        #                       "./ressources/keyword_files/windows/Florian_windows.ppn",
        #                       "./ressources/keyword_files/windows/Lincoln_windows.ppn",
        #                       "./ressources/keyword_files/windows/Tobias_windows.ppn",
        #                       "./ressources/keyword_files/windows/demonstrator_windows.ppn"]
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
            interrupt_check=self.interrupt_callback,
            recording_timeout=500).run()
        return

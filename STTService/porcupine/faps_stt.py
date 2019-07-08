import collections
import os
import platform
import struct
import sys
import time
import wave
from datetime import datetime
from threading import Thread
import speech_recognition as sr

import numpy as np
import pyaudio
import soundfile

from STTService.porcupine.binding.python.porcupine import Porcupine

sys.path.append(os.path.join(os.path.dirname(__file__), '../../binding/python'))

TOP_DIR = os.path.dirname(os.path.abspath(__file__))
DETECT_DING = os.path.join(TOP_DIR, "sounds/ding.wav")
DETECT_DONG = os.path.join(TOP_DIR, "sounds/dong.wav")
DETECT_ON = os.path.join(TOP_DIR, "sounds/on.wav")
DETECT_OFF = os.path.join(TOP_DIR, "sounds/off.wav")
THRESHOLD = 500


class RingBuffer(object):
    """Ring buffer to hold audio from PortAudio"""

    def __init__(self, size=4096):
        self._buf = collections.deque(maxlen=size)

    def extend(self, data):
        """Adds data to the end of buffer"""
        self._buf.extend(data)

    def get(self):
        """Retrieves data from the beginning of buffer and clears it"""
        tmp = bytes(bytearray(self._buf))
        self._buf.clear()
        return tmp


class FAPSSTT(Thread):
    """
    Demo class for wake word detection (aka Porcupine) library. It creates an input audio stream from a microphone,
    monitors it, and upon detecting the specified wake word(s) prints the detection time and index of wake word on
    console. It optionally saves the recorded audio into a file for further review.
    """

    def __init__(
            self,
            library_path,
            model_file_path,
            keyword_file_paths,
            sensitivities,
            input_device_index=None,
            output_path=None,
            detected_callback=lambda: None,
            interrupt_check=lambda: False,
            sleep_time=0.03,
            audio_recorder_callback=None,
            silent_count_threshold=15,
            recording_timeout=100
    ):

        """
        Constructor.

        :param library_path: Absolute path to Porcupine's dynamic library.
        :param model_file_path: Absolute path to the model parameter file.
        :param keyword_file_paths: List of absolute paths to keyword files.
        :param sensitivities: Sensitivity parameter for each wake word. For more information refer to
        'include/pv_porcupine.h'. It uses the
        same sensitivity value for all keywords.
        :param input_device_index: Optional argument. If provided, audio is recorded from this input device. Otherwise,
        the default audio input device is used.
        :param output_path: If provided recorded audio will be stored in this location at the end of the run.
        :param detected_callback: Optional argument. a function or list of functions. The number of
                                  items must match the number of models in
                                  `keyword_file_paths`.
        :param interrupt_check: a function that returns True if the main loop
                                needs to stop.
        :param float sleep_time: how much time in second every loop waits.
        :param audio_recorder_callback: if specified, this will be called after
                                        a keyword has been spoken and after the
                                        phrase immediately after the keyword has
                                        been recorded. The function will be
                                        passed the name of the file where the
                                        phrase was recorded.
        :param silent_count_threshold: indicates how long silence must be heard
                                       to mark the end of a phrase that is
                                       being recorded.
        :param recording_timeout: limits the maximum length of a recording.
        """

        super(FAPSSTT, self).__init__()

        self._library_path = library_path
        self._model_file_path = model_file_path
        self._keyword_file_paths = keyword_file_paths
        self._sensitivities = sensitivities
        self._input_device_index = input_device_index
        self._output_path = output_path
        if self._output_path is not None:
            self._recorded_frames = []

        self._detected_callback = detected_callback
        tc = type(self._detected_callback)
        if tc is not list:
            self._detected_callback = [self._detected_callback]
        if len(self._detected_callback) == 1 and len(self._keyword_file_paths) > 1:
            self._detected_callback *= len(self._keyword_file_paths)
        assert len(self._keyword_file_paths) == len(self._detected_callback), \
            "Error: hotwords in your models (%d) do not match the number of " \
            "callbacks (%d)" % (len(self._keyword_file_paths), len(self._detected_callback))

        self._interrupt_check = interrupt_check
        self._sleep_time = sleep_time
        self._audio_recorder_callback = audio_recorder_callback
        self._silent_count_threshold = silent_count_threshold
        self._recording_timeout = recording_timeout

        self._running = False
        self._state = "PASSIVE"

    def play_audio_file(self, fname=DETECT_DING):
        """Simple callback function to play a wave file. By default it plays
        a Ding sounds.

        :param str fname: wave file name
        :return: None
        """
        ding_wav = wave.open(fname, 'rb')
        ding_data = ding_wav.readframes(ding_wav.getnframes())
        audio = pyaudio.PyAudio()
        stream_out = audio.open(
            format=audio.get_format_from_width(ding_wav.getsampwidth()),
            channels=ding_wav.getnchannels(),
            rate=ding_wav.getframerate(), input=False, output=True)
        stream_out.start_stream()
        stream_out.write(ding_data)
        time.sleep(0.2)
        stream_out.stop_stream()
        stream_out.close()
        audio.terminate()

    def is_silent(self, data_chunk):
        """Returns 'True' if below the 'silent' threshold"""
        return max(data_chunk) < THRESHOLD

    def run(self):
        """
         Creates an input audio stream, initializes wake word detection (Porcupine) object, and monitors the audio
         stream for occurrences of the wake word(s). It prints the time of detection for each occurrence and index of
         wake word.
         """

        num_keywords = len(self._keyword_file_paths)

        keyword_names = \
            [os.path.basename(x).replace('.ppn', '').replace('_compressed', '').split('_')[0] for x in
             self._keyword_file_paths]
        print('Listening... Press Ctrl+C to exit')
        print('listening for:')
        for keyword_name, sensitivity in zip(keyword_names, sensitivities):
            print('- %s (sensitivity: %f)' % (keyword_name, sensitivity))

        porcupine = None
        pa = None
        audio_stream = None

        try:
            porcupine = Porcupine(
                library_path=self._library_path,
                model_file_path=self._model_file_path,
                keyword_file_paths=self._keyword_file_paths,
                sensitivities=self._sensitivities)

            pa = pyaudio.PyAudio()
            audio_stream = pa.open(
                rate=porcupine.sample_rate,
                channels=1,
                format=pyaudio.paInt16,
                input=True,
                frames_per_buffer=porcupine.frame_length,
                input_device_index=self._input_device_index
            )

            self._running = True
            silent_count = 0
            recording_count = 0
            while True:
                if self._interrupt_check():
                    print("detect voice return")
                    return
                pcm = audio_stream.read(porcupine.frame_length)
                pcm = struct.unpack_from("h" * porcupine.frame_length, pcm)

                result = porcupine.process(pcm)
                # small state machine to handle recording of phrase after keyword
                if self._state == "PASSIVE":
                    if (num_keywords == 1 and result) or (num_keywords > 1 and result >= 0):  # key word found
                        if self._output_path is not None:
                            self._recorded_frames = []
                            self._recorded_frames.append(pcm)
                        silent_count = 0
                        recording_count = 0
                        self.play_audio_file(DETECT_ON)
                        if num_keywords == 1 and result:
                            print('[%s] detected keyword' % str(datetime.now()))
                        elif num_keywords > 1 and result >= 0:
                            print('[%s] detected %s' % (str(datetime.now()), keyword_names[result]))
                        callback = self._detected_callback[result]
                        if callback is not None:
                            callback()
                        if self._audio_recorder_callback is not None:
                            self._state = "ACTIVE"
                        continue
                elif self._state == "ACTIVE":
                    stop_recording = False
                    if recording_count > self._recording_timeout:
                        stop_recording = True
                    elif self.is_silent(pcm):  # silence found
                        if silent_count > self._silent_count_threshold:
                            stop_recording = True
                        else:
                            silent_count = silent_count + 1
                    else:
                        silent_count = 0

                    if stop_recording is True:
                        self.play_audio_file(DETECT_OFF)
                        fname = self.save_message(porcupine)
                        self._audio_recorder_callback(fname)
                        self._state = "PASSIVE"
                        continue
                    recording_count = recording_count + 1
                    if self._output_path is not None:
                        self._recorded_frames.append(pcm)

        except KeyboardInterrupt:
            print('stopping ...')
        finally:
            if porcupine is not None:
                porcupine.delete()

            if audio_stream is not None:
                audio_stream.close()

            if pa is not None:
                pa.terminate()

    def save_message(self, p):
        """
        Save the message stored in self.recordedData to a timestamped file.
        """
        if self._output_path is not None and len(self._recorded_frames) > 0:
            recorded_audio = np.concatenate(self._recorded_frames, axis=0).astype(np.int16)
            soundfile.write(self._output_path, recorded_audio, samplerate=p.sample_rate, subtype='PCM_16')
            return self._output_path

    _AUDIO_DEVICE_INFO_KEYS = ['index', 'name', 'defaultSampleRate', 'maxInputChannels']

    @classmethod
    def show_audio_devices_info(cls):
        """ Provides information regarding different audio devices available. """

        pa = pyaudio.PyAudio()

        for i in range(pa.get_device_count()):
            info = pa.get_device_info_by_index(i)
            print(', '.join("'%s': '%s'" % (k, str(info[k])) for k in cls._AUDIO_DEVICE_INFO_KEYS))

        pa.terminate()


def _default_library_path():
    system = platform.system()
    machine = platform.machine()

    if system == 'Darwin':
        return os.path.join(os.path.dirname(__file__), './lib/mac/%s/libpv_porcupine.dylib' % machine)
    elif system == 'Linux':
        if machine == 'x86_64' or machine == 'i386':
            return os.path.join(os.path.dirname(__file__), './lib/linux/%s/libpv_porcupine.so' % machine)
        else:
            raise Exception('cannot autodetect the binary type. Please enter the path to the shared object using '
                            '--library_path command line argument.')
    elif system == 'Windows':
        if platform.architecture()[0] == '32bit':
            return os.path.join(os.path.dirname(__file__), '.\\lib\\windows\\i686\\libpv_porcupine.dll')
        else:
            return os.path.join(os.path.dirname(__file__), '.\\lib\\windows\\amd64\\libpv_porcupine.dll')
    raise NotImplementedError('Porcupine is not supported on %s/%s yet!' % (system, machine))


def audioRecorderCallback(fname):
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


def detectedCallback():
    print('recording audio...', end='', flush=True)


if __name__ == '__main__':
    model_file_path = "./lib/common/porcupine_params.pv"
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

    # if show_audio_devices_info:
    #     PorcupineDemo.show_audio_devices_info()

    if not keyword_file_paths:
        raise ValueError('keyword file paths are missing')

    FAPSSTT(
        library_path=_default_library_path(),
        model_file_path=model_file_path,
        keyword_file_paths=keyword_file_paths,
        sensitivities=sensitivities,
        output_path=output_path,
        input_device_index=input_audio_device_index,
        detected_callback=detectedCallback,
        audio_recorder_callback=audioRecorderCallback).run()

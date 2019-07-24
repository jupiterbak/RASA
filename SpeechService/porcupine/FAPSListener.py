import collections
import os
import struct
import sys
import time
import wave
from datetime import datetime
from threading import Thread
import numpy as np
import pyaudio
import soundfile
import logging

from SpeechService.porcupine.binding.python.porcupine import Porcupine

sys.path.append(os.path.join(os.path.dirname(__file__), '../../binding/python'))

TOP_DIR = os.path.dirname(os.path.abspath(__file__))
DETECT_DING = os.path.join(TOP_DIR, "sounds/ding.wav")
DETECT_DONG = os.path.join(TOP_DIR, "sounds/dong.wav")
DETECT_ON = os.path.join(TOP_DIR, "sounds/on.wav")
DETECT_OFF = os.path.join(TOP_DIR, "sounds/off.wav")
THRESHOLD = 500

logger = logging.getLogger("FAPSListener")
logger.setLevel(logging.DEBUG)
logging.basicConfig(format='[%(asctime)s][%(name)s]%(levelname)s: %(message)s', datefmt='%Y-%m-%d %H:%M:%S')


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


class FAPSListener(Thread):
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
            recording_timeout=200
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

        super(FAPSListener, self).__init__()

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
        for keyword_name, sensitivity in zip(keyword_names, self._sensitivities):
            print('  - {}\t (sensitivity: {})'.format(keyword_name, sensitivity))
        print('\n')

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
                    logger.debug("detect program interruption... returning")
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
                            logger.info('detected keyword')
                        elif num_keywords > 1 and result >= 0:
                            logger.info('detected keyword {}'.format(keyword_names[result]))
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
            logger.debug('stopping ...')
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
        print("======================================================================================================")
        print("# Avialble Audio Devices")
        print("======================================================================================================")
        for i in range(pa.get_device_count()):
            info = pa.get_device_info_by_index(i)
            print(', '.join("'%s': '%s'" % (k, str(info[k])) for k in cls._AUDIO_DEVICE_INFO_KEYS))
        print("======================================================================================================\n")
        pa.terminate()


#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import logging
import multiprocessing
import os
import shlex
import subprocess
import sys
import time
import wave
from timeit import default_timer as timer

import numpy as np
import speech_recognition as sr
from deepspeech import Model

try:
    from shhlex import quote
except ImportError:
    from pipes import quote


# These constants control the beam search decoder
# Beam width used in the CTC decoder when building candidate transcriptions
BEAM_WIDTH = 500

# The alpha hyperparameter of the CTC decoder. Language model weight
LM_ALPHA = 0.75

# The beta hyperparameter of the CTC decoder. Word insertion bonus.
LM_BETA = 1.85

# These constants are tied to the shape of the graph used (changing them changes
# the geometry of the first layer), so make sure you use the same constants that
# were used during training

# Number of MFCC features to use
N_FEATURES = 26

# Size of the context window used for producing timesteps in the input vector
N_CONTEXT = 9

TOP_DIR = os.path.dirname(os.path.abspath(__file__))
TRIE_FILE = os.path.join(TOP_DIR, "model/deepspeech-0.6.1-models/trie")
LM_FILE = os.path.join(TOP_DIR, "model/deepspeech-0.6.1-models/lm.binary")
MODEL_FILE = os.path.join(TOP_DIR, "model/deepspeech-0.6.1-models/output_graph.pb")

logger = logging.getLogger("FAPSDeepSpeechConverter")
logger.setLevel(logging.DEBUG)
logging.basicConfig(format='[%(asctime)s][%(name)s]%(levelname)s: %(message)s', datefmt='%Y-%m-%d %H:%M:%S')


class FAPSDeepSpeechConverter(multiprocessing.Process):
    def __init__(self, audio_queue, text_queue, interrupt_callback=lambda: False, use_google= False):
        multiprocessing.Process.__init__(self)
        self.audio_queue = audio_queue
        self.text_queue = text_queue
        self.interrupt_callback = interrupt_callback
        self.use_google = use_google
        pass

    def convert_samplerate(self, audio_path):
        sox_cmd = 'sox {} --type raw --bits 16 --channels 1 --rate 16000 --encoding signed-integer --endian little ' \
                  '--compression 0.0 --no-dither - '.format(
            quote(audio_path))
        try:
            output = subprocess.check_output(shlex.split(sox_cmd), stderr=subprocess.PIPE)
        except subprocess.CalledProcessError as e:
            raise RuntimeError('SoX returned non-zero status: {}'.format(e.stderr))
        except OSError as e:
            raise OSError(e.errno, 'SoX not found, use 16kHz files or install it: {}'.format(e.strerror))

        return 16000, np.frombuffer(output, np.int16)

    def metadata_to_string(self, metadata):
        return ''.join(item.character for item in metadata.items)

    def run(self):
        # Load the model
        logger.info('Loading model from file {}'.format(MODEL_FILE))
        model_load_start = timer()
        ds = Model(MODEL_FILE, BEAM_WIDTH)
        # N_FEATURES, N_CONTEXT, ALPHABET_FILE,

        model_load_end = timer() - model_load_start
        logger.info('Loaded model in {:.3}s.'.format(model_load_end))

        # Load LM and Trie
        logger.info('Loading language model from files {} {}'.format(LM_FILE, TRIE_FILE))
        lm_load_start = timer()
        ds.enableDecoderWithLM(LM_FILE, TRIE_FILE, LM_ALPHA, LM_BETA)
        lm_load_end = timer() - lm_load_start
        logger.info('Loaded language model in {:.3}s.'.format(lm_load_end))

        # Loop waiting for the next audio to process
        while True:
            if self.interrupt_callback():
                logger.debug("detect program interruption... returning")
                return
            next_audio = self.audio_queue.get()
            if next_audio is None:
                time.sleep(0.03)
                continue
            # Open the file and Execute Deepspeech or Google (online)
            if self.use_google is True:
                r = sr.Recognizer()
                with sr.AudioFile(next_audio) as source:
                    audio = r.record(source)  # read the entire audio file
                # recognize speech using Google Speech Recognition
                try:
                    # for testing purposes, we're just using the default API key
                    # to use another API key, use `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
                    # instead of `r.recognize_google(audio)`
                    txt = r.recognize_google(audio)
                    # txt = r.recognize_sphinx(audio)
                    logger.debug("Google translation --> {}".format(txt))
                    self.text_queue.put(txt)
                except sr.UnknownValueError:
                    logger.error("Google Speech Recognition could not understand audio")
                except sr.RequestError as e:
                    logger.error("Could not request results from Google Speech Recognition service; {0}".format(e))
            else:
                fin = wave.open(next_audio, 'rb')
                fs = fin.getframerate()
                if fs != 16000:
                    logger.warning(
                        'Original sample rate ({}) is different than 16kHz. Resampling might produce erratic '
                        'speech recognition.'.format(
                            fs), file=sys.stderr)
                    fs, audio = self.convert_samplerate(next_audio)
                else:
                    audio = np.frombuffer(fin.readframes(fin.getnframes()), np.int16)
                try:
                    audio_length = fin.getnframes() * (1 / 16000)
                    fin.close()
                    logger.info('Running inference.')
                    inference_start = timer()
                    txt = ds.stt(audio)
                    logger.info('DeepSpeech decoded text --> {}'.format(txt))
                    inference_end = timer() - inference_start
                    logger.debug('Inference took %0.3fs for %0.3fs audio file.' % (inference_end, audio_length))
                    self.text_queue.put(txt)
                except sr.UnknownValueError:
                    logger.error("Deep Speech Recognition could not understand audio")

        pass


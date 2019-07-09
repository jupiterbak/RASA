#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import multiprocessing
import os
import shlex
import signal
import subprocess
import sys
import threading
import time
import wave
from timeit import default_timer as timer
from datetime import datetime

import numpy as np
from deepspeech import Model

try:
    from shhlex import quote
except ImportError:
    from pipes import quote

# These constants control the beam search decoder

# Beam width used in the CTC decoder when building candidate transcriptions
BEAM_WIDTH = 500

# The alpha hyperparameter of the CTC decoder. Language Model weight
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
ALPHABET_FILE = os.path.join(TOP_DIR, "Modeldeepspeech-0.5.1-models/alphabet.txt")
TRIE_FILE = os.path.join(TOP_DIR, "Model/deepspeech-0.5.1-models/trie")
LM_FILE = os.path.join(TOP_DIR, "Model/deepspeech-0.5.1-models/lm.binary")
MODEL_FILE = os.path.join(TOP_DIR, "Model/deepspeech-0.5.1-models/output_graph.pb")


class FAPSDeepSpeechConverter(multiprocessing.Process):
    def __init__(self, audio_queue, text_queue, interrupt_callback = lambda: False):
        multiprocessing.Process.__init__(self)
        self.audio_queue = audio_queue
        self.text_queue = text_queue
        self.interrupt_callback = interrupt_callback
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
        print('Loading model from file {}'.format(MODEL_FILE), file=sys.stderr)
        model_load_start = timer()
        ds = Model(MODEL_FILE, N_FEATURES, N_CONTEXT, ALPHABET_FILE, BEAM_WIDTH)
        model_load_end = timer() - model_load_start
        print('Loaded model in {:.3}s.'.format(model_load_end), file=sys.stderr)

        # Load LM and Trie
        print('Loading language model from files {} {}'.format(LM_FILE, TRIE_FILE), file=sys.stderr)
        lm_load_start = timer()
        ds.enableDecoderWithLM(ALPHABET_FILE, LM_FILE, TRIE_FILE, LM_ALPHA, LM_BETA)
        lm_load_end = timer() - lm_load_start
        print('Loaded language model in {:.3}s.'.format(lm_load_end), file=sys.stderr)

        # Loop waiting for the next audio to process
        while True:
            if self.interrupt_callback():
                print("detect voice return")
                return
            next_audio = self.audio_queue.get()
            if next_audio is None:
                time.sleep(0.03)
                continue
            # Open the file and Execute Deepspeech
            fin = wave.open(next_audio, 'rb')
            fs = fin.getframerate()
            if fs != 16000:
                print(
                    'Warning: original sample rate ({}) is different than 16kHz. Resampling might produce erratic '
                    'speech recognition.'.format(
                        fs), file=sys.stderr)
                fs, audio = self.convert_samplerate(next_audio)
            else:
                audio = np.frombuffer(fin.readframes(fin.getnframes()), np.int16)

            audio_length = fin.getnframes() * (1 / 16000)
            fin.close()

            print('Running inference.', file=sys.stderr)
            inference_start = timer()
            txt = ds.stt(audio, fs)
            print('[{}] DeepSpeech --> {}'.format(str(datetime.now()), txt))
            inference_end = timer() - inference_start
            print('Inference took %0.3fs for %0.3fs audio file.' % (inference_end, audio_length), file=sys.stderr)
            self.text_queue.put(txt)

        return


interrupted = False

def myinterrupt_callback():
    global interrupted
    return interrupted


def signal_handler(signal, frame):
    global interrupted
    interrupted = True


def sendIt(queue):
  queue.put("./output/output_audio.wav")
  threading.Timer(10.0, sendIt, [queue]).start()
  print("Timer Event")


if __name__ == '__main__':
    # capture SIGINT signal, e.g., Ctrl+C
    signal.signal(signal.SIGINT, signal_handler)

    # Establish communication queues
    audioInputQueue = multiprocessing.JoinableQueue()
    textOutputQueue = multiprocessing.JoinableQueue()
    sstProcess = FAPSDeepSpeechConverter(audioInputQueue, textOutputQueue, myinterrupt_callback)
    sstProcess.start()

    # Timer
    sendIt(audioInputQueue)
    print("Exit\n")


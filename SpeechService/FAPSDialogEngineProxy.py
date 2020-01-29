import logging
import multiprocessing
import signal
import threading
import time
import socketio


logger = logging.getLogger("FAPSDialogEngineProxy")
logger.setLevel(logging.DEBUG)
logging.basicConfig(format='[%(asctime)s][%(name)s]%(levelname)s: %(message)s', datefmt='%Y-%m-%d %H:%M:%S')


class FAPSDialogEngineProxy(multiprocessing.Process):
    def __init__(self, text_input_queue, text_output_queue, interrupt_callback=lambda: False):
        multiprocessing.Process.__init__(self)
        self.text_input_queue = text_input_queue
        self.text_output_queue = text_output_queue
        self.interrupt_callback = interrupt_callback
        self.connected = False
        self.session_id = "FAPS_NLU"

    def run(self):
        sio = socketio.Client()

        @sio.event
        def connect():
            logger.info('connection established')
            sio.emit('session_request', {'session_id': self.session_id})

        @sio.event
        def connect_error():
            logger.error('connection error')

        @sio.event
        def disconnect():
            logger.info('disconnected from server')

        @sio.event
        def error():
            logger.error('error')

        @sio.event
        def session_confirm(data):
            logger.debug('Session confirmed! Session_id: {}'.format(data))
            self.connected = True
            self.session_id = data

        @sio.on('bot_uttered')
        def on_bot_uttered_message(data):
            self.text_output_queue.put(data['text'])
            logger.info('Bot_uttered: {}'.format(data['text']))

        def send_user_uttered_message(txt):
            logger.info('Sending message --> {}'.format(txt))
            sio.emit('user_uttered', {'message': '{}'.format(txt), 'session_id': self.session_id})

        # Connect
        sio.connect('http://localhost:5005')

        while True:
            if self.interrupt_callback():
                logger.debug("detect program interruption... returning")
                return

            next_text = self.text_input_queue.get()
            if (next_text is None) or (self.connected is False):
                time.sleep(0.03)
                continue
            send_user_uttered_message(next_text)

        return


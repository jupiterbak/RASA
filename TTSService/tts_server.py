#!/usr/bin/env python

from flask import Flask
from flask_restful import Api, Resource, request
import pyttsx3

__author__ = "Jupiter Bakakeu"
__copyright__ = "Copyright 2019, FAPS"
__credits__ = ["Jupiter Bakakeu"]
__license__ = "GPL"
__version__ = "3.0"
__status__ = "Production"

response = "No Error"


def main(engine):
    app = Flask(__name__)
    @app.route('/speak', methods=['POST', 'GET'])
    def post():
        if request.is_json:
            contents = request.get_json()
            for content in contents:
                engine.startLoop(False)
                engine.say("I will speak this text", 'text')
                print(content["text"])
                engine.iterate()
                return response, 200
        else:
            return response, 404

    api = Api(app)
    app.run(host="0.0.0.0", port='9001', debug=True)


if __name__ == "__main__":
    engine = pyttsx3.init()

    def onEnd(name, completed):
        if completed is True:
            engine.endLoop()
    engine.connect('finished-utterance', onEnd)
    main(engine)



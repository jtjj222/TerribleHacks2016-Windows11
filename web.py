#!/usr/bin/python3

from multiprocessing import Process, Queue
from flask import Flask, jsonify, abort, request, make_response, url_for
app = Flask(__name__, static_url_path = "")


@app.route('/say', methods = ['POST'])
def say_http():
    if not request.json or not 'text' in request.json:
        abort(400)
    say(request.json['text'])

    return jsonify({'Good':'Good!'}), 201


def _say_process(msg):
    import pyttsx
    tts = pyttsx.init()
    tts.setProperty('rate', 150)
    tts.say(msg)
    tts.runAndWait()

def say(msg):
    p = Process(target=_say_process, args=(msg,))
    p.start()
    p.join()


if __name__ == '__main__':
    app.run(debug = True)
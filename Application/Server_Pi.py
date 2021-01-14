from flask import Flask, request
from flask_restplus import Api, Resource, fields
from werkzeug.contrib.fixers import ProxyFix

import RPi.GPIO as GPIO

app = Flask(__name__)
app.wsgi_app = ProxyFix(app.wsgi_app)
api = Api(app, version='1.0', title='Taurus API', description='First Taurus API')

ha = api.namespace('HomeAutomation', description = 'Methods to control the house.')

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
led = 17
ledsts = 0
GPIO.setup(led, GPIO.OUT)
GPIO.output(led, GPIO.LOW)


@ha.route('/turnledon', methods=['GET'])
class TurnLedOn(Resource):
    @ha.doc('Turn led on.')
    def get(self):
        GPIO.output(led, GPIO.HIGH)
        return {"Message": "Turned on."}, 200


@ha.route('/turnledoff', methods=['GET'])
class TurnLedOff(Resource):
    @ha.doc('Turn led off.')
    def get(self):
        GPIO.output(led, GPIO.LOW)
        return {"Message": "Turned off."}, 200


if __name__ == '__main__':
    app.run(host='0.0.0.0')

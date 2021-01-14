from flask import Flask, request
from flask_restplus import Api, Resource, fields
from werkzeug.contrib.fixers import ProxyFix

from gpiozero import LED

app = Flask(__name__)
app.wsgi_app = ProxyFix(app.wsgi_app)
api = Api(app, version='1.0', title='Taurus API', description='First Taurus API')

ha = api.namespace('HomeAutomation', description = 'Methods to control the house.')


@ha.route('/turnledon', methods=['GET'])
class TurnLedOn(Resource):
    @ha.doc('Turn led on.')
    def get(self):
        led = LED(17)
        led.on()


@ha.route('/turnledoff', methods=['GET'])
class TurnLedOff(Resource):
    @ha.doc('Turn led off.')
    def get(self):
        led = LED(17)
        led.off()


if __name__ == '__main__':
    app.run(host='0.0.0.0')

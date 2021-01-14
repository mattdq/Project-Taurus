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
    led = LED(17)
    led.on()


@ha.route('/turnledoff', methods=['GET'])
class TurnLedOff(Resource):
    led = LED(17)
    led.off()


if __name__ == '__main__':
    app.run(debug=True)

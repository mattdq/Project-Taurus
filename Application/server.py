from flask import Flask, request
from flask_restplus import Api, Resource, fields
from werkzeug.contrib.fixers import ProxyFix
import mysql.connector
import datetime

import RPi.GPIO as GPIO

app = Flask(__name__)
app.wsgi_app = ProxyFix(app.wsgi_app)
api = Api(app, version='1.0', title='Taurus API', description='First Taurus API')

cr = api.namespace('Create', description='Methods to insert into the database.')
ct = api.namespace('Consult', description='Methods to consult the database.')
ha = api.namespace('HomeAutomation', description='Methods to control the house.')

User = api.model('User', {
    'usr_name': fields.String(required=True, description='Name of the user.'),
    'usr_pwd': fields.String(required=True, description='Password of the user.'),
    'usr_email': fields.String(required=True, description='E-mail of the user.'),
    'usr_birth': fields.Date(required=True, description='Birthdate of the user.'),
    'usr_address': fields.String(required=True, description='Address of the user.'),
    'usr_cpf': fields.String(required=True, description='CPF of the user.')})

Account = api.model('Account', {
    'usr_pwd': fields.String(required=True, description='Password of the user.'),
    'usr_name': fields.String(required=True, description='Name of the user.'),
    'acc_alias': fields.String(required=True, description='Name of the account.')})

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)


class TaurusDB(object):

    def __init__(self):
        self.Taurus = mysql.connector.connect(
            host="localhost",
            user="matt",
            password='MattDq1!123',
            database="Taurus"
        )
        self.Taurus.autocommit = True
        self.cursor = self.Taurus.cursor()

    def __del__(self):
        self.Taurus.close()

    def createuser(self, data):
        try:
            self.cursor.execute(f"""insert into Taurus.users(`usr_name`, `usr_birth`, `usr_cpf`, `usr_email`, 
                    `usr_pwd`, `usr_credate`, `usr_id`,`usr_address`) values('{data['usr_name']}',
                    '{data['usr_birth']}','{data['usr_cpf']}','{data['usr_email']}','{data['usr_pwd']}',
                    '{datetime.datetime.now().strftime('%Y-%m-%d')}', uuid(), '{data['usr_address']}')""")
        except mysql.connector.errors.IntegrityError:
            return dict(MESSAGE='Some of the information is already taken.'), 400
        except:
            return 500
        return 201

    def getuserid(self, data):
        try:
            self.cursor.execute(
                f"""select usr_id from Taurus.users where usr_name = '{data['usr_name']}' and usr_pwd = '{data['usr_pwd']}'""")
            answer = self.cursor.fetchall()[0]
            return dict(usr_id=answer[0]), 200
        except:
            return 500

    def getaccountid(self, data):
        try:
            self.cursor.execute(
                f"""select a.acc_id from Taurus.accounts as a inner join Taurus.users as u on u.usr_id = a.usr_id where usr_name = '{data['usr_name']}' and usr_pwd = '{data['usr_pwd']}' and acc_alias = '{data['acc_alias']}'""")
            answer = self.cursor.fetchall()[0]
            return dict(acc_id=answer[0]), 200
        except:
            return 500

    def createaccount(self, data):
        try:
            usr_id = self.getuserid(data)[0]['usr_id']
            self.cursor.execute(
                f"""insert into Taurus.accounts(`usr_id`, `acc_credate`, `acc_alias`, `acc_id`) values('{usr_id}', '{datetime.datetime.now().strftime('%Y-%m-%d')}','{data['acc_alias']}', uuid())""")
        except mysql.connector.errors.IntegrityError:
            return dict(MESSAGE='This user already have an account by that alias.'), 400
        except:
            return 500
        return 201

    def createtransaction(self, data):
        try:
            acc_id = self.getaccountid(data)[0]['acc_id']
            self.cursor.execute(
                f"""insert into Taurus.transactions(`tra_tag`, `tra_date`, `acc_id`, `tra_value`, `tra_id`) values('{data['tra_tag']}', '{datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}', '{acc_id}', {data['tra_value']}, uuid())""")
        except:
            return 500
        return 201

    def getbalance(self, data):
        try:
            acc_id = self.getaccountid(data)[0]['acc_id']
            self.cursor.execute(
                f"""select DATE_FORMAT(tra_date,'%Y-%m-%d'), acc_bal from Taurus.balance where acc_id = '{acc_id}'""")
            answer = self.cursor.fetchall()
            answer = dict((each[0], float(each[1])) for each in answer)
            return dict(answer), 200
        except:
            return 500

    def gettransactions(self, data):
        try:
            self.cursor.execute(
                f"""select DATE_FORMAT(tra_date,'%Y-%m-%d'), t.tra_tag, tra_value, tra_id from Taurus.transactions as t inner join (select a.acc_id from Taurus.accounts as a inner join Taurus.users as u on u.usr_id = a.usr_id where usr_name = '{data['usr_name']}' and usr_pwd = '{data['usr_pwd']}' and acc_alias = '{data['acc_alias']}') as j on j.acc_id = t.acc_id""")
            answer = self.cursor.fetchall()
            answer = dict((each[3], (each[1], float(each[2]), each[0])) for each in answer)
            return dict(answer), 200
        except:
            return 500


Taurus = TaurusDB()


@cr.route('/user')
class CreateUserAPI(Resource):
    @cr.doc('Create user.')
    @cr.expect(User)
    def post(self):
        return Taurus.createuser(api.payload)


@cr.route('/account')
class CreateAccountAPI(Resource):
    @cr.doc('Create Account.')
    @cr.expect(Account)
    def post(self):
        return Taurus.createaccount(api.payload)


@cr.route('/transaction')
class CreateAccountAPI(Resource):
    @cr.doc('Create Account.')
    @cr.expect(Account)
    def post(self):
        return Taurus.createtransaction(api.payload)


@ct.route('/userid', methods=['GET'])
class GetUserId(Resource):
    @ct.doc('Get user id.')
    def get(self):
        data = request.args.to_dict()
        return Taurus.getuserid(data)


@ct.route('/accountid', methods=['GET'])
class GetUserId(Resource):
    @ct.doc('Get account id.')
    def get(self):
        data = request.args.to_dict()
        return Taurus.getaccountid(data)


@ct.route('/balance', methods=['GET'])
class GetUserId(Resource):
    @ct.doc('Get account balance.')
    def get(self):
        data = request.args.to_dict()
        return Taurus.getbalance(data)


@ct.route('/transactions', methods=['GET'])
class GetUserId(Resource):
    @ct.doc('Get transaction data.')
    def get(self):
        data = request.args.to_dict()
        return Taurus.gettransactions(data)


@ha.route('/turnledon', methods=['GET'])
class TurnLedOn(Resource):
    @ha.doc('Turn led on.')
    def get(self):
        GPIO.output(17, GPIO.HIGH)
        return {"Message": "Turned on."}, 200


@ha.route('/turnledoff', methods=['GET'])
class TurnLedOff(Resource):
    @ha.doc('Turn led off.')
    def get(self):
        GPIO.output(17, GPIO.LOW)
        return {"Messae": "Turned off."}, 200


@ha.route('/led', methods=['GET'])
class TurnLedOff(Resource):
    @ha.doc('Change led.')
    def get(self):
        pin = int(request.args.get('pin'))
        mode = str(request.args.get('mode'))
        if mode == 'HIGH':
            GPIO.setup(pin, GPIO.OUT)
            GPIO.output(pin, GPIO.HIGH)
            return {"Message": "Turned on."}, 200
        elif mode == 'LOW':
            GPIO.setup(pin, GPIO.OUT)
            GPIO.output(pin, GPIO.LOW)
            return {"Message": "Turned off."}, 200
        else:
            return {"Message": "Wrong input."}, 400


if __name__ == '__main__':
    app.run(host='0.0.0.0')

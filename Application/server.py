from flask import Flask, request
from flask_jsonpify import jsonify
from flask_restful import Resource, Api, reqparse
from json import dumps
from sqlalchemy import create_engine
import datetime
import mysql.connector
import json

app = Flask(__name__)
api = Api(app)


class createUser(Resource):
    def post(self):
        args = json.loads(request.data)

        database = mysql.connector.connect(
            host="localhost",
            user="root",
            password="123456789",
            database="taurus"
        )

        if database.is_connected():
            if len(args) == 5:
                database.autocommit = True
                cursor = database.cursor()
                try:
                    cursor.execute(f"""insert into taurus.users(`username`, `birth`, `cpf/cnpj`, `email`, `password`, `creationdate`) values('{args['username']}','{args['birth']}','{args['cpf/cnpj']}','{args['email']}','{args['password']}','{datetime.datetime.now().strftime('%Y-%m-%d')}')""")
                except mysql.connector.errors.IntegrityError:
                    return dict(MESSAGE='Some of the information is already taken: CPF/CNPJ, username, email'), 400
                cursor.execute(f"""select userid from taurus.users where username = '{args['username']}'""")
                answer = cursor.fetchall()[0]
                return dict(USERID=answer[0]), 200
        else:
            return 500


class createAccount(Resource):

    def post(self):

        args = json.loads(request.data)

        database = mysql.connector.connect(
            host="localhost",
            user="root",
            password="123456789",
            database="taurus"
        )

        if database.is_connected():
            if len(args) == 2:
                database.autocommit = True
                cursor = database.cursor()
                try:
                    cursor.execute(f"""insert into taurus.usersaccounts(`userid`, `creationdate`, `accountalias`) values('{args['userid']}', '{datetime.datetime.now().strftime('%Y-%m-%d')}','{args['accountalias']}')""")
                except mysql.connector.errors.IntegrityError:
                    return dict(MESSAGE='This user already have an account by that alias.'), 400
                cursor.execute(f"""select accountid from taurus.usersaccounts where userid = '{args['userid']}' and accountalias = '{args['accountalias']}'""")
                answer = cursor.fetchall()[0]
                return dict(ACCOUNTID=answer[0]), 200
        else:
            return 500


# todo add a way for the transaction to be found (currently we only have date, account and value so
# if someone buy 2 different stuff costing 50 bucks it may error.
class addTransaction(Resource):
    def post(self):

        args = json.loads(request.data)

        database = mysql.connector.connect(
            host="localhost",
            user="root",
            password="123456789",
            database="taurus"
        )

        if database.is_connected():
            if len(args) == 3:
                database.autocommit = True
                cursor = database.cursor()
                cursor.execute(f"""insert into taurus.acc_transactions(`transactiontag`, `transactiondate`, `accountid`, `transactionvalue`) values('{args['transactiontag']}', '{datetime.datetime.now().strftime('%Y-%m-%d')}', '{args['accountid']}', '{args['transactionvalue']}')""")
                cursor.execute(f"""select transactionid from taurus.acc_transactions where accountid = '{args['accountid']}' and transactionvalue = '{args['transactionvalue']}' and transactiontag = '{args['transactiontag']}' and transactiondate = '{datetime.datetime.now().strftime('%Y-%m-%d')}'""")
                answer = cursor.fetchall()[0]
                return dict(TRANSACTIONID=answer[0]), 200
        else:
            return 500


api.add_resource(createUser, '/createuser')
api.add_resource(createAccount, '/createaccount')
api.add_resource(addTransaction, '/addtransaction')

if __name__ == '__main__':
    app.run(port=1996)

from flask import Flask, request
from flask_restful import Resource, Api
import datetime
from Application.db import DB
import mysql.connector
import json

app = Flask(__name__)
api = Api(app)


class CreateUser(Resource):

    @staticmethod
    def post():
        args = json.loads(request.data)

        taurus = DB()

        database = taurus.Taurus

        if database.is_connected():
            if len(args) == 6:
                database.autocommit = True
                cursor = database.cursor()
                try:
                    cursor.execute(f"""insert into taurus.users(`usr_name`, `usr_birth`, `usr_cpf`, `usr_email`, 
                    `usr_pwd`, `usr_credate`, `usr_id`,`usr_address`) values('{args['usr_name']}',
                    '{args['usr_birth']}','{args['usr_cpf']}','{args['usr_email']}','{args['usr_pwd']}',
                    '{datetime.datetime.now().strftime('%Y-%m-%d')}', uuid(), '{args['usr_address']}')""")
                except mysql.connector.errors.IntegrityError:
                    return dict(MESSAGE='Some of the information is already taken.'), 400
                cursor.execute(f"""select usr_id from taurus.users where usr_name = '{args['usr_name']}'""")
                answer = cursor.fetchall()[0]
                return dict(USERID=answer[0]), 200
        else:
            return 500


class GetUserId(Resource):

    @staticmethod
    def post():
        args = json.loads(request.data)

        taurus = DB()

        database = taurus.Taurus

        if database.is_connected():
            if len(args) == 1:
                database.autocommit = True
                cursor = database.cursor()
                try:
                    cursor.execute(f"""select usr_id from Taurus.users where usr_name = '{args['usr_name']}'""")
                    answer = cursor.fetchall()[0]
                    return dict(USERID=answer[0]), 200
                except:
                    return 500
        else:
            return 500


class GetUserData(Resource):

    @staticmethod
    def post():
        args = json.loads(request.data)

        taurus = DB()

        database = taurus.Taurus

        if database.is_connected():
            if len(args) == 2:
                database.autocommit = True
                cursor = database.cursor()
                try:
                    cursor.execute(f"""select usr_name, usr_birth, usr_email, usr_cpf, usr_credate, usr_address from Taurus.users where usr_name = '{args['usr_name']}' and usr_pwd = '{args['usr_pwd']}'""")
                    answer = cursor.fetchall()[0]
                    return dict(USERID=answer[0]), 200
                except:
                    return 500
        else:
            return 500


class CreateAccount(Resource):

    @staticmethod
    def post():

        args = json.loads(request.data)

        taurus = DB()

        database = taurus.Taurus

        if database.is_connected():
            if len(args) == 2:
                database.autocommit = True
                cursor = database.cursor()
                try:
                    cursor.execute(
                        f"""insert into Taurus.accounts(`usr_id`, `acc_credate`, `acc_alias`, `acc_id`) values('{args['usr_id']}', '{datetime.datetime.now().strftime('%Y-%m-%d')}','{args['acc_alias']}', uuid())""")
                except mysql.connector.errors.IntegrityError:
                    return dict(MESSAGE='This user already have an account by that alias.'), 400
                cursor.execute(
                    f"""select acc_id from Taurus.accounts where usr_id = '{args['usr_id']}' and acc_alias = '{args['acc_alias']}'""")
                answer = cursor.fetchall()[0]
                return dict(ACCOUNTID=answer[0]), 200
        else:
            return 500


class GetAccountId(Resource):

    @staticmethod
    def post():

        args = json.loads(request.data)

        taurus = DB()

        database = taurus.Taurus

        if database.is_connected():
            if len(args) == 2:
                database.autocommit = True
                cursor = database.cursor()
                try:
                    cursor.execute(f"""select acc_id from Taurus.accounts where usr_id = '{args['usr_id']}' and acc_alias = '{args['acc_alias']}'""")
                    answer = cursor.fetchall()[0]
                    return dict(ACCOUNTID=answer[0]), 200
                except mysql.connector.errors.IntegrityError:
                    return 500
        else:
            return 500


class GetAccountData(Resource):

    @staticmethod
    def post():

        args = json.loads(request.data)

        taurus = DB()

        database = taurus.Taurus

        if database.is_connected():
            if len(args) == 2:
                database.autocommit = True
                cursor = database.cursor()
                try:
                    cursor.execute(f"""select usr_id, acc_alias, acc_credate from Taurus.accounts where usr_id = '{args['usr_id']}' and acc_alias = '{args['acc_alias']}'""")
                    answer = cursor.fetchall()[0]
                    return dict(ACCOUNTID=answer[0]), 200
                except mysql.connector.errors.IntegrityError:
                    return 500
        else:
            return 500


class GetAccountBalance(Resource):

    @staticmethod
    def post():

        args = json.loads(request.data)

        taurus = DB()

        database = taurus.Taurus

        if database.is_connected():
            if len(args) == 1:
                database.autocommit = True
                cursor = database.cursor()
                try:
                    cursor.execute(f"""select tra_date, acc_bal from Taurus.balance where acc_id = '{args['acc_id']}'""")
                    answer = {}
                    ansdict = dict(cursor.fetchall())
                    for key, value in ansdict.items():
                        answer[key.strftime("%Y-%m-%d")] = float(value)
                    return dict(answer), 200
                except mysql.connector.errors.IntegrityError:
                    return 500
        else:
            return 500


class GetAccountTransactions(Resource):

    @staticmethod
    def post():

        args = json.loads(request.data)

        taurus = DB()

        database = taurus.Taurus

        if database.is_connected():
            if len(args) == 1:
                database.autocommit = True
                cursor = database.cursor()
                try:
                    cursor.execute(f"""select tra_tag, tra_date, tra_value, tra_id from Taurus.transactions where acc_id = '{args['acc_id']}'""")
                    answer = {}
                    ansdict = cursor.fetchall()
                    ansdict = dict((each[0], each[1:]) for each in ansdict)
                    for key, value in ansdict.items():
                        answer[key] = [value[0].strftime("%Y-%m-%d"), float(value[1]), value[2]]
                    return dict(answer), 200
                except mysql.connector.errors.IntegrityError:
                    return 500
        else:
            return 500


class AddTransaction(Resource):

    @staticmethod
    def post():

        args = json.loads(request.data)

        taurus = DB()

        database = taurus.Taurus

        if database.is_connected():
            if len(args) == 3:
                database.autocommit = True
                cursor = database.cursor()
                time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                cursor.execute(
                    f"""insert into Taurus.transactions(`tra_tag`, `tra_date`, `acc_id`, `tra_value`, `tra_id`) values('{args['tra_tag']}', '{time}', '{args['acc_id']}', {args['tra_value']}, uuid())""")
                cursor.execute(
                    f"""select tra_id from Taurus.transactions where acc_id = '{args['acc_id']}' and tra_value = {args['tra_value']} and tra_tag = '{args['tra_tag']}' and tra_date = '{time}'""")
                answer = cursor.fetchall()[0]
                return dict(TRANSACTIONID=answer[0]), 200
        else:
            return 500


class GetTransactionData(Resource):

    @staticmethod
    def post():

        args = json.loads(request.data)

        taurus = DB()

        database = taurus.Taurus

        if database.is_connected():
            if len(args) == 1:
                database.autocommit = True
                cursor = database.cursor()
                cursor.execute(
                    f"""select tra_tag, tra_date, tra_value, acc_id from Taurus.transactions where tra_id = '{args['tra_id']}'""")
                answer = cursor.fetchall()[0]
                return dict(TRANSACTIONID=answer[0]), 200
        else:
            return 500


api.add_resource(CreateUser, '/createuser')
api.add_resource(GetUserId, '/getuserid')
api.add_resource(GetUserData, '/getuserid')

api.add_resource(CreateAccount, '/createaccount')
api.add_resource(GetAccountId, '/getaccountid')
api.add_resource(GetAccountData, '/getaccountid')
api.add_resource(GetAccountBalance, '/getaccountbalance')
api.add_resource(GetAccountTransactions, '/getaccounttransactions')

api.add_resource(AddTransaction, '/addtransaction')
api.add_resource(GetTransactionData, '/getaccountid')

if __name__ == '__main__':
    app.run(port=1996)

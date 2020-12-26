from flask import Flask, request
from flask_restful import Resource, Api, reqparse
from sqlalchemy import create_engine
from json import dumps
from flask_jsonpify import jsonify
import mysql.connector

app = Flask(__name__)
api = Api(app)


class Products(Resource):
    def get(self):
        database = mysql.connector.connect(
            host="localhost",
            user="root",
            password="123456789",
            database="sucos_vendas"
        )
        if database.is_connected():
            database.autocommit = True
            cursor = database.cursor()
            cursor.execute("SELECT CODIGO_DO_PRODUTO FROM tabela_de_produtos")
            resposta = cursor.fetchall()
            return {'produtos': [i[0] for i in resposta]}, 200
        else:
            return None

    def post(self):

        parser = reqparse.RequestParser()  # initialize

        parser.add_argument('prodcode')
        parser.add_argument('prodname')
        parser.add_argument('prodpack')
        parser.add_argument('prodsize')

        args = parser.parse_args()

        database = mysql.connector.connect(
            host="localhost",
            user="root",
            password="123456789",
            database="sucos_vendas"
        )

        if database.is_connected():
            if args['prodcode'] is not None:
                database.autocommit = True
                cursor = database.cursor()
                cursor.execute(f"SELECT * FROM TABELA_DE_PRODUTOS where CODIGO_DO_PRODUTO = {args['prodcode']}")
                resposta = cursor.fetchall()[0]
                return dict(CODIGO_DO_PRODUTO=resposta[0],
                            NOME_DO_PRODUTO=resposta[1],
                            EMBALAGEM=resposta[2],
                            TAMANHO=resposta[3],
                            SABOR=resposta[4],
                            PRECO_DE_LISTA=resposta[5]), 200
        else:
            return None


api.add_resource(Products, '/products')

if __name__ == '__main__':
    app.run(port=5996)

import mysql.connector


class DB:
    def __init__(self):
        self.Taurus = mysql.connector.connect(
            host="localhost",
            user="matt",
            password='Test!1234',
            database="Taurus"
        )

    def __del__(self):
        self.Taurus.close()

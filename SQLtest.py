import mysql.connector
from mysql.connector import Error




class SQL:
    def __init__(self, host_name, user_name, user_password):
        self.connection = None
        try:
            self.connection = mysql.connector.connect(
                host=host_name,
                user=user_name,
                passwd=user_password,
            )
            print("Connection to MySQL DB successful")
        except Error as e:
            print(f"The error '{e}' occurred")

    def get_game_text(self):
        query = "SELECT game FROM discord.settings"
        with self.connection.cursor() as cursor:
            cursor.execute(query)
            for row in cursor.fetchall():
                return row[0]




connection = SQL("26.8.182.214", "Bot", "Bot_Python")

print(connection.get_game_text())
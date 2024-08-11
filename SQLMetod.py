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

    def UpdataBD(self):
        self.connection = None
        try:
            self.connection = mysql.connector.connect(
                host='localhost',
                user="Bot",
                passwd="Bot_Python",
            )
        except Error as e:
            print(e)

    def add_Admin(self, id_admin, lvl):
        query = f"INSERT INTO discord.admin_list (idadmin_list,lvl_admin) VALUES ('{id_admin}','{lvl}')"
        with self.connection.cursor() as cursor:
            cursor.execute(query)
            self.connection.commit()

    def get_admin_list(self):
        admin_list = []
        query = f'SELECT * FROM discord.admin_list'
        with self.connection.cursor() as cursor:
            cursor.execute(query)
            for row in cursor.fetchall():
                admin_list.append(int(row[0]))
            return admin_list

    def delete_admin(self, admin):
        query = f"DELETE FROM discord.admin_list WHERE (idadmin_list = '{admin}')"
        with self.connection.cursor() as cursor:
            cursor.execute(query)
            self.connection.commit()

    def get_game_text(self):
        query = "SELECT game FROM discord.settings"
        with self.connection.cursor() as cursor:
            cursor.execute(query)
            for row in cursor.fetchall():
                return row[0]

    def set_game_text(self, text, who):
        query = f"UPDATE discord.settings SET game = '{text}', whoset = '{who}' WHERE idsettings = 1"
        with self.connection.cursor() as cursor:
            cursor.execute(query)
            self.connection.commit()

    def who_set(self):
        query = "SELECT whoset FROM discord.settings"
        with self.connection.cursor() as cursor:
            cursor.execute(query)
            for row in cursor.fetchall():
                return row[0]

    def get_ping_list(self):
        ping_list = []
        query = "SELECT * FROM discord.ping_list"
        with self.connection.cursor() as cursor:
            cursor.execute(query)
            for row in cursor.fetchall():
                ping_list.append(int(row[0]))
            return ping_list

    def add_ping_list(self, people, important):
        query = f"INSERT INTO discord.ping_list (people,important) VALUES ('{people}','{important}')"
        with self.connection.cursor() as cursor:
            cursor.execute(query)
            self.connection.commit()

    def del_ping_list(self, people):
        query = f"DELETE FROM discord.ping_list WHERE (people = '{people}')"
        with self.connection.cursor() as cursor:
            cursor.execute(query)
            self.connection.commit()

    def get_quest_word(self, word):
        query = f"SELECT word_answer,id_word FROM discord.word_quest WHERE word_quest = '{word}'"
        with self.connection.cursor() as cursor:
            cursor.execute(query)
            for row in cursor.fetchall():
                return [row[0], row[1]]

    def add_query_quest_word(self, word, id_who):
        query = f"INSERT INTO discord.word_quest (word_quest,id_word) VALUES ('{word}','{id_who}')"
        with self.connection.cursor() as cursor:
            cursor.execute(query)
            self.connection.commit()

    def get_list_quest_word(self):
        word_answer = {}
        query = f"SELECT * FROM discord.word_quest"
        with self.connection.cursor() as cursor:
            cursor.execute(query)
            for row in cursor.fetchall():
                word_answer.update({row[0]: row[1]})
            return word_answer

    def answer_quest_word(self, word, answer):
        query = f"UPDATE discord.word_quest SET word_answer = '{answer}' WHERE word_quest = '{word}'"
        with self.connection.cursor() as cursor:
            cursor.execute(query)
            self.connection.commit()

    def delete_quest(self, word):
        query = f"DELETE FROM discord.word_quest WHERE (word_quest = '{word}')"
        with self.connection.cursor() as cursor:
            cursor.execute(query)
            self.connection.commit()

    def get_who_word(self, word):
        query = f"SELECT id_word FROM discord.word_quest WHERE (word_quest = '{word}')"
        with self.connection.cursor() as cursor:
            cursor.execute(query)
            for row in cursor.fetchall():
                return row[0]

    def armagedon_start(self, time):
        query = f"UPDATE discord.armagedon SET Start = '1', timeStart = '{time}'"
        with self.connection.cursor() as cursor:
            cursor.execute(query)
            self.connection.commit()

    def get_time_armagedon(self):
        query = f"SELECT timeStart FROM discord.armagedon"
        with self.connection.cursor() as cursor:
            cursor.execute(query)
            for row in cursor.fetchall():
                time = row[0]
            return time

    def is_armagedon(self):
        query = f"SELECT Start FROM discord.armagedon"
        with self.connection.cursor() as cursor:
            cursor.execute(query)
            for row in cursor.fetchall():
                start = row[0]
            if start == 0:
                return False
            elif start == 1:
                return True

    def armagedon_end(self):
        query = f"UPDATE discord.armagedon SET End = '1'"
        with self.connection.cursor() as cursor:
            cursor.execute(query)
            self.connection.commit()

    def is_armagedon_end(self):
        query = f"SELECT End FROM discord.armagedon"
        with self.connection.cursor() as cursor:
            cursor.execute(query)
            for row in cursor.fetchall():
                end = row[0]
            if end == 0:
                return False
            elif end == 1:
                return True

    def ban_user(self, user_id: int, time):
        query = f"INSERT INTO discord.ban_list (user_id,ban_time) VALUES ('{user_id}','{time}')"
        with self.connection.cursor() as cursor:
            cursor.execute(query)
            self.connection.commit()

    def unban_user(self, user_id: int):
        query = f"DELETE FROM discord.ban_list WHERE (user_id = '{user_id}')"
        with self.connection.cursor() as cursor:
            cursor.execute(query)
            self.connection.commit()

    def get_ban_list_time(self):
        ban_list = {}
        query = f'SELECT * FROM discord.ban_list'
        with self.connection.cursor() as cursor:
            cursor.execute(query)
            for row in cursor.fetchall():
                ban_list.update({int(row[0]): int(row[1])})
            return ban_list

    def get_ban_list(self):
        ban_list = []
        query = f'SELECT * FROM discord.ban_list'
        with self.connection.cursor() as cursor:
            cursor.execute(query)
            for row in cursor.fetchall():
                ban_list.append(int(row[0]))
            return ban_list

    def add_ping_note(self, time, people, note):
        query = f"INSERT INTO discord.ping_note (people,ping_time,ping_note) VALUES ('{people}','{time}','{note}')"
        with self.connection.cursor() as cursor:
            cursor.execute(query)
            self.connection.commit()

    def get_ping_note(self):
        ping_note = []
        query = f'SELECT * FROM discord.ping_note'
        with self.connection.cursor() as cursor:
            cursor.execute(query)
            for row in cursor.fetchall():
                ping_note.append(row)
            return ping_note

    def delete_ping_note(self, time):
        query = f"DELETE FROM discord.ping_note WHERE (ping_time = '{time}')"
        with self.connection.cursor() as cursor:
            cursor.execute(query)
            self.connection.commit()

    def get_target_search_list(self):
        target_list = []
        query = f"SELECT * FROM discord.search_target"
        with self.connection.cursor() as cursor:
            cursor.execute(query)
            for row in cursor.fetchall():
                target_list.append(str(row[0]))
            return target_list

    def get_target_search(self, uid):
        query = f"SELECT * FROM discord.search_target WHERE idsearch_target = '{uid}'"
        with self.connection.cursor() as cursor:
            cursor.execute(query)
            return cursor.fetchone()

    def remove_target_search(self, uid):
        query = f"DELETE FROM discord.search_target WHERE idsearch_target = '{uid}'"
        with self.connection.cursor() as cursor:
            cursor.execute(query)
            self.connection.commit()

    def add_target_search(self, uid):
        query = f"INSERT INTO discord.search_target VALUES ('{uid}')"
        with self.connection.cursor() as cursor:
            cursor.execute(query)
            self.connection.commit()

    def terapiya_add(self):
        query = f"SELECT * FROM discord.terapiya"
        with self.connection.cursor() as cursor:
            cursor.execute(query)
            number = int(cursor.fetchone()[0])
        query = f"UPDATE discord.terapiya SET idterapiya = '{number+1}'"
        with self.connection.cursor() as cursor:
            cursor.execute(query)
            self.connection.commit()

    def terapiya_clear(self):
        query = f"UPDATE discord.terapiya SET idterapiya = '1'"
        with self.connection.cursor() as cursor:
            cursor.execute(query)
            self.connection.commit()

    def terapiya_get(self):
        query = f"SELECT * FROM discord.terapiya"
        with self.connection.cursor() as cursor:
            cursor.execute(query)
            return int(cursor.fetchone()[0])

    def churka_mode_get(self):
        query = f"SELECT * FROM discord.churka_mode"
        with self.connection.cursor() as cursor:
            cursor.execute(query)
            return int(cursor.fetchone()[0])

    def churka_mode_set(self, mode: int):
        query = f"UPDATE discord.churka_mode SET idchurka_mode = '{mode}'"
        with self.connection.cursor() as cursor:
            cursor.execute(query)
            self.connection.commit()


    def ban_gpt(self, user_id: int):
        query = f"INSERT INTO discord.gpt_ban (idgpt_ban) VALUES ('{user_id}')"
        with self.connection.cursor() as cursor:
            cursor.execute(query)
            self.connection.commit()

    def unban_gpt(self, user_id: int):
        query = f"DELETE FROM discord.gpt_ban WHERE (idgpt_ban = '{user_id}')"
        with self.connection.cursor() as cursor:
            cursor.execute(query)
            self.connection.commit()

    def get_gtp_ban_list(self):
        ban_list = []
        query = f'SELECT * FROM discord.gpt_ban'
        with self.connection.cursor() as cursor:
            cursor.execute(query)
            for row in cursor.fetchall():
                ban_list.append(int(row[0]))
            return ban_list

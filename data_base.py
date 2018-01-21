import os
from urllib import parse
import psycopg2
import SQLQueries


class DataBaseConnect:
    def __init__(self):
        self.parse_object = parse.uses_netloc.append("postgres")
        # DATABASE_URL --> переменная окружения
        # в которой данные от базы данных
        self.url = parse.urlparse(os.environ["DATABASE_URL"])
        self.connection = psycopg2.connect(
                            database=self.url.path[1:],
                            user=self.url.username,
                            password=self.url.password,
                            host=self.url.hostname,
                            port=self.url.port
                            )
        self.connection.autocommit = True
        self.cursor = self.connection.cursor()

    def get_users(self, user_id):
        self.cursor.execute(SQLQueries.GET_USERS.format(user_id))
        result = self.cursor.fetchall()
        return result[0][0].split(',')

    def get_all_ids(self):
        self.cursor.execute(SQLQueries.GET_ALL_IDS)
        result = self.cursor.fetchall()
        return [x[0] for x in result]

    def add_user(self, user, user_id):
        if user == int(user_id):
             return {'status': 0, 'message': 'You can\'t invite yourself.'}
        users = self.get_users(user_id)
        if str(user) not in users:
            users.append(str(user))
            self.cursor.execute(SQLQueries.ADD_USER.format(','.join(users), user_id))

    def create_user(self, user_id):
        all_users = self.get_all_ids()
        if str(user_id) not in all_users:
            self.cursor.execute(SQLQueries.CREATE_USER.format(user_id))

    def close_connection(self):
        self.connection.close()

import sqlite3

class DataUser:
    def __init__(self, db_name = None):
       # self.con = sqlite3.connect(db_name, check_same_thread=False) if db_name else None
       # self.cursor = self.con.cursor()
        self.db_name = db_name # Для update

    def get_data(self, user_login):
        self.con = sqlite3.connect(self.db_name, check_same_thread=False) if self.db_name else None
        self.cursor = self.con.cursor()
        query_get_id = '''
                        SELECT id FROM users
                        WHERE login = (?)
                    '''

        rez = self.cursor.execute(query_get_id,(user_login,))
        res = rez.fetchone()

        query_get_user_data = '''
                                SELECT * FROM users_data
                                WHERE id = (?)
                            '''
        self.cursor.execute(query_get_user_data,( res[0],))
        data = self.cursor.fetchall()

        data_user = data[0]
        self.con.close() # Закрытие соединения базы
        return data_user
        
    def update_data(self, user_login , name, surname, age, about):
        self.con = sqlite3.connect(self.db_name, check_same_thread=False) if self.db_name else None
        self.cursor = self.con.cursor()
        query_update_new_user_data ='''
            UPDATE users_data
            SET  name = (?), surname = (?), age = (?), about = (?)
            WHERE user_id = (?)

        '''

        query_get_id = '''
            SELECT id FROM users
            WHERE login = (?)
        '''
        result = self.cursor.execute(query_get_id,(user_login,))
        response = result.fetchone()
        self.cursor.execute(query_update_new_user_data,(name, surname, age, about, response[0]))
        self.con.commit()
        self.con.close() # Закрытие соединения базы
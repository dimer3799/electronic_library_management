import sqlite3
import hashlib

class UserControl:
    def __init__(self, db_name = None):
        self.con = sqlite3.connect(db_name, check_same_thread=False) if db_name else None
        self.cursor = self.con.cursor()
        self.db_name = db_name # для authorezation

    def get_hash(self, password):
        hash = hashlib.sha1(password.encode())
        result = hash.hexdigest()
        return result

    def registration(self, user_form):
        self.con = sqlite3.connect(self.db_name, check_same_thread=False) if self.db_name else None
        self.cursor = self.con.cursor()

        # Обработка данных при регистрации

        # Обработка логина
        if user_form['login'].isspace() or user_form['login'] == '':
            return {'status': 'login_incorect'}
        
        # Обработка имени
        if user_form['name'].isspace() or user_form['name'] == '' or user_form['name'].isdigit():
            return {'status': 'name_incorect'}

        # Обработка фамилии
        if user_form['surname'].isspace() or user_form['surname'] == '' or user_form['surname'].isdigit():
            return {'status': 'surname_incorect'}

        # Обработка возраста
        if user_form['age'].isspace() or user_form['age'] == '' or user_form['age'].isalpha():
            return {'status': 'age_incorect'}

        # Обработка пароля
        if user_form['pass'].isspace() or user_form['pass'] == '':
            return {'status': 'pass_incorect'}

        query_add_new_user ='''
            INSERT INTO users
            (login, password_hash)
            VALUES
            (?, ?)
        '''

        query_add_new_user_data ='''
            INSERT INTO users_data
            (user_id, name, surname, age, about)
            VALUES
            (?, ?, ?, ?, ?)
        '''

        query_get_login = '''
            SELECT id FROM users
            WHERE login = (?)
        '''
        result = self.cursor.execute(query_get_login,(user_form['login'],))
        response = result.fetchone()
        if response is not None:
            self.con.close() # Закрытие соединения базы
            return {'status': 'login_busy'}
        else:
            self.cursor.execute(query_add_new_user,(user_form['login'],self.get_hash(user_form['pass'])))
            self.con.commit()
            result_login = self.cursor.execute(query_get_login,(user_form['login'],))
            response = result_login.fetchone()
            self.cursor.execute(query_add_new_user_data,(response[0], user_form['name'], user_form['surname'], user_form['age'], ''))
            self.con.commit()
            self.con.close() # Закрытие соединения базы
            return {'status': 'ok'}
            
    
    def authorization(self, user_form):
        self.con = sqlite3.connect(self.db_name, check_same_thread=False) if self.db_name else None
        self.cursor = self.con.cursor()
        query_get_login = '''
            SELECT id FROM users
            WHERE login = (?)
        '''
        query_get_password = '''
            SELECT id FROM users
            WHERE 
            login = (?) 
            AND  
            password_hash = (?)
        '''

        result = self.cursor.execute(query_get_login, (user_form['login'],))
        response = result.fetchone()
        if response is not None:        
            result = self.cursor.execute(query_get_password, (user_form['login'],self.get_hash(user_form['pass'])))
            response = result.fetchone()
            if response is not None:
                self.con.close() # Закрытие соединения базы

                return {'status': 'ok'}
            print('PASSWORD FAIL')
            self.con.close() # Закрытие соединения базы

            return {'status': 'err'}
        print('LOGIN FAIL')
        self.con.close() # Закрытие соединения базы
        return {'status': 'err'}

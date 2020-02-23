import sqlite3

class Book:
    def __init__(self, db_name = None):
        self.con = sqlite3.connect(db_name, check_same_thread=False) if db_name else None
        self.cursor = self.con.cursor()
        self.db_name = db_name

    # Вывод книг на главную страницу
    def output(self, index):
        index_start = index - 9
        index_finish = index
        self.con = sqlite3.connect(self.db_name, check_same_thread=False) if self.db_name else None
        self.cursor = self.con.cursor()
        # Вывод книг
        query_get_book = '''
            SELECT * FROM book
            WHERE id >= (?) AND id <= (?)
        '''
        result = self.cursor.execute(query_get_book,(index_start, index_finish))
        response = result.fetchall()

        # Закрытие курсора и соединения с базой
        self.con.close()

        return response

    def output_one(self, book_id):
        self.con = sqlite3.connect(self.db_name, check_same_thread=False) if self.db_name else None
        self.cursor = self.con.cursor()
        query_get_book_one = '''
            SELECT * FROM book
            WHERE id = (?)
            '''

        result = self.cursor.execute(query_get_book_one, (book_id,))
        response = result.fetchone()
           
        # Закрытие курсора и соединения с базой
        self.con.close()
        return response

    def genre(self):
        # Вывод всех жанров в список
        self.con = sqlite3.connect(self.db_name, check_same_thread=False) if self.db_name else None
        self.cursor = self.con.cursor()
        query_get_book_one = '''
            SELECT * FROM genre_book
            '''

        result = self.cursor.execute(query_get_book_one)
        response = result.fetchall()           
        # Закрытие курсора и соединения с базой
        self.con.close()
        return response
        
    def reviews(self, id_book):
        # Вывод отзывов на книгу
        self.con = sqlite3.connect(self.db_name, check_same_thread=False) if self.db_name else None
        self.cursor = self.con.cursor()
        self.con.close()
        #return response

    def search(self, user_form):
        #Поиск книги
        self.con = sqlite3.connect(self.db_name, check_same_thread=False) if self.db_name else None
        self.cursor = self.con.cursor()
        if (user_form['name_book'] == '') and (user_form['name_author'] == '') and (user_form['genre'] == 'Пусто'):
            return {'status': 'data_none'}
        
        self.con.close()


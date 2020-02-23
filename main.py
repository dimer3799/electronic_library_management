from flask import Flask, request, render_template, url_for, redirect, session
from menu import MENU_ANONYMOUS, MENU_USERS
from contrl import UserControl
from user_data import DataUser
from book import Book


app = Flask(__name__)
userControl = UserControl('data.db')
data_user = DataUser('data.db')
books = Book('data.db')
app.secret_key = 'q23//-1*4qqwqA'

@app.route('/')
@app.route('/index/<index>')
def index(index = 10):
    index = int(index)
    if index < 15:
        index = 10
    if session.get('user'):
        return render_template('index.html', menu_items = MENU_USERS, user = session['user'], data_book = books.output(index), index = index)    
    return render_template('index.html', menu_items = MENU_ANONYMOUS, user = False, data_book = books.output(index), index = index)

# Вход в личный кабинет
@app.route('/sign_in/', methods=['GET', 'POST'])
def sign_in():
    if request.method == 'GET':
        if session.get('user'):
            return redirect('/')
            # return render_template('index.html', menu_items = MENU_USERS , user = session['user'], data_book = books.output(10))
        return render_template('sign_in.html', menu_items = MENU_ANONYMOUS , user = False)

    result = userControl.authorization(request.form)

    if result['status'] == 'ok':
        session['user'] = request.form['login']
        return redirect('/')
            
    return render_template('sign_in.html', menu_items = MENU_ANONYMOUS, is_err = True, user = False)

# Добавление книг
@app.route('/control/')
def control():
    if session.get('user'):
        return render_template('control.html', menu_items = MENU_USERS, user = session['user'])

# Регистрация
@app.route('/sign_up/', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'GET':
        if session.get('user'): 
            return render_template('index.html', menu_items = MENU_USERS , user = session['user'])
        return render_template('sign_up.html', menu_items = MENU_ANONYMOUS, user = False)

    result = userControl.registration(request.form)
    # Недопустимы символы в логине
    if result['status'] == 'login_incorect':
        return render_template('sign_up.html', menu_items = MENU_ANONYMOUS, login_incorect = True, user = False)
    # Недопустимы символы в имени
    if result['status'] == 'name_incorect':
        return render_template('sign_up.html', menu_items = MENU_ANONYMOUS, name_incorect = True, user = False)
    # Недопустимы символы в фамилии
    if result['status'] == 'surname_incorect':
        return render_template('sign_up.html', menu_items = MENU_ANONYMOUS, surname_incorect = True, user = False)
    # Недопустимы символы в возрасте
    if result['status'] == 'age_incorect':
        return render_template('sign_up.html', menu_items = MENU_ANONYMOUS, age_incorect = True, user = False)
    # Недопустимы символы в пароле
    if result['status'] == 'pass_incorect':
        return render_template('sign_up.html', menu_items = MENU_ANONYMOUS, pass_incorect = True, user = False)


    
    if result['status'] == 'ok':
        session['user'] = request.form['login']
        return render_template('index.html', menu_items = MENU_USERS, user = session['user'])

    return render_template('sign_up.html', menu_items = MENU_ANONYMOUS, login_busy = True, user = False)

# Личный кабинет
@app.route('/user_page/', methods=['GET', 'POST'])
def user_page():
    if session.get('user'):
        if request.method == 'GET':
            return render_template('user_page.html', menu_items = MENU_USERS, user = session['user'], data = data_user.get_data(session['user']))
        else:
            data_user.update_data(session.get('user'), request.form['name'], request.form['surname'], request.form['age'], request.form['about'])
            return render_template('user_page.html', menu_items = MENU_USERS, user = session['user'], data = data_user.get_data(session['user']))

# Изменения личный данных
@app.route('/profile/')
def profile():
    if session.get('user'):
        return render_template('profile.html', menu_items = MENU_USERS, user = session['user'])

# Нет страницы
@app.errorhandler(404)
def not_found(error):
    return render_template('404.html', menu_items = MENU_ANONYMOUS,  user = False)

# Выход из личного кабинета
@app.route('/logout/')
def logout():
    session.pop('user')
    return redirect('/')

# Страница книги
@app.route('/book/<book_id>')
def book(book_id):
    if session.get('user'):
        return render_template('book.html', menu_items = MENU_USERS, user = session['user'], data_book = books.output_one(book_id))    
    return render_template('book.html', menu_items = MENU_ANONYMOUS, user = False, data_book = books.output_one(book_id))

# Поиск книги
@app.route('/search/', methods=['GET', 'POST'])
def search():
    data_incorect = False
    menu_items = MENU_ANONYMOUS
    user = False
    if request.method == 'POST':
        result = books.search(request.form)
        # Обработка пустых данных
        if result['status'] == 'data_none':
            data_incorect = True    
    if session.get('user'):
        menu_items = MENU_USERS
        user = session['user']
                
    return render_template('search.html', menu_items = menu_items, user = user, data_genre = books.genre(), data_incorect = data_incorect)

        

if __name__ == '__main__':
    app.run(debug=True)
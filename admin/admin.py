import sqlite3
from flask import Blueprint, flash, redirect, render_template, request, session, url_for, g

admin = Blueprint('admin', __name__, template_folder='templates', static_folder='static')

_hesh = [{"url": '.index', "title": 'Панель'},
         {"url": '.listpubs', "title": 'Список статей'},
         {"url": '.listusers', "title": 'Список пользователей'},
         {'url': '.logout', 'title': 'Выйти'}]


db = None
@admin.before_request
def before_request():
    """Установление соединения с БД перед выполнением запроса"""
    global db
    db = g.get('link_db')

@admin.teardown_request
def teardown_request(request):
    global db
    db = None
    return request

@admin.route('/')
def index():
  if not is_logged():
    return redirect(url_for('.login'))
  return render_template("admin/index.html", hesh = _hesh, title = "Админ-панель")

@admin.route('/login', methods = ["POST", "GET"])
def login():
  if is_logged():
    return redirect(url_for('.index'))
  
  if request.method == 'POST':
    if request.form['user'] == "admin" and request.form['psw'] == "12345":
      login_admin()
      return redirect(url_for('.index'))
    else:
      flash("Неверная пара логин-пароль")
  return render_template('admin/login.html', title = 'Админ-панель')

@admin.route('/logout', methods = ["POST", "GET"])
def logout():
  if request.method == 'POST':
    if not is_logged():
      return redirect(url_for('.login'))
  logout_admin()
  return redirect(url_for('.login'))

def login_admin():
  session['admin_logged'] = 1

def is_logged():
  return True if session.get('admin_logged') else False

def logout_admin():
  session.pop('admin_logged', None)

@admin.route('/list-pubs')
def listpubs():
    if not is_logged():
        return redirect(url_for('.login'))

    list = []
    if db:
        try:
            cur = db.cursor()
            cur.execute(f"SELECT title, text, url FROM posts")
            list = cur.fetchall()
        except sqlite3.Error as e:
            print("Ошибка получения статей из БД " + str(e))

    return render_template('admin/listpubs.html', title='Список статей', hesh = _hesh, list=list)

@admin.route('/list-users')
def listusers():
    if not is_logged():
        return redirect(url_for('.login'))

    list = []
    if db:
        try:
            cur = db.cursor()
            cur.execute(f"SELECT name, email FROM users ORDER BY time DESC")
            list = cur.fetchall()
        except sqlite3.Error as e:
            print("Ошибка получения статей из БД " + str(e))

    return render_template('admin/listusers.html', title='Список пользователей', hesh=_hesh, list=list)
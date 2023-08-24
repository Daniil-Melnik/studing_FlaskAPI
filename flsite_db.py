import sqlite3
import os
from flask import Flask, abort, flash, make_response, redirect, render_template, request, g, url_for
from FDataBase import FDataBase
from UserLogin import UserLogin
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, current_user, login_required, login_user, logout_user

# configuration
DATABASE = '/tmp/flsite.db'
DEBUG = True
SECRET_KEY = "qseft1234"
MAX_CONTENT_LENGTH = 1024 * 1024

app = Flask(__name__)
app.config.from_object(__name__)

app.config.update(dict(DATABASE=os.path.join(app.root_path, 'flsite.db')))

login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message = "Авторизуйтесь для доступа к закрытым данным"
login_manager.login_message_category = "success"

@login_manager.user_loader
def load_user(user_id):
  print("load user")
  return UserLogin().fromDB(user_id, dbase)

def connect_db():
  conn = sqlite3.connect(app.config['DATABASE'])
  conn.row_factory = sqlite3.Row
  return conn

def create_db():
  db = connect_db()
  with app.open_instance_resource('db_sql.sql', mode = 'r') as f:
    db.cursor().executescript(f.read())
  db.commit()
  db.close()

def get_db():
  if not hasattr(g, 'link_db'):
    g.link_db = connect_db()
  return g.link_db

dbase = None
@app.before_request
def before_request():
  global dbase
  db = get_db()
  dbase = FDataBase(db)

@app.route("/")
def index():
  return render_template('index_db.html', title = "Главная",hesh = dbase.getMenu(), posts = dbase.getPostsAnnonce())

@app.teardown_appcontext
def close_db(error):
  if hasattr(g, 'link_db'):
    g.link_db.close()

@app.route("/add_post", methods=["POST", "GET"])
def addPost():
  if request.method == "POST":
    if len(request.form['name']) > 4 and len(request.form['post']) > 10:
      res = dbase.addPost(request.form['name'], request.form['post'], request.form['url'])
      if not res:
        flash('Ошибка добавления статьи', category= 'error')
      else:
        flash('Статья добавлена успешно', category='success')
    else:
      flash('Ошибка добавления статьи', category='error')
  return render_template('add_post.html', hesh = dbase.getMenu(), title = "Добавление статьи")

@app.route("/post/<alias>")
@login_required
def showPost(alias):
  title, post = dbase.getPost(alias)
  if not title:
    abort(404)
  return render_template('post.html', hesh = dbase.getMenu(), title=title, post=post)

@app.route("/login", methods = ["GET", "POST"])
def login():
  if current_user.is_authenticated:
    return redirect(url_for('profile'))
  if request.method == 'POST':
    user = dbase.getUserByEmail(request.form['email'])
    if user and check_password_hash(user['psw'], request.form['psw']):
      userlogin = UserLogin().create(user)
      rm = True if request.form.get('remainme') else False
      login_user(userlogin, remember = rm)
      return redirect(request.args.get("next") or url_for('profile'))
    
    flash("Неверная пара логин-пароль", "error")
  return render_template("login.html", hesh = dbase.getMenu(), title = "Авторизация")

@app.route("/register", methods = ["POST", "GET"])
def register():
  if request.method == "POST":
    if len(request.form['name']) > 4 and len(request.form['email']) >4 \
    and len(request.form['psw']) > 4 and request.form['psw'] == request.form['psw2']:
      hash = generate_password_hash(request.form['psw'])
      res = dbase.addUser(request.form['name'], request.form['email'], hash)
      if res:
        flash("Вы успешно зарегистрированы", "success")
        return redirect(url_for('login'))
      else:
        flash("Ошибка при добавлении в БД", "error")
    else:
      flash("Неверно заполнены поля", "error")

  return render_template("register.html", hesh = dbase.getMenu(), title = "Регистрация")

@app.route("/logout")
@login_required
def logout():
  logout_user()
  flash("Вы вышли из аккаунта", "success")
  return redirect(url_for('login'))


@app.route("/profile")
@login_required
def profile():
  return render_template("profile.html", hesh = dbase.getMenu(), title = "Профиль")

@app.route("/userava")
@login_required
def userava():
  img = current_user.getAvatar(app)
  if not img:
    return ""
  
  h = make_response(img)
  h.headers['Content-Type'] = 'image/png'
  return h

if __name__ == "__main__":
    app.run(debug = True)

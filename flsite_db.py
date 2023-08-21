import sqlite3
import os
from flask import Flask, abort, flash, render_template, request, g
from FDataBase import FDataBase

# configuration
DATABASE = '/tmp/flsite.db'
DEBUG = True
SECRET_KEY = "qseft1234"

app = Flask(__name__)
app.config.from_object(__name__)

app.config.update(dict(DATABASE=os.path.join(app.root_path, 'flsite.db')))

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


@app.route("/")
def index():
  db = get_db()
  dbase = FDataBase(db)
  return render_template('index_db.html', title = "Главная",hesh = dbase.getMenu(), posts = dbase.getPostsAnnonce())

@app.teardown_appcontext
def close_db(error):
  if hasattr(g, 'link_db'):
    g.link_db.close()

@app.route("/add_post", methods=["POST", "GET"])
def addPost():
  db = get_db()
  dbase = FDataBase(db)

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

@app.route("/post/<int:id_post>")
def showPost(id_post):
  db = get_db()
  dbase = FDataBase(db)
  title, post = dbase.getPost(id_post)
  if not title:
    abort(404)
    
  return render_template('post.html', hesh = dbase.getMenu(), title=title, post=post)

if __name__ == "__main__":
    app.run(debug = True)
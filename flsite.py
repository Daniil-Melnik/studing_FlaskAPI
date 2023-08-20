from flask import Flask, render_template, url_for, request, flash, session, redirect
import os
import string

app = Flask(__name__)

app.config['SECRET_KEY'] = 'home56172'

_hesh = [{"name": "Установка", "url": "install-flask"},
         {"name": "Первое приложение", "url": "first-app"},
         {"name": "Обратная связь", "url": "contact"}]

@app.route("/index")
def index():
  print( url_for('index') )
  return render_template('index.html', title="Главная", hesh=_hesh)

@app.route("/about")
def about():
  print( url_for('about') )
  return render_template('about.html', title = "О сайте")

@app.route("/list")
def list():
  print( url_for('list') )
  return render_template('list.html', title = "Список", hesh = _hesh)

@app.route("/contact", methods=["POST", "GET"])
def contact():
  if request.method == 'POST':
    if len(request.form['username']) > 2:
      flash('Сообщение отправлено', category="success")
    else:
      flash('Ошибка отправки', category="error")
    print(request.form)
  return render_template('contact.html', title = "Обратная связь", hesh = _hesh)

@app.route("/profile/<username>")
def profile(username):
  return f"Пользователь: {username}"

@app.route("/login", methods={"POST", "GET"})
def login():
  if 'userLogged' in session:
    return redirect(url_for('profile', username=session['userLogged']))
  elif request.method == 'POST' and request.form['username'] == "dan" and request.form['psw'] == "123":
    session['userLogged'] = request.form['username']
    return redirect(url_for('profile', username=session['userLogged']))
  return render_template('login.html', title="Авторизация", hesh = _hesh)

@app.errorhandler(404)
def pageNotFound(error):
  return render_template('page404.html', title="Страница не найдена", hesh=_hesh)

# with app.test_request_context():
#   print( url_for('index') )

if __name__ == "__main__":
  app.run(debug = True)
from flask import Flask, render_template, url_for
import string

app = Flask(__name__)

_hesh = [{"name": "Установка", "url": "install-flask"},
         {"name": "Первое приложение", "url": "first-app"},
         {"name": "Обратная связь", "url": "contact"}]

@app.route("/index")
def index():
  print( url_for('index') )
  return render_template('index.html')

@app.route("/about")
def about():
  print( url_for('about') )
  return render_template('about.html', title = "О сайте")

@app.route("/list")
def list():
  print( url_for('list') )
  return render_template('list.html', title = "Список", hesh = _hesh)

@app.route("/contact")
def contact():
  print( url_for('contact') )
  return render_template('contacts.html', title = "Контакты")

@app.route("/profile/<username>/<data>")
def profile(username, data):
  print( url_for('profile', username="user1", data=123) )
  return f"Пользователь: {username}, Данные: {data}"

# with app.test_request_context():
#   print( url_for('index') )

if __name__ == "__main__":
  app.run(debug = True)
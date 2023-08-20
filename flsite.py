from flask import Flask, render_template, url_for
import string

app = Flask(__name__)

_hesh = [{"id" : 55, "text" : "Текст 1"}, {"id" : 56, "text" : "Текст 2"}, {"id" : 57, "text" : "Текст 3"}, {"id" : 58, "text" : "Текст 4"}, {"id" : 59, "text" : "Текст 5"}]

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

if __name__ == "__main__":
  app.run(debug = True)
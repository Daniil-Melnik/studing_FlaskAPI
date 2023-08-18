from flask import Flask, render_template
import string

app = Flask(__name__)

hesh = [{"id" : 55, "text" : "Текст 1"}, {"id" : 56, "text" : "Текст 2"}, {"id" : 57, "text" : "Текст 3"}, {"id" : 58, "text" : "Текст 4"}, {"id" : 59, "text" : "Текст 5"}]

@app.route("/index")
def index():
  return render_template('index.html')

@app.route("/about")
@app.route("/")
def about():
  st = "<h1>О сайте</h1>"
  for li in hesh:
    q = str(li["id"])
    t = str(li["text"])
    st+="<li>" + q + " " + t + "</li>"
  return st

if __name__ == "__main__":
  app.run(debug = True)
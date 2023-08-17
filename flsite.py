from flask import Flask
import string

app = Flask(__name__)

hesh = [{"id" : 55}, {"id" : 56}, {"id" : 57}, {"id" : 58}, {"id" : 59}]

@app.route("/index")
def index():
  return "index"

@app.route("/about")
@app.route("/")
def about():
  st = "<h1>О сайте</h1>"
  for li in hesh:
    q = str(li["id"])
    st+="<li>" + q + "</li>"
  return st

if __name__ == "__main__":
  app.run(debug = True)
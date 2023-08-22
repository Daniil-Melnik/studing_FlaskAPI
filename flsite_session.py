import datetime
from flask import Flask, render_template, make_response, url_for, request, session

app = Flask(__name__)
app.config['SECRET_KEY'] = 'qseft1234'
app.permanent_session_lifetime = datetime.timedelta(days = 10)

@app.route('/')
def index():
  if 'visits' in session:
    session['visits'] = session.get('visits') + 1
  else:
    session['visits'] = 1
  return(f"<h1>Main page</h1><p>Число просмотров: {session['visits']}")

data = [1, 2, 3, 4]
@app.route("/session")
def session_data():
  session.permanent = True
  if 'data' not in session:
    session['data'] = data
  else:
    session['data'][1] += 1
    session.modified = True
  return f"<p>session['data']: {session['data']}"

if __name__ == "__main__":
  app.run(debug = True)
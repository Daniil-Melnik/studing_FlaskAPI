from flask import Flask, render_template, make_response, url_for, request, session

app = Flask(__name__)
app.config['SECRET_KEY'] = 'qseft1234'

@app.route('/')
def index():
  if 'visits' in session:
    session['visits'] = session.get('visits') + 1
  else:
    session['visits'] = 1
  return(f"<h1>Main page</h1><p>Число просмотров: {session['visits']}")

if __name__ == "__main__":
  app.run(debug = True)
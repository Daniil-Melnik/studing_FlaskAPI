from flask import Flask, make_response, render_template

app = Flask(__name__)

_hesh = [{"title": "Главная", "url": "/"}, {"title": "Добавить статью", "url": "/add_post"}]

@app.route("/")
def index():
    content = render_template('index.html', hesh = _hesh, posts = [])
    res = make_response(content)
    res.headers['Content-Type'] = 'text/plain'
    res.headers['Server'] = 'flasksite'
    return res

if __name__ == "__main__":
    app.run(debug = True)
from flask import Flask, make_response, redirect, render_template, url_for

app = Flask(__name__)

_hesh = [{"title": "Главная", "url": "/"}, {"title": "Добавить статью", "url": "/add_post"}]

@app.route("/index_img")
def index_img():
  img = None
  with app.open_resource( app.root_path + "/static/images_html/framework-flask-intro.files/map.jpg", mode="rb") as f:
    img = f.read()
  if img is None:
    return "None image"
    
  res = make_response(img)
  res.headers['Content-Type'] = 'image/jpg'
  return res

@app.route("/index_text")
def index_text():
  content = render_template('index.html', hesh = _hesh, posts=[])
  res = make_response(content)
  res.headers['Content-Type'] = 'text/plain'
  res.headers['Server'] = 'flassksite'
  return res

@app.route('/transfer')
def transfer():
  return redirect(url_for('index_text'), 301)

if __name__ == "__main__":
    app.run(debug = True)
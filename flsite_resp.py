from flask import Flask, make_response, render_template

app = Flask(__name__)

_hesh = [{"title": "Главная", "url": "/"}, {"title": "Добавить статью", "url": "/add_post"}]

@app.route("/")
def index():
    img = None
    with app.open_resource( app.root_path + "/static/images_html/framework-flask-intro.files/map.jpg", mode="rb") as f:
        img = f.read()
    if img is None:
        return "None image"
    
    res = make_response(img)
    res.headers['Content-Type'] = 'image/jpg'
    return res

if __name__ == "__main__":
    app.run(debug = True)
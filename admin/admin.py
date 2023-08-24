from flask import Blueprint, flash, redirect, render_template, request, session, url_for

admin = Blueprint('admin', __name__, template_folder='templates', static_folder='static')

@admin.route('/')
def index():
  return"admin"

@admin.route('/login', methods = ["POST", "GET"])
def login():
  if request.method == 'POST':
    if request.form['user'] == "admin" and request.form['psw'] == "12345":
      login_admin()
      return redirect(url_for('.index'))
    else:
      flash("Неверная пара логин-пароль")
  return render_template('admin/login.html', title = 'Админ-панель')

@admin.route('/logout', methods = ["POST", "GET"])
def logout():
  if request.method == 'POST':
    if not is_logged():
      return redirect(url_for('.login'))
  logout_admin()
  return redirect(url_for('.login'))

def login_admin():
  session['admin_logged'] = 1

def is_logged():
  return True if session.get('admin_logged') else False

def logout_admin():
  session.pop('admin_logged', None)
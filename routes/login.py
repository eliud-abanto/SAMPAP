from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, login_user, login_required, current_user, logout_user
from models.user import User
from utils.db import db
from utils.formsLogin.forms import LoginForm

login_manager = LoginManager()

user_login = Blueprint('login', __name__)

@user_login.route('/', methods=["POST", "GET"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('download_posts.index'))
    form = LoginForm()
    if form.validate_on_submit() and request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        user = User.query.filter_by(username=username).first()
        if user is not None and user.verify_password(password):
            login_user(user)
            return redirect(url_for("login.dashboard"))
        else:
            flash('Credenciales invalidas.')
    return render_template("login.html", form=form)

@user_login.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard/dashboard.html', name=current_user.firstname, lastname=current_user.lastname)

@user_login.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for("login.login"))

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
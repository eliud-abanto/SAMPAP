from flask import Flask, render_template, request
from routes.users import users
from routes.posts import posts
from routes.download import download_posts
from routes.login import user_login, login_manager
from routes.employee import employees
from routes.galery import galery
from utils.db import db
from flask_wtf.csrf import CSRFProtect
from utils.migrations import migrate

#UPLOAD_FOLDER = '/static/images/posts/'

app = Flask(__name__)
app.config['SECRET_KEY'] = 'SECRETINTRANET'
#app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

### TOKEN CSRF PARA FORMULAROS
CSRFProtect(app)

#PARA OBTENER BASE URL DE LA APLICACION
@app.context_processor
def inject_base_url():
    return {'base_url': request.scheme + '://' + request.host}

### RESPUESTA 404 PAGINAS DE ERROR
def page_not_found(error):
    return render_template('error404.html'), 404

app.register_error_handler(404, page_not_found)

#### CONFIGURACION DE BASE DE DATOS
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql://root:"''"@localhost/intra"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
migrate.init_app(app, db)
login_manager.init_app(app)
login_manager.login_view = 'login.login'

app.register_blueprint(users)
app.register_blueprint(posts)
app.register_blueprint(download_posts)
app.register_blueprint(user_login)
app.register_blueprint(employees)
app.register_blueprint(galery)

from flask import Blueprint, render_template, request, redirect, jsonify
from flask_login import login_required
from models.user import User
from werkzeug.security import generate_password_hash
from utils.db import db
from utils.formsLogin.forms import SignUpForm

users = Blueprint('users', __name__)

@users.route('/users')
@login_required
def index():
    users = User.query.all()
    return render_template("users/index.html", users=users)

@users.route('/list-users', methods=["GET"])
@login_required
def items():
    items = User.query.all()
    return jsonify(data=[item.to_dict() for item in items])

@users.route('/users/create', methods=['POST'])
@login_required
def create():
    form = SignUpForm(request.form)
    if form.validate_on_submit() and request.method == "POST":
        id = request.form['id']
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        username = request.form['username']
        role = request.form['role']
        status = request.form['status']
        password = request.form['password']

        # Validar usuario
        userr = User.query.filter_by(username=username).first()
        if userr and str(userr.id) != id:
            return jsonify(success=False, errors=form.errors)
        
        if int(id) == 0:
            new_user = User(firstname,lastname,username,password,role,status)
            db.session.add(new_user)
            db.session.commit()
            return jsonify(success=True, msg="Usuario agregado correctamente")
        else:
            # Para actualizar
            userId = User.query.filter_by(id=id).first()
            if userId is None:
                return jsonify(success=False, errors="Usuario no encontrado")
            #userId = User.query.get(id)
            if request.form['password'] == '':
                userId.firstname = firstname
                userId.lastname = lastname
                userId.username = username
                userId.role = role
                userId.status = status
                db.session.commit()
                return jsonify(success=True, msg="Usuario actualizado correctamente sin password")
            else:
                # Para actualizar
                userId = User.query.filter_by(id=id).first()
                if userId is None:
                    return jsonify(success=False, errors="Usuario no encontrado")
                #userId = User.query.get(id)
                userId.firstname = firstname
                userId.lastname = lastname
                userId.username = username
                userId.password = generate_password_hash(password)
                userId.role = role
                userId.status = status
                db.session.commit()
                return jsonify(success=True, msg="Usuario actualizado correctamente con password")
    else:
        return jsonify(success=False, errors=form.errors)
    
@users.route('/user/edit/<int:user_id>', methods=['GET'])
@login_required
def edit_user(user_id):
    user = User.query.filter_by(id=user_id).first()
    return jsonify(user.to_dict())

@users.route('/delete_user/<int:user_id>', methods=['DELETE'])
@login_required
def delete_user(user_id):
    user = User.query.get(user_id)
    db.session.delete(user)
    db.session.commit()
    return jsonify(success=True)

from flask import Blueprint, render_template, redirect, request, flash, url_for, current_app as app, jsonify
from flask_login import current_user, login_required
from flask_login import current_user
from models.post import Post
from utils.db import db
from utils.formsPost.forms import PostForm
from werkzeug.utils import secure_filename
import os
from datetime import datetime
from slugify import slugify
from flask import send_from_directory
from sqlalchemy import or_

posts = Blueprint('posts', __name__)

ALLOWED_EXTENSIONS = {'xlsx', 'xls', 'doc', 'docx'}

@posts.route('/posts')
@login_required
def index():
    #posts = Post.query.all()
    return render_template("posts/post.html", posts=posts)

@posts.route('/list-posts', methods=["GET"])
@login_required
def items():
    items = Post.query.all()
    return jsonify(data=[item.to_dict() for item in items])

# PARA TRABAJAR FORMATO DE IMAGENES
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# PARA TRABAJAR LOS SLUG DE LOS TITULOS DE CADA POST
def generate_slug(title):
    return slugify(title)

@posts.route('/posts/create', methods=['POST','GET'])
@login_required
def create():
    form = PostForm()
    if form.validate_on_submit() and request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        image = request.files['image']
        status = request.form['status']
        date = datetime.utcnow()
        user_id = current_user.id
        created_on = datetime.utcnow()
        updated_on = datetime.utcnow()

        file_filename = None

        if image and allowed_file(image.filename):
            timestamp = datetime.timestamp(datetime.now())
            file_filename = secure_filename(str(timestamp) + '_' + image.filename)
            if file_filename.rsplit('.', 1)[1].lower() in ['xls', 'xlsx', 'doc', 'docx']:
                create_filename = secure_filename(str(timestamp) + '_' + image.filename)
                image.save(os.path.join(app.static_folder, 'files/' + create_filename))

        if image:
            if Post.query.filter(or_(Post.image == image)).first():  # Utilizar el operador OR para la consulta
                flash('Error: El archivo ya existe en la base de datos', 'error')
                return render_template('posts/newPost.html', form=form)


        slug_generated = generate_slug(title)
        new_post = Post(title, description, file_filename, slug_generated, status,date,user_id,created_on,updated_on)
        db.session.add(new_post)
        db.session.commit()
        flash('Archivo creado exitosamente!', 'success')

    return render_template('posts/newPost.html', form=form)

# @posts.route('/post/edit/<int:post_id>', methods=['POST','GET'])
# @login_required
# def post_edit(post_id):
#     post = Post.query.get_or_404(post_id)
#     form = PostForm(obj=post)

#     if form.validate_on_submit():
#         form.populate_obj(post)
#         image = request.files['image']

#         if image and allowed_file(image.filename):
#             timestamp = datetime.timestamp(datetime.now())
#             file_filename = secure_filename(str(timestamp) + '_' + image.filename)
#             if file_filename.rsplit('.', 1)[1].lower() in ['xls', 'xlsx', 'doc', 'docx']:
#                 if file_filename.rsplit('.', 1)[1].lower() in ['xls', 'xlsx']:
#                     file_path = os.path.join(app.static_folder, 'files/', file_filename)
#                 elif file_filename.rsplit('.', 1)[1].lower() in ['doc', 'docx']:
#                     file_path = os.path.join(app.static_folder, 'files/', file_filename)
                
#                 image.save(file_path)
#                 post.file_filename = file_path

#         db.session.commit()
#         flash('Post actualizado exitosamente!', 'success')
#         return redirect(url_for('posts.post_edit', post_id=post.id))

#     return render_template('posts/post_edit.html', post=post, form=form)

# @posts.route('/post/edit/<int:post_id>', methods=['POST','GET'])
# @login_required
# def post_edit(post_id):
#     post = Post.query.get_or_404(post_id)
#     form = PostForm(obj=post)  # Pasar el objeto 'post' al formulario para cargar los valores actuales

#     if form.validate_on_submit() and request.method == 'POST':
#         form.populate_obj(post)  # Actualizar los datos del objeto 'post' con los datos del formulario
#         image = request.files['image']
#         # word_filename = None
#         file_filename = None

#         if image and allowed_file(image.filename):
#             if post.image:
#                 if os.path.exists(os.path.join(app.static_folder, 'files/word', post.image)):
#                     os.remove(os.path.join(app.static_folder, 'files/word', post.image))   # Eliminar el archivo de Word existente

#             timestamp = datetime.timestamp(datetime())
#             file_filename_new = secure_filename(str(timestamp) + '_' + image.filename)  # Crear un nuevo nombre de archivo basado en la marca de tiempo y el nombre del archivo
#             if file_filename.rsplit('.', 1)[1].lower() in ['xls', 'xlsx']:
#                 excel_filename = secure_filename(str(timestamp) + '_' + image.filename)
#                 image.save(os.path.join(app.static, 'files/excel/' + excel_filename))
#                 post.excel_filename = excel_filename  # Actualizar el nombre del archivo de Excel en el objeto 'post'
#             elif file_filename.rsplit('.', 1)[1].lower() in ['doc', 'docx']:
#                 word_filename = secure_filename(str(timestamp) + '_' + image.filename)
#                 image.save(os.path.join(app.static_folder, 'files/word/' + word_filename))
#                 post.word_filename = word_filename  # Actualizar el nombre del archivo de Word en el objeto 'post'

#         db.session.commit()
#         flash('Post actualizado exitosamente!', 'success')
#         return redirect(url_for('posts.post_edit', post_id=post.id))  # Redirigir a la página de edición del post

#     return render_template('posts/post_edit.html', post=post, form=form)


@posts.route('/delete_post/<int:post_id>', methods=['DELETE'])
@login_required
def delete_post(post_id):
    post = Post.query.get(post_id)
    db.session.delete(post)
    db.session.commit()
    return jsonify(success=True)



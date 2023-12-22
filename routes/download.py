from flask import Blueprint, render_template, jsonify
from flask_login import login_required
from models.post import Post

download_posts = Blueprint('download_posts', __name__)

@download_posts.route('/download_posts')
@login_required
def index():
    download_posts = Post.query.all()
    return render_template("download/download_posts.html", download_posts=download_posts)

@download_posts.route('/list-posts', methods=["GET"])
@login_required
def items():
    items = Post.query.all()
    return jsonify(data=[item.to_dict() for item in items])

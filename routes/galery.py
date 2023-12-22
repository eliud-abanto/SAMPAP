from flask import Blueprint, render_template
from models.galery import Galery

galery = Blueprint('galery', __name__)

@galery.route('/galery')
def faq():
    galery = Galery.query.all()
    return render_template('galery/galery.html', galery=galery)
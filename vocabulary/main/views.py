from flask import render_template
from flask_login import current_user

from . import main


@main.route('/', methods=['GET','POST'])
def index():
    return render_template('index.html')
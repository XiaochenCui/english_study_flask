import json

from flask import flash
from flask import redirect
from flask import render_template
from flask import request
from flask import url_for
from flask_login import current_user, login_required

from externel_lib.serialize import serialize_list
from vocabulary import db
from vocabulary.main.forms import PreferencesForm
from vocabulary.models import Word
from . import main


@main.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')


@main.route('/word', methods=['GET', 'POST'])
@login_required
def word():
    if not current_user.level:
        flash('请先设置单词等级')
        return redirect(url_for('main.preferences'))
    else:
        # words_index 中的元素为一个tuple(world, 熟悉程度, 是否记住)
        words_index = current_user.get_words(10)

        words = []
        for i in words_index:
            word = Word.query.filter_by(word=i[0]).first()
            words.append(word)

        return render_template('word_learn.html', words=words)


@main.route('/get-word', methods=['POST'])
def get_word():
    words = current_user.get_words(5)
    if word:
        return json.dumps({'status': 'OK', 'words': serialize_list(words)})
    else:
        return json.dumps({'status': 'ERROR'})


@main.route('/preferences', methods=['GET', 'POST'])
@login_required
def preferences():
    form = PreferencesForm()

    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.level = form.level.data
        current_user.learn_word_number_every_day = form.learn_number.data

        db.session.add(current_user)

        flash('设置已更改')
        return redirect(request.url)

    form.username.data = current_user.username
    form.level.data = current_user.level
    form.learn_number.data = current_user.learn_word_number_every_day

    return render_template('preferences.html', form=form)

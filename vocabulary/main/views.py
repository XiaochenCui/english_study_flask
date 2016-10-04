import json

from flask import flash
from flask import redirect
from flask import render_template
from flask import request
from flask import url_for
from flask_login import current_user, login_required
from sqlalchemy.orm import query
from sqlalchemy import and_

from external_lib.serialize import serialize_list
from vocabulary import db
from vocabulary.main.forms import PreferencesForm, AddNoteForm
from vocabulary.models import Word, Note
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
        if current_user.task_complied:
            flash('今天的单词任务已经完成')
            return render_template('mission_complied.html')

        else:
            if not current_user.words_today:
                # 未加载
                flash('正在加载单词列表，请稍后刷新页面')
                return render_template('word_learn.html')
            else:
                # 获取单词列表
                words = current_user.get_words(10)

                words_obj = []

                for word in words:
                    word_obj = Word.query.filter_by(word=word).first()
                    if word_obj:
                        words_obj.append(word_obj)

                return render_template('word_learn.html', words=words_obj)


@main.route('/get-word', methods=['POST'])
@login_required
def get_word():
    words_with_flag = request.get_json(force=True, silent=True, cache=True)

    # 接受单词列表
    current_user.set_words(words_with_flag)

    if current_user.task_complied:
        return json.dumps({'status': 'COMPLIED'})
    else:
        words = current_user.get_words(10)

        if words:
            words_obj = []
            for word in words:
                word_obj = Word.query.filter_by(word=word).first()
                words_obj.append(word_obj)

            return json.dumps({'status': 'OK', 'words': serialize_list(words_obj)})
        else:
            return json.dumps({'status': 'ERROR'})


@main.route('/notes-mine', methods=['POST'])
@login_required
def get_notes_mine():
    data = request.get_json(force=True, silent=True, cache=True)

    user_id = data['user_id']
    word = data['word']

    notes = []

    result = db.engine.execute(
        "SELECT * FROM notes JOIN words ON notes.word_id = words.id WHERE notes.user_id={user_id} AND words.word='{word}';".format(
            user_id=user_id, word=word))

    for r in result:
        notes.append({'context': r['context'],
                      'user': r['user_id']})

    if notes:
        return json.dumps(notes)
    else:
        return json.dumps({'status': 'NONE'})


@main.route('/notes-others', methods=['POST'])
@login_required
def get_notes_others():
    data = request.get_json(force=True, silent=True, cache=True)

    user_id = data['user_id']
    word = data['word']

    notes = []

    result = db.engine.execute(
        "SELECT * FROM notes JOIN words ON notes.word_id = words.id WHERE notes.user_id<>{user_id} AND words.word='{word}';".format(
            user_id=user_id, word=word))

    for r in result:
        notes.append({'context': r['context'],
                      'user': r['user_id']})

    if notes:
        return json.dumps(notes)
    else:
        return json.dumps({'status': 'NONE'})


@main.route('/add-note', methods=['POST'])
@login_required
def add_note():
    context = request.form['context']
    word = request.form['word']

    if context:
        flash('添加成功')
        return json.dumps({'status': 'SUCCESS'})
    else:
        flash('笔记不能为空')
        return json.dumps({'status': 'NONE'})


@main.route('/notes/<word>', methods=['GET', 'POST'])
@login_required
def notes(word=None):
    form = AddNoteForm()

    if word:
        form.word.default = word

    if form.validate_on_submit():
        word_obj = Word.query.filter_by(word=word).first()

        note = Note(
            context=form.context.data,
            user_id=current_user.id,
            word_id=word_obj.id
        )

        db.session.add(note)
        db.session.commit()

        notes_mine, notes_others = Note.get_notes(current_user.id, word_obj.word)

        flash('添加成功')
        return render_template('notes.html',
                               form=form,
                               notes_mine=notes_mine,
                               notes_others=notes_others, )

    else:
        if word:
            notes_mine, notes_others = Note.get_notes(current_user.id, word)

            return render_template('notes.html',
                                   form=form,
                                   notes_mine=notes_mine,
                                   notes_others=notes_others, )

        else:
            return render_template('404.html')


@main.route('/mission-complied', methods=['GET'])
@login_required
def mission_complied():
    flash('任务完成！')

    return render_template('mission_complied.html')


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

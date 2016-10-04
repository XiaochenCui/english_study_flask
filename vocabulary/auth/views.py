from flask import render_template, redirect, request, url_for, flash
from flask_login import login_user, logout_user, current_user

from vocabulary import db
from vocabulary.models import User
from . import auth
from .forms import LoginForm, RegistrationForm, ChangePasswordForm


@auth.before_app_request
def before_request():
    if current_user.is_authenticated:
        current_user.ping()


@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.verify_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect(url_for('main.index'))
        else:
            flash('incorrect username or password')
            return redirect(url_for('auth.login'))
    else:
        return render_template('auth/login.html', form=form)


@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()

    if form.validate_on_submit():
        user = User(username=form.username.data,
                    password=form.password.data)
        db.session.add(user)
        db.session.commit()

        return redirect(url_for('auth.login'))
    else:
        return render_template('auth/register.html', form=form)


@auth.route('/change-password', methods=['GET', 'POST'])
def change_password():
    form = ChangePasswordForm()
    if form.validate_on_submit():
        if current_user.verify_password(form.old_password.data):
            current_user.password = form.password.data
            db.session.add(current_user)
            flash('密码更改成功')
            return redirect(url_for('main.index'))
        else:
            flash('密码不可用')
    return render_template("auth/change_password.html", form=form)


@auth.route('/logout', methods=['GET', 'POST'])
def logout():
    logout_user()
    flash('你已经登出')
    return redirect(url_for('main.index'))

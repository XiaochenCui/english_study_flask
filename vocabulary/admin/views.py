from flask import current_app
from flask import flash
from flask import redirect
from flask import request
from flask import url_for
import flask_admin
from flask_login import current_user
from flask_admin.menu import MenuLink
from flask_admin.contrib.sqla import ModelView

from vocabulary import db
from vocabulary.models import User, Word


class AdminModelView(ModelView):

    def is_accessible(self):
        if current_app.config['DEBUG']:
            return True
        else:
            return current_user.is_administrator

    def inaccessible_callback(self, name, **kwargs):
        if current_user.is_authenticated:
            flash('你没有管理员权限')
            return redirect(url_for('main.index'))
        else:
            flash('请先进行登录')
            return redirect(url_for('auth.login', next=request.url))


class UserView(AdminModelView):
    # 不可见的列
    column_exclude_list = ['password_hash']


class WordView(AdminModelView):
    pass


admin = flask_admin.Admin(name='Admin',
                          index_view=flask_admin.AdminIndexView(),
                          template_mode='bootstrap3')

# 增加view
admin.add_view(UserView(User, db.session))
admin.add_view(WordView(Word, db.session))

# 增加主页链接
admin.add_link(MenuLink(name='返回主页', url='/'))

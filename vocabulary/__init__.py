from flask import Flask
from flask import request
from flask import session
from flask_bootstrap import Bootstrap
from flask_mail import Mail
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_babelex import Babel

from config import config

bootstrap = Bootstrap()
mail = Mail()
moment = Moment()

db = SQLAlchemy()

login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'auth.login'
login_manager.login_message = '请登录'
login_manager.needs_refresh_message = '请重新验证'



def create_app(config_name):
    app = Flask(__name__)

    app.config.from_object(config[config_name])

    bootstrap.init_app(app)
    mail.init_app(app)
    moment.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)

    from .admin.views import admin
    admin.init_app(app)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/auth')

    # 初始化 babel
    babel = Babel(app)

    @babel.localeselector
    def get_locale():
        override = request.args.get('lang')

        if override:
            session['lang'] = override

        return session.get('lang', 'zh_CN')

    return app

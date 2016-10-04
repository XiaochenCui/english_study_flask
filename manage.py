from flask_script import Manager, Shell
from flask_migrate import Migrate, MigrateCommand

from vocabulary import create_app
from vocabulary.models import *

app = create_app('default')

manager = Manager(app)
migrate = Migrate(app, db)


def make_shell_context():
    return dict(app=app, db=db, User=User, Word=Word, Note=Note)


manager.add_command("shell", Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()
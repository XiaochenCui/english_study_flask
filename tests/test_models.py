import unittest
from flask import current_app

from vocabulary import create_app, db
from vocabulary.models import Word, User


class ModelsTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()

        db.create_all()

        # Word.load_json('/home/chenxiao/Dropbox/project/english_study_flask/vocabulary/resource/cet4.json')

    def tearDown(self):
        db.session.remove()
        db.drop_all()

        self.app_context.pop()

        # def generator_user(self):
        #     self.user_123 = User(username='123',
        #                          password='123')
        #     self.user_123.level = 'CET4'
        #     self.user_123.init_words()
        #
        #     self.user_abc = User(username='abc', password='123')
        #
        # def test_words(self):
        #     words = Word.query.all()
        #     print(words)
        #
        # def test_user123(self):
        #     self.generator_user()
        #
        #     print(self.user_123.words.keys())

import json
import os
import pickle
import random
import traceback
from collections import defaultdict

import datetime
from collections import deque
from copy import copy
from functools import partial, partialmethod
from threading import Thread

from flask import current_app
from flask_login import UserMixin

from werkzeug.security import generate_password_hash, check_password_hash

from externel_lib.dictionary import get_the_value, get_the_key, dict_to_tuple
from externel_lib.tries import TrieST
from . import db, login_manager


class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(128))

    admin = db.Column(db.Boolean, default=False)

    # 用户的学习等级
    level = db.Column(db.String(64))

    # 用户学习的单词信息
    # 单词的熟悉程度从1到5
    # 用trie树保存
    words = db.Column(db.PickleType)

    # list ot tuples
    # [(word, i, f)]:
    #   i: 熟悉程度
    #   f: 今天是否需要背诵
    words_today = db.Column(db.PickleType)

    words_update_time = db.Column(db.DateTime)

    # 今天的任务是否完成
    task_complied = db.Column(db.Boolean, default=False)

    # 每天的学习量
    learn_word_number_every_day = db.Column(db.Integer)

    # 最后一次登录的时间
    last_seen = db.Column(db.DateTime(), default=datetime.datetime.today)

    words_queue = deque()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # 初始化self.admin值
        if self.username == 'admin':
            self.admin = True
        else:
            self.admin = False

        # 初始化words
        self.words = TrieST()

    @property
    def password(self):
        raise AttributeError('password is not readable.')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    @property
    def is_administrator(self):
        return self.admin

    def get_words_tuple(self, num):
        """
        返回n个待学的单词

        Args:
            num:
        Returns:
            deque
        """

        # 如果单词队列空，则先进行初始化
        if not self.words_queue:
            self.words_queue.extend([i for i in filter(lambda i: not i[2], self.words_today)])

        # 元素转为tuple
        # self.words_queue_tuple = [dict_to_tuple(i, False) for i in self.words_queue]

        # 修正 num
        if num > len(self.words_queue):
            num = len(self.words_queue)

        # 切片 words=self.words_queue[:i]
        words = [self.words_queue[i] for i in range(num)]

        return words

    def get_words(self, num):
        words_tuple = self.get_words_tuple(num)
        words = [i[0] for i in words_tuple]

        return words

    def set_words(self, words_with_flag: list):
        """
        将学习结果回写

        Args:
            words_with_flag: list of tuples.
        """
        for word in words_with_flag:

            # 将所有指定单词从deque中删除
            User.recursion_delete(self.words_queue, word['word'])

            # 将没记住的单词重新加入deque尾部
            if not word['flag']:
                self.words_queue.append(word)
            # 将记住的单词回写，并将熟悉程度+1
            else:
                self.words_extent_increase(word['word'])

        # 如果队列空，则表示任务完成
        if not self.words_queue:
            self.task_complied = True

        db.session.add(self)
        db.session.commit()

    @staticmethod
    def recursion_delete(iterator, element):
        """
        临时版本, iterator为deque,i为dict或tuple

        Args:
            iterator:
            element:
        """
        for i in iterator:
            if isinstance(i, dict):
                if element in i.keys():
                    iterator.remove(i)
                    return True
            elif isinstance(i, tuple):
                if element in i:
                    iterator.remove(i)
                    return True
        return False

    def words_extent_increase(self, word):
        # copy self.words_toady
        words_copy = copy(self.words)

        # update self.words
        words_copy[word] += 1

        self.words = copy(words_copy)

        # copy self.words_toady
        words_copy = copy(self.words_today)

        # update self.words_toady
        for i in range(len(words_copy)):
            w = words_copy[i]
            if w[0] == word:
                words_copy[i] = (word, w[1] + 1, True)

        self.words_today = copy(words_copy)

    def get_words_piece(self):
        pass

    def set_level(self, level=None):
        self.level = random.choice(Word.LEVELS)
        db.session.add(self)
        db.session.commit()

    def init_words(self, level=None, initial=True):
        """
        把指定单词等级中的单词全部装入self.words

        Args:
            level: 如果为空，则将装入self.level对应的单词
            initial: 如果为True,则先将self.words重置为空
        """
        words = Word.filter_by_level(self.level if not level else level)

        if initial:
            self.words = TrieST()

        for word in words:
            self.words = self.add_word(word.word)

        db.session.add(self)
        db.session.commit()

    add_words = partialmethod(init_words, initial=False)

    def add_word(self, word, level=1):
        self.words[word] = level
        return self.words

    def get_word_level(self, word):
        return self.words[word]

    def ping(self):
        self.last_seen = datetime.datetime.today()

        # 更新今日单词
        if not self.words_update_time or self.words_update_time.date() != datetime.datetime.today().date():
            self.update_words_today()

        db.session.add(self)

    def async_function(self, app, *args, **kwargs):
        pass

    def update_words_today(self):
        app = current_app._get_current_object()

        t = Thread(target=self.update_words_today_async, args=[app])
        t.start()

        return t

    def update_words_today_async(self, app):
        """
        更新今天需要学的单词

        Returns:

        """
        with app.app_context():
            if not self:
                return

            # 获取单词列表
            l = self.words.keys()
            # 过滤
            l = [i for i in filter(lambda x: get_the_value(x) < 5, l)]
            # 排序
            l.sort(key=get_the_value)

            dif = len(l) - self.learn_word_number_every_day

            # 如果l中的单词不够，从数据表words中再取
            if dif < 0:
                dif_words = Word.filter_by_level(self.level)[:(-dif)]

                for word in dif_words:
                    # 将新单词加入self.words
                    self.add_word(word.word)

                    # 将新单词加入self.words_today
                    l += [{word.word: 1}]

            else:
                l = l[:self.learn_word_number_every_day]

            self.words_today = [dict_to_tuple(i, False) for i in l]

            self.words_update_time = datetime.datetime.today()

            current_db_sessions = db.session.object_session(self)
            current_db_sessions.add(self)

    def is_first_login_in_today(self):
        pass

    @staticmethod
    def on_changed_level(target, value, oldvalue, initiator):
        """
        当User().level改变时，添加words

        Args:
            target:
            value: new level
            oldvalue:
            initiator:
        """
        target.add_words(level=value)

    def __repr__(self):
        return '{cls}: {name}'.format(
            cls=self.__class__.__name__,
            name=self.username,
        )

    __str__ = __repr__


db.event.listen(User.level, 'set', User.on_changed_level)


class Word(db.Model):
    __tablename__ = 'words'

    id = db.Column(db.Integer, primary_key=True)

    word = db.Column(db.String(128), unique=True, index=True)

    description = db.Column(db.Text)
    phonetic = db.Column(db.String(128))
    tags = db.Column(db.PickleType)

    LEVELS = ['CET4', 'CET6', 'TOEFL']

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # 初始化self.admin值
        self.tags = random.choice(Word.LEVELS)

    def init_data(self):
        pass

    def set_tags(self, tags=None):
        self.tags = [random.choice(Word.LEVELS), ]
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def load_json(file):
        """
        将file(json格式)中的单词提交到数据库

        :param file:
        """
        with open(file, 'r') as f:
            data = json.load(f)

            words = data['content']

            for word in words:
                try:
                    word_dic = {'word': word['word'],
                                'description': word['description'],
                                'phonetic': word['phonetic']}
                    insert_if_not_exist(db.session, Word, **word_dic)
                except KeyError:
                    traceback.print_exc()
                    print('KeyError occurred in {}'.format(word))

    @classmethod
    def filter_by_level(cls, level, words=None):
        result = []

        if not words:
            words = Word.query.all()
        for word in words:
            if level in word.tags:
                result.append(word)
        return result

    def __repr__(self):
        return '{cls}: {word}'.format(
            cls=self.__class__.__name__,
            word=self.word,
        )

    __str__ = __repr__


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


def insert_if_not_exist(session, model, **kwargs):
    """
    向数据库中提交一个object(如果原先不存在)

    :param session:
    :param model:
    :param kwargs:
    :return:
    """
    instance = session.query(model).filter_by(**kwargs).first()
    if instance:
        return
    else:
        instance = model(**kwargs)
        session.add(instance)
        session.commit()

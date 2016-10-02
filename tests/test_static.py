import unittest
from collections import deque

from vocabulary.models import User


class StaticTestCase(unittest.TestCase):
    def test_recursion_delete(self):
        q = deque([{'first': 1},
                   {'second': 2},
                   {'third': 3}])
        e1 = 'third'
        e2 = 'nice'

        self.assertEqual(len(q), 3)
        self.assertTrue(User.recursion_delete(q, e1))
        self.assertFalse(User.recursion_delete(q, e2))
        self.assertEqual(len(q), 2)

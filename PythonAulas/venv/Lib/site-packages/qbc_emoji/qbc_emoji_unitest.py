import unittest
from ybc_emoji import *


class MyTestCase(unittest.TestCase):
    def test_word2emoji(self):
        word2emoji('猿编程', '😊')


if __name__ == '__main__':
    unittest.main()

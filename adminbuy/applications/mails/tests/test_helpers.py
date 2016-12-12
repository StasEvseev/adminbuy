# coding: utf-8


import unittest

from adminbuy.applications.mails.helper import rus_to_eng


class Test(unittest.TestCase):
    def test_rus_to_eng(self):
        result = rus_to_eng(u'Мама мыла раму')
        self.assertEqual(u'Mama myla ramu', result)

        result = rus_to_eng(u'Жили были шука и щенок')
        self.assertEqual(u'Jili byli suka i senok', result)

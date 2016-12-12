# coding: utf-8

import unittest

from adminbuy.excel import get_name_number


class TestCase(unittest.TestCase):
    def test_get_name_number(self):
        result = get_name_number(u"Men's Health №01(222)Цена!")
        self.assertEqual(result, (u"Men's Health", u"01", u"222"))

        result = get_name_number(u"Бомба с перцем №51(700)")
        self.assertEqual(result, (u"Бомба с перцем", u"51", u"700"))

        result = get_name_number(u"Жизнь(+16) №49(830)")
        self.assertEqual(result, (u"Жизнь(+16)", u"49", u"830"))

        result = get_name_number(
            u"Комсомольская правда / вторник /№13.12(20161213)")
        self.assertEqual(
            result,
            (u"Комсомольская правда / вторник /", u"13.12", u"20161213"))

        result = get_name_number(u"Язмыш кочагы 11(01) НОВИНКА!")
        self.assertEqual(result, (u"Язмыш кочагы", u"11", u"01"))

        result = get_name_number(
            u"Попугай / спец №11(108) Пухлый попугай спец Свежие сканворды")
        self.assertEqual(result, (u"Попугай / спец", u"11", u"108"))

        result = get_name_number(u"Космополитен / мини формат /№01(173)")
        self.assertEqual(result,
                         (u"Космополитен / мини формат /", u"01", u"173"))

        result = get_name_number(
            u"Оракул / спец / Таинственные истории №26(97) Цена!")
        self.assertEqual(
            result,
            (u"Оракул / спец / Таинственные истории", u"26", u"97"))

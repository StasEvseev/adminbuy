# coding:utf-8

import datetime
import os


def rus_to_eng(text):
    if text:
        symbols = (
            u"абвгдеёжзийклмнопрстуфхцчшщъыьэюяАБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬ"
            u"ЭЮЯ",
            u"abvgdeejzijklmnoprstufhzcss_y_euaABVGDEEJZIJKLMNOPRSTUFHZCSS_Y_"
            u"EUA")
        tr = dict([(ord(a), ord(b)) for (a, b) in zip(*symbols)])
        try:
            return text.translate(tr)  # looks good
        except TypeError as exc:
            return text


def get_date(part):
    from dateutil import parser
    for par in part._headers:
        name, value = par
        if name == "Date":
            return parser.parse(value)
    return datetime.datetime.now()


def get_title(part):
    from applications.mails.action import decode
    for par in part._headers:
        name, value = par
        if name == "Subject":
            return decode(value)
    return ""


def get_from(part):

    for p in part._headers:
        name, value = p
        if name == "From":
            num_begin = value.find("<") + 1
            num_end = value.find(">")
            return value[num_begin:num_end]
    return ""


def get_to(part):
    for p in part._headers:
        name, value = p
        if name == "To":
            return value

    return ""


def get_cont_type_file(part):
    num_end = part._headers[0][1].find(';')
    cont_t = part._headers[0][1][:num_end]

    return cont_t


def name_for_file(part, path):
    """
    Генерация имени для файла(без корреляции).
    """
    from applications.mails.action import decode
    cont_t = get_cont_type_file(part)
    filename = decode(part.get_filename())
    ext = ''
    if '.' in filename:
        filename, ext = filename[:filename.find('.')], \
                        filename[filename.find('.'):]
    filename = rus_to_eng(filename)
    date_ = datetime.datetime.now()
    result = 'nakl_%s_%s' % (filename, date_.strftime('%d%m%Y'))
    result = ''.join([result, ext])
    if os.path.isfile(os.path.join(path, result)):
        result = ''.join(['(%s)' % id(path), result])

    return result

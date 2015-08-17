#coding:utf-8
import datetime
import os


def rus_to_eng(text):
    if text:
        symbols = (u"абвгдеёжзийклмнопрстуфхцчшщъыьэюяАБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ",
                   u"abvgdeejzijklmnoprstufhzcss_y_euaABVGDEEJZIJKLMNOPRSTUFHZCSS_Y_EUA")
        tr = dict( [ (ord(a), ord(b)) for (a, b) in zip(*symbols) ] )
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
            # values = parsedate_tz(value)
            # year, m, d, H, M, S, _, __, ___, t = values
            # return datetime.datetime(year, m, d, H, M, S, 0, t)
            # return datetime.datetime.strptime(
            #     value, '%a, %d %b %Y %H:%M:%S %Z')
    return datetime.datetime.now()


def get_title(part):
    from applications.mails.action import decode
    from email.header import decode_header
    for par in part._headers:
        name, value = par
        if name == "Subject":
            return decode(value)
    # subject, _ = decode_header(part._headers[5][1])[0]
    return ""


def get_from(part):
    # num_begin = part._headers[6][1].find('<') + 1
    # num_end = part._headers[6][1].find('>')

    for p in part._headers:
        name, value = p
        if name == "From":
            num_begin = value.find("<") + 1
            num_end = value.find(">")
            return value[num_begin:num_end]
    return ""

    # return part._headers[6][1][num_begin:num_end]


def get_to(part):
    for p in part._headers:
        name, value = p
        if name == "To":
            return value
    # num_begin = part._headers[7][1].find('<') + 1
    # num_end = part._headers[7][1].find('>')

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
        filename, ext = filename[:filename.find('.')], filename[filename.find('.'):]
    filename = rus_to_eng(filename)
    date_ = datetime.datetime.now()
    result = 'nakl_%s_%s' % (filename, date_.strftime('%d%m%Y'))
    # if cont_t == 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet':
    result = ''.join([result, ext])
    if os.path.isfile(os.path.join(path, result)):
        result = ''.join(['(%s)' % id(path), result])

    return result
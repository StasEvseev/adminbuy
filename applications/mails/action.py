# coding:utf-8

from email.header import decode_header

import imaplib
import email as email_module
import os
from collections import namedtuple

from applications.mails.helper import (get_title, get_date, get_from, get_to,
                                       name_for_file, rus_to_eng)
from config import (mail_folder, user_imap, user_pass, imap_server,
                    DIR_PROJECT, PATH_TO_GENERATE_INVOICE, PATH_WEB)


detach_dir = '.'

DIR_ATTACH = os.path.join(DIR_PROJECT, mail_folder)


class ProjectException(Exception):
    pass


class NotConnect(ProjectException):
    pass


class NotMails(ProjectException):
    pass


MailObject = namedtuple('MailObject',
                        ['title', 'date_', 'from_', 'to_', 'file_'])
MailObjectNew = namedtuple('MailObjectNew',
                           ['title', 'date_', 'from_', 'to_', 'files', 'text'])


def get_mail(mail, search_str):
    mail.list()
    mail.select('inbox')
    result, data = mail.search(None, *search_str)
    return result, data


def get_count_mails(email):
    """
    функция получения количества новых писем
    """
    m, l_ids = get_ids_mails(email)
    return len(l_ids)


def get_ids_mails(email):
    """
    Получение идентификаторов непрочитанных писем от некоего отправителя
    """
    try:
        mail = imaplib.IMAP4_SSL(imap_server)
        mail.login(user_imap, user_pass)
    except Exception as err:
        raise NotConnect(u'Нет соединения с сервером. Проверьте подключение.')
    else:
        search_str = ['UnSeen', ]
        # if from_imap:
        from_str = '(FROM "%s")' % email
        search_str.append(from_str)
        result, data = get_mail(mail, search_str)

        ids = data[0]  # data is a list.
        id_list = ids.split()

    return mail, id_list


class MailHepls(object):
    @classmethod
    def get_mails(cls, emails):
        """
        Получение всех непрочитанных писем от некоего отправителя
        """

        results = {}

        if not os.path.exists(PATH_TO_GENERATE_INVOICE):
            os.makedirs(DIR_ATTACH)

        mail = None
        try:
            for email in emails:
                results[email] = []
                mail, ids = get_ids_mails(email)
                for id in ids:
                    result, data = mail.fetch(id, "(RFC822)")
                    if data[0] is not None:
                        raw_email = data[0][1]

                        pmail = email_module.message_from_string(raw_email)
                        try:
                            mail_item = files_imap(pmail)
                        except Exception:
                            raise
                        results[email].append(mail_item)
        finally:
            if mail:
                mail.close()
                mail.logout()

        return ids, results


def mark_as_unseen(ids):
    """
    Помечаем письма с ids как непросмотренные
    """
    try:
        mail = imaplib.IMAP4_SSL(imap_server)
        mail.login(user_imap, user_pass)
    except Exception as err:
        raise NotConnect(u'Нет соединения с сервером. Проверьте подключение.')
    else:
        mail.select('inbox')
        for id in ids:
            mail.store(id, '-FLAGS', '\Seen')
        mail.close()
        mail.logout()


def decode(str):
    if str and str.startswith("=?UTF"):
        return decode_header(str)[0][0]
    if str and str[:14] in ["=?Windows-1251", '=?windows-1251']:
        return decode_header(str)[0][0].decode("windows-1251")
    return str


def files_imap(pmail):
    title = get_title(pmail)
    date_ = get_date(pmail)
    from_ = get_from(pmail)
    to_ = get_to(pmail)

    text = ""
    files = []

    # body = email.message_from_file(pmail)

    for part in pmail.walk():

        if (part.get_content_maintype() == "text" and
                part.get_content_type() == "text/plain"):
            text = part.get_payload(decode=True)
            try:
                text = text.decode("windows-1251")
            except UnicodeEncodeError:
                pass

        if part.get_content_maintype() == 'multipart':
            continue

        if part.get('Content-Disposition') is None:
            continue

        filename = decode(part.get_filename())
        filename = rus_to_eng(filename)

        print "FIND FILE - ", filename

        if bool(filename):
            filename = name_for_file(part, PATH_TO_GENERATE_INVOICE)
            filepath = os.path.join(PATH_TO_GENERATE_INVOICE, filename)
            link = os.path.join(PATH_WEB, filename)

            if not os.path.isfile(filepath):
                print filename

            fp = open(filepath, 'wb')
            fp.write(part.get_payload(decode=True))
            fp.close()
            files.append({'name': filename, 'path': filepath, 'link': link})

    m = MailObjectNew(title=title, date_=date_, from_=from_, to_=to_,
                      files=files, text=text)

    return m


def file_imap(pmail):
    """
    Получение объекта письма.
    """
    title = get_title(pmail)
    date_ = get_date(pmail)
    from_ = get_from(pmail)
    to_ = get_to(pmail)

    for part in pmail.walk():
        if part.get_content_maintype() == 'multipart':
            continue
        if part.get('Content-Disposition') is None:
            continue
        filename = decode(part.get_filename())
        print "FIND FILE - ", filename
        if bool(filename):
            filename = name_for_file(part, DIR_ATTACH)
            filepath = os.path.join(DIR_ATTACH, filename)
            if not os.path.isfile(filepath):
                print filename
            fp = open(filepath, 'wb')
            fp.write(part.get_payload(decode=True))
            fp.close()

            m = MailObject(title=title, date_=date_, from_=from_, to_=to_,
                           file_=filepath)

            return m

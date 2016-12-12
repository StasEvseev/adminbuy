# coding:utf-8

from collections import namedtuple

import email as emaillib
import imaplib

import os


from .helper import (get_title, get_date, get_from, get_to, name_for_file,
                     rus_to_eng, decode)
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


LetterModel = namedtuple(
    'MailObject', ['title', 'date_', 'from_', 'to_', 'file_'])
NewLetterModel = namedtuple(
    'MailObjectNew', ['title', 'date_', 'from_', 'to_', 'files', 'text'])


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
        imap_connection = imaplib.IMAP4_SSL(imap_server)
        imap_connection.login(user_imap, user_pass)
    except Exception as err:
        raise NotConnect(u'Нет соединения с сервером. Проверьте подключение.')
    else:
        search_str = ['UnSeen', ]
        # if from_imap:
        from_str = '(FROM "%s")' % email
        search_str.append(from_str)
        result, data = get_mail(imap_connection, search_str)

        ids = data[0]  # data is a list.
        id_list = ids.split()

    return imap_connection, id_list


class EmailProvider(object):
    @classmethod
    def fetch_letters(cls, sender_emails):
        """
        Получение всех непрочитанных писем от некоего отправителя
        """

        results = {}

        if not os.path.exists(PATH_TO_GENERATE_INVOICE):
            os.makedirs(DIR_ATTACH)

        imap_connection = None
        try:
            for email in sender_emails:
                results[email] = []
                imap_connection, ids = get_ids_mails(email)

                for id in ids:
                    result, data = imap_connection.fetch(id, "(RFC822)")

                    if data[0] is not None:
                        raw_data = data[0][1]

                        message_object = emaillib.message_from_string(raw_data)
                        try:
                            letter = parse_letter(message_object)
                        except Exception:
                            raise

                        results[email].append(letter)
        finally:
            if imap_connection:
                imap_connection.close()
                imap_connection.logout()

        return ids, results


def mark_as_unseen(ids):
    """
    Помечаем письма с ids как непросмотренные
    """
    try:
        imap_connection = imaplib.IMAP4_SSL(imap_server)
        imap_connection.login(user_imap, user_pass)
    except Exception:
        raise NotConnect(u'Нет соединения с сервером. Проверьте подключение.')

    imap_connection.select('inbox')
    for id in ids:
        imap_connection.store(id, '-FLAGS', '\Seen')

    imap_connection.close()
    imap_connection.logout()


def parse_letter(pmail):
    title = get_title(pmail)
    date_ = get_date(pmail)
    from_ = get_from(pmail)
    to_ = get_to(pmail)

    text = ""
    files = []

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

    m = NewLetterModel(
        title=title, date_=date_, from_=from_, to_=to_, files=files, text=text)

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

            m = LetterModel(
                title=title, date_=date_, from_=from_, to_=to_, file_=filepath)

            return m

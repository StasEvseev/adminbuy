# coding: utf-8
from tasks.instance import celery

__author__ = 'StasEvseev'


@celery.task
def run_every_minute():
    # from mailmodule import send_mail_async
    # r = redis.StrictRedis(host='localhost', port=6379, db=0)
    print "PUBLISH"
    # r.publish("sms_replies", "%s %s" % ("BLA", "BLA"))
    # send_mail_async(u"1", u"2")
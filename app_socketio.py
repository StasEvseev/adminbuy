# coding: utf-8

from flask import Flask
from flask.ext.socketio import SocketIO, join_room

__author__ = 'StasEvseev'


app = Flask(__name__)

socketio = SocketIO(app)

cnt = 0


@socketio.on('connect')
def test_connect(message):
    join_room('1')
    print "CONNECT"


@socketio.on('disconnect')
def test_disconnect():
    print('Client disconnected')


def redis_thread():
    import redis
    from datetime import datetime
    global cnt
    cnt += 1

    r = redis.StrictRedis(host="localhost", port=6379, db=0)
    r = r.pubsub()
    r.subscribe("sms_replies")

    r.subscribe("mail_handle")

    print "SUBSCRIBE"
    while True:
        for m in r.listen():
            if m['channel'] == "mail_handle":
                socketio.emit('mail handle', {
                    'id': int(m['data'])
                }, room='1')
            else:
                socketio.emit('new mail', {
                    'data': "Содержание %s" % cnt,
                    'date': datetime.now().strftime("%H:%M:%S"),
                    'title': 'Письмо №%s' % cnt,
                    'image': '',
                    'is_new': True
                }, room='1')


def wr(fnc):
    """
    Оборачиваем запуск сервера - запускаем тред для редиса.
    """
    def f(*args, **kwargs):
        import threading
        t = threading.Thread(target=redis_thread)
        t.daemon = True
        t.start()
        return fnc(*args, **kwargs)
    return f


from socketio.sgunicorn import NginxGeventSocketIOWorker
NginxGeventSocketIOWorker.run = wr(NginxGeventSocketIOWorker.run)

if __name__ == "__main__":
    socketio.run(app, port=8100)

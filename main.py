
#-*-coding: utf-8-*-

# Version: 0.1
# Author: Anson Tang <anson.tkg@gmail.com>
# License: Copyright(c) 2015 Anson.Tang
# Summary: 
from datetime import datetime

import tornado.websocket
import tornado.ioloop
import tornado.web
import socket

'''
This is a simple websocket echo server that uses the Tornado websocket handler.
Please run 'pip install tornado' with python of version 2.7.9 or greater to install tornado.
This program will echo back the reverse of whatever it recives.
Messages are output to the terminal for debuggin purposes.
'''

def get_date():
    dt = datetime.now()
    return dt.strftime("%Y-%m-%d %H:%M:%S %f")

clients = dict()

class IndexHandler(tornado.web.RequestHandler):
    @tornado.web.asynchronous
    def get(self):
        self.render("index.html")

class WSHandler(tornado.websocket.WebSocketHandler):
    def open(self):
        self.uid = self.get_argument("uid")
        print "New User(%s) Connection..."%self.uid
        clients[self.uid] = {'uid':self.uid, 'object':self}

    def send_message(self, uid, obj, message):
        msg = uid + get_date() + '  ' + message[::-1] + '\n\n'
        print '[message back message] uid(%s): %s.' % (uid, msg)
        obj.write_message(msg)

    def on_message(self, message):
        print 'message received: %s.' % message
        index = message.find(':')
        flag = message[:index]
        if flag == "send":
            self.send_message(self.uid, self, message[index+1:])
        elif flag == "sendtoall":
            for uid in clients.iterkeys():
                self.send_message(uid, clients[uid]['object'], message[index+1:])

    def on_close(self):
        print 'connection closed...'
        if self.uid in clients:
            del clients[self.uid]

    def check_origin(self, origin):
        return True

if __name__ == "__main__":
    app = tornado.web.Application([
        (r'/', IndexHandler),
        (r'/ws', WSHandler),
        ])
    app.listen(8888)
    myIP = socket.gethostbyname(socket.gethostname())
    print '*** websocket server started at %s ***'% myIP
    tornado.ioloop.IOLoop.instance().start()

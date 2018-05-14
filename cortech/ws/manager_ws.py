import logging
import json

LOGGER = logging.getLogger(__name__)


class SocketManager():

    def __init__(self):
        self.sockets = {}

    def register(self, _id, socket):
        self.sockets[_id] = socket

    def unregister(self, _id):
        self.sockets.pop(_id)

    def notify(self, msg):
        for _id in self.sockets:
            socket = self.sockets[_id]
            msg = msg['fullDocument']
            msg.pop('_id')
            print(msg)
            print(type(msg))
            print('****')
            socket.write_message(msg)

    # def check_origin(self, origin):
    #     return True
    #
    # def open(self):
    #     print('holiwi')
    #     self.write_message("connection opened")
    #     listeners = self.application.listeners
    #     self.application.listeners.append(self)
    #
    # @classmethod
    # def notify(self, values):
    #     for socket in self.application.listeners:
    #         socket.write(values)
    #
    # @classmethod
    # def update_cache(cls, change):
    #     cls.cache.append(change)
    #     if len(cls.cache) > cls.cache_size:
    #         cls.cache = cls.cache[-cls.cache_size:]
    #
    # @classmethod
    # def send_change(cls, change):
    #     change_json = json_util.dumps(change)
    #     print("size listeners: " + str(len(cls.listeners)))
    #     for waiter in cls.listeners:
    #         try:
    #             waiter.write_message(change_json)
    #             print("sending changes....")
    #         except Exception:
    #             print("Error sending message")
    #             # logging.error("Error sending message", exc_info=True)
    #
    # @classmethod
    # def on_change(cls, change):
    #     print("got change of type '%s'", change.get('operationType'))
    #     # logging.info("got change of type '%s'", change.get('operationType'))
    #
    #     # Each change notification has a binary _id. Use it to make an HTML
    #     # element id, then remove it.
    #     html_id = urlsafe_b64encode(change['_id']['_data']).decode().rstrip(
    #               '=')
    #     change.pop('_id')
    #     change['html'] = '<div id="change-%s"><pre>%s</pre></div>' % (
    #         html_id,
    #         tornado.escape.xhtml_escape(pformat(change)))
    #
    #     change['html_id'] = html_id
    #     print("Sending Change ... ")
    #     MongoSocket.send_change(change)
    #     print("Updating Change ... ")
    #     MongoSocket.update_cache(change)

from tornado import websocket
from bson import json_util
from base64 import urlsafe_b64encode
import tornado.escape
from pprint import pformat
import uuid
import logging

LOGGER = logging.getLogger(__name__)


class MainSocket(websocket.WebSocketHandler):
    """Handles long polling communication between xterm.js and server."""

    def initialize(self, close_future=None):
        """Base class initialization."""
        self.close_future = close_future

    def check_origin(self, origin):
        return True

    def open(self):
        """Open a Websocket associated to a console."""
        self.id = str(uuid.uuid4())
        LOGGER.info("WebSocket opened: {0}".format(self.id))
        self.application.manager.register(self.id, self)
        LOGGER.info("TTY On!")

    def on_close(self):
        """Close console communication."""
        LOGGER.info('TTY Off!')
        LOGGER.info("WebSocket closed: {0}".format(self.id))
        self.application.manager.unregister(self.id)
        if self.close_future is not None:
            self.close_future.set_result(("Done!"))

    def on_message(self, message):
        """Execute a command on console."""
        LOGGER.info(message)
# class MongoSocket(websocket.WebSocketHandler):
#     listeners = []
#     cache = []
#     cache_size = 10
#
#     def check_origin(self, origin):
#         return True
#
#     def open(self):
#         print('holiwi')
#         self.write_message("connection opened")
#         listeners = self.application.listeners
#         self.application.listeners.append(self)
#
#     @classmethod
#     def notify(self, values):
#         for socket in self.application.listeners:
#             socket.write(values)
#
#     @classmethod
#     def update_cache(cls, change):
#         cls.cache.append(change)
#         if len(cls.cache) > cls.cache_size:
#             cls.cache = cls.cache[-cls.cache_size:]
#
#     @classmethod
#     def send_change(cls, change):
#         change_json = json_util.dumps(change)
#         print("size listeners: " + str(len(cls.listeners)))
#         for waiter in cls.listeners:
#             try:
#                 waiter.write_message(change_json)
#                 print("sending changes....")
#             except Exception:
#                 print("Error sending message")
#                 # logging.error("Error sending message", exc_info=True)
#
#     @classmethod
#     def on_change(cls, change):
#         print("got change of type '%s'", change.get('operationType'))
#         # logging.info("got change of type '%s'", change.get('operationType'))
#
#         # Each change notification has a binary _id. Use it to make an HTML
#         # element id, then remove it.
#         html_id = urlsafe_b64encode(change['_id']['_data']).decode().rstrip(
#                   '=')
#         change.pop('_id')
#         change['html'] = '<div id="change-%s"><pre>%s</pre></div>' % (
#             html_id,
#             tornado.escape.xhtml_escape(pformat(change)))
#
#         change['html_id'] = html_id
#         print("Sending Change ... ")
#         MongoSocket.send_change(change)
#         print("Updating Change ... ")
#         MongoSocket.update_cache(change)

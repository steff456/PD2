from tornado import websocket


class MongoSocket(websocket.WebSocketHandler):

    def open(self):
        self.application.listeners.append(self)

    @classmethod
    def notify(self, values):
        for socket in self.application.listeners:
            socket.write(values)

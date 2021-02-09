import asyncio
import json
import time

from autobahn.asyncio.websocket import WebSocketServerProtocol, \
    WebSocketServerFactory


class Server(WebSocketServerProtocol):
    """

        Class containing all the custom log for the websocket server

        """

    @staticmethod
    def get_timestamp():
        """

        Returns the current unix timestamp of the server

        :return: current unix timestamp of the server
        :rtype: int

        """
        return int(time.time())

    def get_event(self, c):
        """

        Creates a JSON string containing the message count and the current timestamp

        :param c: The message count
        :type c: int
        :return: A JSON string containing the message count and the current timestamp
        :rtype: string

        """

        return json.dumps({"c": c, "ts": self.get_timestamp()})

    def notify(self, c, isBinary):
        """

        Send a connected client an event JSON string

        :param c: The message count
        :type c: int
        :return: void

        """
        message = self.get_event(c)
        self.sendMessage(str.encode(message), isBinary)

    def onConnect(self, request):
        '''

        Event triggered whenever there is a new connection incoming to the server

        :param request: Information on the client wishing to connect
        :type request: autobahn.websocket.types.TransportDetails
        :return: void
        '''
        print("Client connecting: {0}".format(request.peer))

    def onOpen(self):
        '''

        Event triggered whenever a new client successfully establishes a connection to the server

        :return: void
        '''
        print("WebSocket connection open.")
        self.notify(0, False)

    def onMessage(self, payload, isBinary):
        '''

        Event triggered whenever an incoming message is received by the server

        :param payload: the message being received
        :type payload: bytes
        :param isBinary: whether the incoming message is in binary format
        :type isBinary: bool
        :return:
        '''
        # decode incoming message into an associative array
        data = json.loads(payload)

        # notify client with event for message with count "c"
        self.notify(data["c"], isBinary)

    def onClose(self, wasClean, code, reason):
        '''

        Event triggered whenever a connection between the server and a client is closed

        :param wasClean: Whether the WebSocket connection was closed cleanly.
        :type wasClean: bool
        :param code: Close status code as sent by the WebSocket peer.
        :type code: int
        :param reason: Close reason as sent by the WebSocket peer.
        :type reason: string
        :return: void
        '''
        print("WebSocket connection closed: {0}".format(reason))

"""

Initializes the websocket server
Sets the callback function, host, and port,
as well as starts the loop the server runs in

"""
if __name__ == '__main__':
    factory = WebSocketServerFactory("ws://127.0.0.1:8080")
    factory.protocol = Server

    loop = asyncio.get_event_loop()
    coro = loop.create_server(factory, '0.0.0.0', 8080)
    server = loop.run_until_complete(coro)

    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.close()
        loop.close()
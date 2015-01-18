__author__ = 'Eric Ahn'

from twisted.internet.protocol import Factory
from twisted.protocols.basic import LineReceiver
from twisted.internet import reactor

class SocketServer(LineReceiver):

    def lineReceived(self, data):
        print repr(data)

    def connectionMade(self):
        print 'RPi connected'

    def connectionLost(self, reason):
        print 'RPi disconnected'

class SocketServerFactory(Factory):

    protocol = SocketServer

def main():
    reactor.listenTCP(8000, SocketServerFactory())
    reactor.run()

if __name__ == '__main__':
    main()
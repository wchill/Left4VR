__author__ = 'Eric Ahn'

from twisted.internet import reactor
from twisted.internet.protocol import Factory
from twisted.internet.serialport import SerialPort
from twisted.protocols.basic import LineReceiver

putter = None

class SerialClient(LineReceiver):

    def lineReceived(self, line):
        # print repr(line)
        if putter is not None:
            putter.message(line)

class SocketClient(LineReceiver):

    def __init__(self):
        global putter
        putter = self

    def connectionMade(self):
        print 'Connected to PC'

    def connectionLost(self, reason):
        print 'Disconnected from PC'
        reactor.stop()

    def lineReceived(self, data):
        print repr(data)

    def message(self, message):
        # print repr(message)
        self.transport.write(message + '\n')

class SocketFactory(Factory):

    protocol = SocketClient

if __name__ == '__main__':
    f = SocketFactory()
    reactor.connectTCP("192.168.137.1", 8000, f)
    SerialPort(SerialClient(), '/dev/ttyAMA0', reactor, baudrate='9600')
    reactor.run()
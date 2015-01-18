__author__ = 'Eric Ahn'

from twisted.internet import reactor
from twisted.internet.protocol import Factory, ClientFactory, Protocol
from twisted.internet.serialport import SerialPort
from twisted.protocols.basic import LineReceiver
import RPi.GPIO as GPIO

putter = None
GPIO.setmode(GPIO.BCM)
GPIO.setup(13, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(19, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(26, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(5, GPIO.OUT)
GPIO.setup(6, GPIO.OUT)
GPIO.output(5, False)
GPIO.output(6, False)

class SerialClient(LineReceiver):

    def lineReceived(self, line):
        print repr(line)
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
        message += ' %d ' % 0 if GPIO.input(13) else 1
        message += '%d ' % 0 if GPIO.input(19) else 1
        message += '%d' % 1 if GPIO.input(26) else 0
        self.transport.write(message + '\r\n')

class SocketFactory(ClientFactory):

    protocol = SocketClient

if __name__ == '__main__':
    f = SocketFactory()
    reactor.connectTCP("192.168.137.1", 8000, f)
    SerialPort(SerialClient(), '/dev/ttyAMA0', reactor, baudrate='115200')
    reactor.run()

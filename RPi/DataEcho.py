#!/usr/bin/python
__author__ = 'Eric Ahn'

from twisted.internet import reactor
from twisted.internet.protocol import ClientFactory
from twisted.protocols.basic import LineReceiver
import RPi.GPIO as GPIO


CONTROL_IP = '192.168.137.1'
SERVER_IP = ''

CROUCH_PIN = 13
SHOOT_PIN = 19
RELOAD_PIN = 26

GPIO.setmode(GPIO.BCM)
GPIO.setup(CROUCH_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(SHOOT_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(RELOAD_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
# ground pins 5 and 6
GPIO.setup(5, GPIO.OUT)
GPIO.setup(6, GPIO.OUT)
GPIO.output(5, False)
GPIO.output(6, False)

GPIO.setup(21, GPIO.OUT)
GPIO.output(21, False)

client = None
factory = None


class SocketClient(LineReceiver):

    def __init__(self):
        global client
        client = self
        self.crouch_state = False
        self.shoot_state = False
        self.reload_state = False 
        GPIO.add_event_detect(CROUCH_PIN, GPIO.BOTH, callback=event_crouch, bouncetime=50)
        GPIO.add_event_detect(SHOOT_PIN, GPIO.BOTH, callback=event_shoot, bouncetime=50)
        GPIO.add_event_detect(RELOAD_PIN, GPIO.BOTH, callback=event_reload, bouncetime=50)

    def connectionMade(self):
        print 'Connected to PC'

    def connectionLost(self, reason):
        print 'Disconnected from PC'
        reactor.stop()

    def lineReceived(self, data):
        print repr(data)

    def send_crouch(self, value):
        print 'crouch {0}'.format(value)
        if self.crouch_state != value:
            self.transport.write('C{0}\r\n'.format(1 if value else 0))
            self.crouch_state = value

    def send_shoot(self, value):
        if self.shoot_state != value:
            if value is False or self.reload_state is False:
                print 'shoot {0}'.format(value)
                self.transport.write('S{0}\r\n'.format(1 if value else 0))
                self.shoot_state = value
            else:
                print 'shoot blocked by unfinished reload'

    def send_reload(self, value):
        print 'reload {0}'.format(value)
        if self.reload_state != value:
            self.transport.write('R{0}\r\n'.format(1 if value else 0))
            self.reload_state = value


class GameClient(LineReceiver):

    def __init__(self):
        pass

    def connectionMade(self):
        print 'Connected to server'

    def connectionLost(self, reason):
        print 'Disconnected from server'
        reactor.stop()

    def lineReceived(self, data):
        if data[0] == 'C':
            print 'Client connected to server'
        elif data[0] == 'F':
            print 'Weapon fired'
            # haptic_feedback()
        else:
            print repr(data)


def event_crouch(channel):
    if client is not None:
        reactor.callFromThread(client.send_crouch, not GPIO.input(13))


def event_shoot(channel):
    if client is not None:
        reactor.callFromThread(client.send_shoot, not GPIO.input(19))


def event_reload(channel):
    if client is not None:
        reactor.callFromThread(client.send_reload, not not GPIO.input(26))


class SocketFactory(ClientFactory):

    def __init__(self):
        pass

    protocol = SocketClient


class GameFactory(ClientFactory):

    def __init__(self):
        pass

    protocol = GameClient

if __name__ == '__main__':
    factory = SocketFactory()
    reactor.connectTCP(CONTROL_IP, 8000, SocketFactory())
    # reactor.connectTCP(SERVER_IP, 50000, GameFactory())
    try:
        reactor.run()
    except KeyboardInterrupt:
        pass
    GPIO.cleanup()
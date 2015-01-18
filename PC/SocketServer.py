__author__ = 'Eric Ahn'

from twisted.internet.protocol import Factory
from twisted.protocols.basic import LineReceiver
from twisted.internet import reactor
import ctypes
import SendKeys

SendInput = ctypes.windll.user32.SendInput

# C struct redefinitions
PUL = ctypes.POINTER(ctypes.c_ulong)
class KeyBdInput(ctypes.Structure):
    _fields_ = [("wVk", ctypes.c_ushort),
                ("wScan", ctypes.c_ushort),
                ("dwFlags", ctypes.c_ulong),
                ("time", ctypes.c_ulong),
                ("dwExtraInfo", PUL)]

class HardwareInput(ctypes.Structure):
    _fields_ = [("uMsg", ctypes.c_ulong),
                ("wParamL", ctypes.c_short),
                ("wParamH", ctypes.c_ushort)]

class MouseInput(ctypes.Structure):
    _fields_ = [("dx", ctypes.c_long),
                ("dy", ctypes.c_long),
                ("mouseData", ctypes.c_ulong),
                ("dwFlags", ctypes.c_ulong),
                ("time",ctypes.c_ulong),
                ("dwExtraInfo", PUL)]

class Input_I(ctypes.Union):
    _fields_ = [("ki", KeyBdInput),
                 ("mi", MouseInput),
                 ("hi", HardwareInput)]

class Input(ctypes.Structure):
    _fields_ = [("type", ctypes.c_ulong),
                ("ii", Input_I)]

# Actuals Functions

def PressKey(hexKeyCode):
    extra = ctypes.c_ulong(0)
    ii_ = Input_I()
    ii_.ki = KeyBdInput( 0, hexKeyCode, 0x0008, 0, ctypes.pointer(extra) )
    x = Input( ctypes.c_ulong(1), ii_ )
    ctypes.windll.user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))

def ReleaseKey(hexKeyCode):
    extra = ctypes.c_ulong(0)
    ii_ = Input_I()
    ii_.ki = KeyBdInput( 0, hexKeyCode, 0x0008 | 0x0002, 0, ctypes.pointer(extra) )
    x = Input( ctypes.c_ulong(1), ii_ )
    ctypes.windll.user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))

user32 = ctypes.windll.user32

class SocketServer(LineReceiver):

    def __init__(self):
        self.shoot_event = False
        self.reload_event = False
        self.crouch_event = False
        self.use_event = False

    def lineReceived(self, data):
        # print repr(data)
        event = data.split(' ')

        if int(event[0], 16) < 48 and int(event[1], 16) < 48:
            PressKey(0x12)
            self.use_event = True
        elif self.use_event:
            self.use_event = False
            ReleaseKey(0x12)

        if event[3] == '1':
            PressKey(0x1D)
            self.crouch_event = True
        elif self.crouch_event:
            self.crouch_event = False
            ReleaseKey(0x1D)

        if event[4] == '1':
            user32.mouse_event(0x0002, 0, 0, 0, 0) # press left
            self.shoot_event = True
        elif self.shoot_event:
            self.shoot_event = False
            user32.mouse_event(0x0004, 0, 0, 0, 0) # release left

        if event[5] == '1' and self.reload_event == False:
            SendKeys.SendKeys('R')
            self.reload_event = True
        elif event[5] == '0':
            self.reload_event = False

    def connectionMade(self):
        print 'RPi connected'
        self.transport.write('lol\r\n')

    def connectionLost(self, reason):
        print 'RPi disconnected'
        user32.mouse_event(0x0004, 0, 0, 0, 0)
        self.shoot_event = False
        ReleaseKey(0x1D)
        self.crouch_event = False
        ReleaseKey(0x12)
        self.use_event = False

class SocketServerFactory(Factory):

    protocol = SocketServer

def main():
    reactor.listenTCP(8000, SocketServerFactory())
    reactor.run()

if __name__ == '__main__':
    main()
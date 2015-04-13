__author__ = 'Eric Ahn'

from twisted.internet.protocol import Factory
from twisted.protocols.basic import LineReceiver
from twisted.internet import reactor
import ctypes
import SendKeys
from win32gui import GetWindowText, GetForegroundWindow
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
        self.reload_event = False
        self.use1 = False
        self.use2 = False
        self.events = {}

    def lineReceived(self, data):

        if GetWindowText(GetForegroundWindow()) == 'Left 4 Dead 2':

            # switch weapons
            if data[0] == 'C':
                if data[1] == '1':
                    user32.mouse_event(0x0800, 0, 0, -120, 0)

            # shoot
            elif data[0] == 'S':
                if data[1] == '1':
                    user32.mouse_event(0x0002, 0, 0, 0, 0) # press left
                else:
                    user32.mouse_event(0x0004, 0, 0, 0, 0) # release left

            # reload
            elif data[0] == 'R':
                if data[1] == '1' and self.reload_event == False:
                    SendKeys.SendKeys('R')
                    self.reload_event = True
                elif data[1] == '0':
                    self.reload_event = False

            # press key
            elif data[0] == 'K':
                if data[1] == '+':
                    PressKey(ord(data[2]))
                elif data[1] == '-':
                    ReleaseKey(ord(data[2]))

            # melee shove
            elif data[0] == 'M':
                if data[1] == '1':
                    user32.mouse_event(0x0008, 0, 0, 0, 0) # press right
                else:
                    user32.mouse_event(0x0010, 0, 0, 0, 0) # release right

            # glove event
            elif data[0] == 'G':
                if data[1] == '1':
                    self.use1 = not not int(data[2])
                else:
                    self.use2 = not not int(data[2])
                if self.use1 and self.use2:
                    PressKey(0x12)
                else:
                    ReleaseKey(0x12)

    def connectionMade(self):
        peer = self.transport.getPeer()
        print 'Client {0}:{1} connected'.format(peer.host, peer.port)
        self.transport.write('lol\r\n')

    def connectionLost(self, reason):
        peer = self.transport.getPeer()
        print 'Client {0}:{1} disconnected'.format(peer.host, peer.port)
        user32.mouse_event(0x0004, 0, 0, 0, 0)
        user32.mouse_event(0x0010, 0, 0, 0, 0)
        #self.shoot_event = False
        ReleaseKey(0x1D)
        #self.crouch_event = False
        ReleaseKey(0x12)
        #self.use_event = False

class SocketServerFactory(Factory):

    protocol = SocketServer

def main():
    reactor.listenTCP(8000, SocketServerFactory())
    reactor.run()

if __name__ == '__main__':
    main()
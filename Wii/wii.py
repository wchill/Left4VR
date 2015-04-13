def press(key):
	sock.send('K+{0}\r\n'.format(chr(key)))

def release(key):
	sock.send('K-{0}\r\n'.format(chr(key)))

def nunchuckUpdate():
    global last_x, last_y, last_space, last_crouch
    # Nunchuck stick update
    y = wiimote[0].nunchuck.stick.y
    x = wiimote[0].nunchuck.stick.x

    if y >= stickDeadZone and last_y != 1:
        last_y = 1
        press(0x11)
        release(0x1F)
    elif y <= -stickDeadZone and last_y != -1:
        last_y = -1
        press(0x1F)
        release(0x11)
    elif y < stickDeadZone and y > -stickDeadZone and last_y != 0:
        last_y = 0
        release(0x11)
        release(0x1F)

    if x >= stickDeadZone and last_x != 1:
        last_x = 1
        release(0x1E)
        press(0x20)
    elif x <= -stickDeadZone and last_x != -1:
        last_x = -1
        press(0x1E)
        release(0x20)
    elif x < stickDeadZone and x > -stickDeadZone and last_x != 0:
        last_x = 0
        release(0x1E)
        release(0x20)

    if wiimote[0].nunchuck.buttons.button_down(NunchuckButtons.C) and not last_space:
        last_space = True
        press(0x39)
    elif not wiimote[0].nunchuck.buttons.button_down(NunchuckButtons.C) and last_space:
        last_space = False
        release(0x39)

    if wiimote[0].nunchuck.buttons.button_down(NunchuckButtons.Z) and not last_crouch:
        last_crouch = True
        press(0x1D)
    elif not wiimote[0].nunchuck.buttons.button_down(NunchuckButtons.Z) and last_crouch:
        last_crouch = False
        release(0x1D)

if starting:
    system.setThreadTiming(TimingTypes.HighresSystemTimer)
    system.threadExecutionInterval = 2

    import socket
    import struct

    global sock, last_x, last_y, last_space, last_crouch, address
    address = '192.168.137.1'
    last_x = 0
    last_y = 0
    last_space = False
    last_crouch = False
    sock = socket.create_connection((address, 8000))
    sock.setblocking(0)

    # 40 seems to be a good balance after some experimentation
    stickDeadZone = 40

    wiimote[0].nunchuck.update += nunchuckUpdate
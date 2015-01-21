# Use in FreePIE

def nunchuckUpdate():
   # Nunchuck stick update
   y = wiimote[0].nunchuck.stick.y
   x = wiimote[0].nunchuck.stick.x
   
   keyboard.setKey(Key.W, (y >= stickDeadZone))
   keyboard.setKey(Key.S, (y <= -stickDeadZone))
   keyboard.setKey(Key.D, (x >= stickDeadZone))
   keyboard.setKey(Key.A, (x <= -stickDeadZone))

   # Nunchuck C Z buttons
   # Assign C button to jump
   keyboard.setKey( Key.Space, wiimote[0].nunchuck.buttons.button_down(NunchuckButtons.C) )
   # Assign Z button to next weapon (note that this requires remapping next weapon to the I key)
   keyboard.setKey( Key.I, wiimote[0].nunchuck.buttons.button_down(NunchuckButtons.Z) )


if starting:
   system.setThreadTiming(TimingTypes.HighresSystemTimer)
   system.threadExecutionInterval = 2

   # 40 seems to be a good balance after some experimentation
   stickDeadZone = 40

   # wiimote[0].buttons.update += wiimoteButtonUpdates
   wiimote[0].nunchuck.update += nunchuckUpdate
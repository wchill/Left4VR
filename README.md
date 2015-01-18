# Left 4 Virtual Reality
Immersive VR Friendly Controls for First Person Shooter Games
![Final Hackathon Product](http://s3.amazonaws.com/challengepost/photos/production/solution_photos/000/200/219/datas/xlarge.png?1421591141)

```
this is a hackathon project for MHacks V
http://mhacksv.challengepost.com/submissions/31657-left-4-virtual-reality
```

##The Idea

Most virtual reality experiences today are passive ones. We've all enjoyed Rift Coaster and the like, and these are promising first steps. But the promise of VR is *reality*… immersion. 

Or project is another step in the direction of immersion. We largely have two components to our product - a glove and a nerf gun. Both of these components are fitted with enough sensors to let you forget that you're using a controller and let you focus instead on surviving in the zombie infested world of Left 4 Dead 2.

This project is built with a special focus on Left 4 Dead 2 as we understand that a good virtual reality experience requires accuracy and finesse just as much as it requires general functionality. In this regard, while our project will work with most first person shooter games, we have intentionally built it to be great for Left 4 Dead 2.


##Design
###The Armed Controller
The dominant controller for the project is the Armed Controller. It looks like a gun and use for this controller is clear enough: aiming down sights, firing, reloading, etc. It started off as an ordinary Nerf Rapidstrike, which we then gutted to make space for sensors and sensor feeds. We chose this model of the Nerf for its form factor (which is similar to most guns in fps games), its versatility (the collapsible stock, design and multiple tactical rails) and for its electrically controlled trigger system (most moving parts were electrically driven, not mechanically). All the preexisting sensors from the Rapidstrike feed into a Raspberry Pi which is mounted on the side of the gun. 
We’ve also removed the contents of what used to be battery compartment of the Rapidstrike and fitted a Nintendo Wii Remote and Nunchuk controller there. This controller is used to get information about the Armed Controller’s movements and to control movement within the game (walking, sprinting, control of an under-barrel attachment such as a flashlight, etc).
Power is supplied to the Armed Controller by the mounted Raspberry Pi, which in turn can be powered via Micro USB. We could therefore power this part of the project using a battery pack/wall adapter/similar. The Raspberry Pi is currently connected to our gaming computer using an Ethernet cable in the interest of maintaining low latency. We have support for Bluetooth as well, although the response times aren’t desirable (in the order of tens of milliseconds depending on the environment) and in an application like VR where fast response times are crucial, we found this to be an unacceptable compromise for our needs.

###The Unarmed Controller
Another major component of the build is the Unarmed Controller worn on the unarmed hand. It basically consists of a custom built glove controller and a Myo armband. This controller is to be used to perform most other gestures in the game. This includes (but not limited to) picking up items, using throwables, signaling fellow players, and interacting with fellow players and the environment.
There are two flex sensors and one pressure sensor in the glove that we use to read the state of the hand. These sensors are sampled at 100Hz and feed into an Arduino Pro Micro, which feeds data via UART to the Raspberry Pi on the side of the Armed Controller. The Myo feeds data directly to the gaming PC via Bluetooth.

###The Oculus
The Oculus Rift DK2 completes our set up by providing the visuals to the user as well as the ability to look around the world using its excellent head tracking.

##Limitations
We came close to the product we had originally envisioned, however there were a number of items that we did not have time to implement.
+ **Microsoft Kinect**: We wanted to use the Microsoft Kinect to watch the body’s posture to adjust for crouching, running, aiming down sights and the like. Unfortunately we were not able to do this because of the time restriction so we improvised and used the Nintendo Nunchuk Controllers instead.
+ **Wireless**: Moving around in VR space almost necessarily means we end up tangled in all the wires. We originally wanted to use wireless communications like Bluetooth, but we were unable to do that as we didn’t have enough time to reduce the response lag on Bluetooth to something suitable for VR. As a result, our project is a veritable mess of wires.

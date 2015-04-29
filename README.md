# Left 4 Virtual Reality
Immersive VR Friendly Controls for First Person Shooter Games

###At MHacks V
http://mhacksv.challengepost.com/submissions/31657-left-4-virtual-reality
https://www.youtube.com/watch?v=oh_zPe3Ard0

###At EOH 2015 
https://www.youtube.com/watch?v=bhYxKahUGq4


##Collaborators
| Name | GitHub | Personal |
|:------------- |:-------------:|:-----:|
| Abhishek Modi | https://github.com/modi95 |http://www.akmodi.com/|
| Andrew Kuznetsov | https://github.com/akuznets0v|http://www.andrewkuz.net/sov|
| Eric Ahn | https://github.com/wchill |http://intense.io/|
| Jimmy Guo| https://github.com/B1indfire||

![Our team](https://raw.githubusercontent.com/wchill/Left4VR/master/pics/Mhacks%20V%20Team.jpg)
![EOH Team](https://github.com/wchill/Left4VR/blob/master/pics/D7K_5535_Edit.JPG?raw=true)

##The Idea

Most virtual reality experiences today are passive ones. We've all enjoyed Rift Coaster and the like, and these are promising first steps. But the promise of VR is *reality*… immersion. 

Or project is another step in the direction of immersion. We largely have two components to our product - the Nerf gun and gesture controls. Both of these components are fitted with enough sensors to let you forget that you're using a controller and let you focus instead on surviving in the zombie infested world of Left 4 Dead 2.

![Final Hackathon Product](http://s3.amazonaws.com/challengepost/photos/production/solution_photos/000/200/219/datas/xlarge.png?1421591141)
![Version 2 at EOH](https://raw.githubusercontent.com/wchill/Left4VR/master/pics/EOH_2015.jpg)

This project is built with a special focus on Left 4 Dead 2 as we understand that a good virtual reality experience requires accuracy and finesse just as much as it requires general functionality. In this regard, while our project will work with most first person shooter games with some tweaking, we have intentionally decided to showcase it using Left 4 Dead 2 only. Left 4 Dead 2 was chosen because of its emphasis on cooperative play, meaning that one does not need to worry about trying to compete against very skilled keyboard + mouse users. It also provides a lot of room for using gestures in a comfortable, natural way. We are currently looking into porting this system to the Borderlands and Metro series.


##Design
###Armed Controller
The dominant controller for the project is the Armed Controller. It looks like a gun and use for this controller is clear enough: aiming down sights, firing, reloading, etc. It started off as an ordinary Nerf Rapidstrike, which we then gutted to make space for sensors and sensor feeds. We chose this model of the Nerf for its form factor (which is similar to most guns in fps games), its versatility (the collapsible stock, design and multiple tactical rails) and for its electrically controlled trigger system (most moving parts were electrically driven, not mechanically). All the preexisting switches from the Rapidstrike feed into a Raspberry Pi which is mounted on the side of the gun. There is also a switch that detects whether a magazine is inserted into the controller and a reload action is performed accordingly. 

We’ve also removed the contents of what used to be battery compartment of the Rapidstrike and fitted a Nintendo Wii Remote, MotionPlus and Nunchuck controller there. This controller is used to get information about the Armed Controller’s movements and to control movement within the game (walking, sprinting, control of an under-barrel attachment such as a flashlight, etc). These communicate directly with the PC via Bluetooth. The plan is to remove the Wii Remote completely from the equation and have the MotionPlus and Nunchuk interface with the Pi directly over I2C to reduce software complexity, power consumption and response time.

Power is supplied to the Armed Controller by the mounted Raspberry Pi, which in turn can be powered via Micro USB. We could therefore power this part of the project using a battery pack/wall adapter/similar - currently an off-the-shelf USB battery pack is used. The Raspberry Pi uses Wi-Fi to communicate with the gaming computer, with real-world latency around 2ms, but Ethernet is also an option if even lower latency is desired/needed. We have support for Bluetooth as well, although the response times using the Pi's USB stack aren’t desirable (in the order of tens of milliseconds depending on the environment) and in an application like VR where fast response times are crucial, we found this to be an unacceptable compromise for our needs.

###Gesture Controls
Another major component of the build is the gesture controls. Currently this consists of a custom-made glove worn on the left hand and a Myo gesture control armband on the right forearm. This is to be used to perform most other gestures in the game. This includes (but not limited to) picking up items, using throwables, signaling fellow players, and interacting with fellow players and the environment.

There are two flex sensors in the glove that we use to read the state of the hand. These sensors are sampled at 100Hz using a Spark Core, which feeds data via Wi-Fi to the PC. The Myo actually commmunicates with another computer using Bluetooth, then the data is processed using the myo-python library and transmitted over the network back to the PC. The plan is to remove this component and replace it with the IMUs in the Nunchuk/MotionPlus on the Armed Controller.

Currently we plan on improving the glove such that it has 5 flex sensors (one for each finger) and also conductive pads to allow extra gestures by touching fingertips together.

###The Oculus
The Oculus Rift DK2 completes our set up by providing the visuals to the user as well as the ability to look around the world using its excellent head tracking. In the initial version the Vireio Perception driver was used; however currently VorpX is being used.

###Software Stack
The software stack has undergone several iterations to improve code reusability and modularity. The goal is to make it simple to add any additional peripheral devices, supported games or keybindings that we want to use.

Currently much of the processing is done on the PC itself using a Python script. Using the Twisted async networking library, it listens on a socket for incoming connections and converts the incoming data into virtual input. Currently all actions are hardcoded, but code is currently being developed in order to modularize this so that event triggers/actions can be dynamically added by peripheral devices. There is no security; this may or may not be fixed in the future. Any peripheral devices that wish to control the host computer can simply open up a socket connection to the given address and port. This means that if one peripheral fails (due to power, mechanical failure, or some other reason), the rest of the system will remain running. This is a huge improvement over how the system was implemeneted at MHacks V, where everything had to be powered on in a certain order.

The Wii Remote/Nunchuk/MotionPlus, while they communicate via Bluetooth to the PC, do not directly control the script. They pass through another software layer - FreePIE, an input emulator which provides Python scripting functions to make use of popular controllers. Our FreePIE script also opens up a socket to the master script. If the gaming computer does not have Bluetooth, another computer like a laptop can instead run FreePIE, allowing some flexibility.

The configuration of the software stack also allows for other features beyond this project; for example, it would be possible to write a mobile app to turn a smartphone or tablet into a very capable gaming controller, or to use another computer's keyboard and mouse for remote control/gaming.

##Limitations
We came close to the product we had originally envisioned, however there were a number of items that we did not have time to implement or are not currently possible.
+ **Microsoft Kinect**: We wanted to use the Microsoft Kinect to watch the body’s posture to adjust for crouching, running, aiming down sights and the like. Unfortunately we were not able to do this because of the time restriction so we improvised and used the Nintendo Nunchuk Controllers instead.  
+ **Haptic feedback**: Adding in vibration motors into the Nerf gun would allow for more realistic feeling controls.  
+ **Reload enforcement**: In most games guns are reloaded automatically when the magazine is empty. Obviously we would like to disable this for greater realism. However currently this is not possible in most games. It can be accomplished in Left 4 Dead 2 using a server-side trick, but the animations will not look correct and it only works with Source-based multiplayer games.

## Problems encountered

#### Initial version
Because of the lack of native VR support in Left 4 Dead, we had to use a 3rd party driver called [Vireio Perception](http://www.mtbs3d.com/index.php?option=com_content&view=category&id=169&Itemid=490). This caused multiple issues:  
* ~~The Myo Control software would conflict with Perception as Perception was attempting to inject its own graphical DLLs into Myo Control, causing errors. This required launching our setup in a particular order (run Perception with admin privileges -> launch L4D -> close Perception -> launch Myo Control)~~ Using myo-python fixes this problem; in addition changes are being made to use the MotionPlus instead of the Myo.
* ~~Switching screens caused Left 4 Dead to crash on startup, complaining about "Failed to create D3D device!" Because this happened on-stage right before we were to present, we were unable to fix this issue in time. Cause (and solution) remains unknown.~~ No longer seems to be an issue on either Vireio or VorpX, most likely driver-related.  
* Mirroring the display on the Rift was nontrivial. ~~We had to use [Open Broadcaster Software](https://obsproject.com/), a tool that streamers normally use, to capture the video from Left 4 Dead so it could be displayed on an external monitor. Unfortunately, because of how Perception works, we didn't get a nice stereo view like you would expect, but instead we got one that seemed very jittery (likely because it was switching between left and right views quickly).~~ OBS no longer works. We now use a modified game server with a spectator plugin and another computer with another copy of Left 4 Dead 2 to do a visual preview. It does not show the HUD or any Rift-specific distortions and is not quite real-time, but it is better than using OBS.  
* The Oculus Rift had to be run in extended display mode as the primary monitor, making setting everything up an immense hassle because all our windows would show up on the Rift and there would be nothing on the desktop monitor.

#### Current version
We have now switched to VorpX after some improvements to our stack, which has its own problems unfortunately.
* ~~When an item pickup is visible, the level geometry may flash white.~~ No longer an issue in the latest version of VorpX
* Open Broadcaster Software no longer works using either Vireio or VorpX. For spectating, another machine is used along with a L4D2 server that allows spectating in coop mode. Obviously this is not a portable solution, but for Source-based games it is sufficient.

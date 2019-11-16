# Simpsons Shuffler 
*Short press of button will play random episode. Long press will shutdown pi*
*Button diagram and python script are in repository*

## This guide will walk you through building your own Simpsons Shuffler

About a year ago i was looking for cool raspberry pi projects to do. I stumbled across one that I immediately new 
I needed to build, The Simpsons Shuffler by Stephen Coyle. After hours of building and making the code he provided work for 
me and my needs (and a little help from Stephen himself) I had a Raspberry Pi Zero W that shuffles episodes of the simpsons on button push and ALSO safely turned off the pi on a long button press. 

I posted my project to reddit and have been recieving requests for help ever since. As it turns out, there is no step by step guide for this project, and none that include a power off feature. Until now!



### prerequisites
  - Cyberduck for mac (or whatever ftp software you prefer)
    *Filezilla for windows*
  - Applepi Baker (to add the image to sd card) for mac
    *Etcher on mac and windows*
  - Usb keyboard
  - Mini hdmi to hdmi adapter if using the Pi Zero
  - Micro usb to usb adapter

This project was made with a Raspberry Pi Zero W. It can be done on other pi's as well, but for the sake of this guide it's going to be Pi Zero W specific.


*This is a work in progress and all feedback is welcome!*

# Lets get started!

## Step 1: Rasbian lite image
  - Download the Rasbian lite image https://www.raspberrypi.org/downloads/raspbian/
  - Bake image onto your sd card using ApplePi Baker or alternative  
  
## Step 2: Activate WiFi
  - Plug your keyboard into your pi
  - Plug pi into a tv or monitor and let it boot for the first time (can take a while so be patient)
  - Default username is "pi" password is "raspberry"
  - Type into the command line "sudo raspi-config" and hit enter. Follow the instructions to set up wifi
    *If having trouble with WiFi please refer here https://www.raspberrypi.org/documentation/configuration/wireless/wireless-cli.md

## Step 3: Install omx player (This is how we will be playing the video files)
  - Type the following into the command line and press enter.
  ```sudo apt-get install omxplayer ```
  - Once finished downloading and installing reboot the pi
  -  Type the following and hit enter to reboot
  ```sudo reboot``` 
  
## Step 4: Make file on the pi for the script
  - Change the directory to where the script will live "cd /home/pi"
  - Create a file in that directory by typing the following
  ``` sudo nano buttonscript.py ```
  *You can type the script in right now ssh in later and copy and paste the code that I've added to this guide (I recommend copy and pasting)*

## Step 5: Have the script start on boot
  - Type the following and hit enter
  ``` cd /lib/systemd/system/ ```
  - Create button.service file 
  ```sudo nano button.service```
  * Add the text below to button.service*
```
[Unit]
Description=buttonscript
After=multi-user.target

[Service]
User=pi
Type=simple
ExecStart=/usr/bin/python /home/pi/buttonscript.py
Restart=on-abort

[Install]
WantedBy=multi-user.target
```

## Step 5: Activate the startup script we just added
  - Type the following and then hit enter
  ``` sudo chmod 644 /lib/systemd/system/button.service ``` 
  - Type the following and then hit enter
  ``` sudo chmod +x /home/pi/buttonscript.py ```
  - Type the following and then hit enter
  ``` sudo systemctl daemon-reload ```
  - Type the following and then hit enter
  ``` sudo systemctl enable button ```
  - Type the following and then hit enter
  ``` sudo systemctl start button ```
  
## Step 6: Add video files (check to make sure video files are compatable with omxplayer !important)
  - Type the following and then hit enter
  ``` cd /home/pi ``` 
  - Create a file for Simpsons episodes
  ``` sudo nano simpsons ```
  - Reboot pi "
  ``` sudo reboot ```
  - Use an ftp program to ssh into your pi and find the Simpson file you just made.
  - Drag all of the video files you want to shuffle into that folder. This will take a LONG time to transfer the files, so be ready to leave it overnight.

## THATS IT FOR SETTING UP, TIME FOR WIRING!!
  *If your pi has a header pre-soldered in simply use jumper wires for connecting, if not be prepared to solder.* 
  *You can connect the wires to both the 10k resistor and the button by soldering and using spade connectors.*
  **Make sure you are using normally open button !important**

I have uploaded a diagram to give a visual guide, use the diagram and the instructions below in tandum to better undstand how to wire up your button to your pi. 

Use this chart as a reference https://pinout.xyz/ for the pin layout on the Raspberry Pi

- we are using Pin 11 (BCM 17) and our ground will be Pin 6

- Wire the ground wire to 10k resistor. Then other side of 10k resistor to T splice with the pin 11 (BCM 17)

- pin 11 (BCM 17) wire goes: pin 11/ground splice/button

- Next wire is 3.3v (pin 1) to the other side of the button

## Everything should be ready! Woohoo!
Go ahead and plug your pi into your tv and wait for it to load to the login. Then press your button and yell out in joy when it plays your favorite episode (or doesnt work and you get to start re-tracing your steps)

## Python script below 

```
#!/usr/bin/python

import RPi.GPIO as GPIO
import time
import os
import random

buttonPin = 17 

directory = "/home/pi/simpsons/"

GPIO.setmode(GPIO.BCM)
GPIO.setup(buttonPin, GPIO.IN)

def playEpisode():
	episode = random.choice(os.listdir(directory))
	cmd = "nohup omxplayer -b -o hdmi "+"'"+directory+episode+"' &"
	os.system('killall omxplayer.bin')
	os.system(cmd)


try:

    # measure the time the button is pressed as timeA
    GPIO.wait_for_edge(buttonPin, GPIO.RISING)
    timeA = time.time()

    # measure the time the button is released as timeB
    GPIO.wait_for_edge(buttonPin, GPIO.FALLING)
    timeB = time.time()

    # take the first time away from the second time, to get the difference
    timeDifference = timeB - timeA

    # if the difference in times is more than 4 seconds, shutdown, or else play an episode and restart this script
    if timeDifference > 4:
        os.system('sudo shutdown now')
    else:
        playEpisode()
        # point this to the location of this file
        os.system('sudo python /home/pi/buttonscript.py')

except KeyboardInterrupt:  
    GPIO.cleanup() 
```

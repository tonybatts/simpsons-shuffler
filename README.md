# simpsons-shuffler Guide 
# Short press of button will play random episode. Long press will shutdown pi

A guide to a raspberry pi shuffler for tv shows

About a year ago i was looking for cool raspberry pi projects to do. I stumbled across one that i immediately new 
I needed to build, The Simpsons Shuffler by Stephen Coyle. After hours of building and making the code he provided work for 
me and my needs (and a little help from Stephen himself) I had a pi zero that shuffles episodes of the simpsons on button push and ALSO safely turned off the pi on a long button press. I posted my project to reddit and have been recieving requests for help ever since. So I have decided to finally make my own step by step guide. 




# prerequisites
  - Cyberduck (sftp) for mac
  - applepi baker (to add image to sd card) for mac
  - Filezilla (sftp) for windows
  - Etcher (to add image to sd card) on mac and windows
  - usb keyboard
  - mini hdmi to hdmi adapter
  - microusb to usb adapter

This project was made with a raspberry pi zero w (to make connecting the wires easier). It can be done on other pi's as well, but for the sake of this guide its going to be pi zero w specific.


This is a work in progress and all feedback is welcome!

# Setting up the Raspberry Pi Zero W Simpsons Shuffler

# Step 1: Rasbian lite image
  - Download Rasbian lite image from here https://www.raspberrypi.org/downloads/raspbian/
  - Bake image onto your sd card (i used 64gb) I used ApplePi Baker
  
# Step 2: Activate WiFi
  - plug your keyboard into your pi
  - Plug pi into a tv or monitor and let it boot for the first time (can take a while so be patient)
  - username is "pi" password is "raspberry"
  - type into the command line "sudo raspi-config" and follow the instructions to set up wifi
If having trouble with WiFi please refer here https://www.raspberrypi.org/documentation/configuration/wireless/wireless-cli.md

# Step 3: Get omx player (player we will be using)
  - Type into the command line "sudo apt-get install omxplayer"

Wait until finished downloading and installing and then reboot to activate changes
  - "sudo reboot" 
  
# Step 4: Make file on the pi for the script
  - change the directory to the one where the script will be "cd /home/pi"
  - create the file where the script will be "sudo nano buttonscript.py"
You can type the script in right now or you can use an ftp to find that file you just created and copy and paste the code that i've added to the bottom of this guide (i recommend copy and pasting)

# Step 5: Have the script start on boot
  - "cd /lib/systemd/system/"
  - create button.service file "sudo nano button.service"
Add the text below to button.service

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

# Step 5: Activate the startup script we just added
  - "sudo chmod 644 /lib/systemd/system/button.service"
  - "chmod +x /home/pi/buttonscript.py"
  - "sudo systemctl damon-reload"
  - "sudo systemctl enable buttonscript"
  - "sudo systemctl start buttonscript"
  
Step 6: Now time to add video files (check to make sure video files are compatable with omxplayer!)
  - "cd /home/pi"
  - create file for simpsons episodes  "sudo nano simpsons"
  - reboot pi "sudo reboot"
  
Use an ftp program to ssh into your pi and find the simpson file you just made. Drag all of the video files you want to shuffle into that folder. This will take a LONG time to transfer the files, so be ready to leave it overnight.

# THATS IT FOR SETTING UP TIME FOR WIRING
For the wires if you are using the zero w h like i was you can use jumper wires to connect to the pi. 
For conecting the wires to the 10k resistor and and the button you can solder or rig it up with electrical tape.
I personally used spade connectors to connect to my button
Make sure you are using normally open button!

I will upload a diagram to show more clearly how to wire the button. 
Use this chart as a reference https://pinout.xyz/ for the pin layout

- we are using Pin 11 (BCM 17) and our ground will be Pin 6

- Wire the ground wire to 10k resistor. Then other side of 10k resistor to T splice with the pin 11 (BCM 17)

- pin 11 (BCM 17) wire goes: pin 11/ground splice/button

- Next wire is 3.3v (pin 1) to the other side of the button

# Everything should be ready! Woohoo!
Go ahead and plug your pi into your tv and wait for it to load to the login. Then press your button and yell out in joy when it plays your favorite episode (or doesnt work and you get to start retracing your steps)

# here is the python script 

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

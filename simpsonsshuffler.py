!/Usr/Bin/Python

import RPi.GPIO as GPIO import time import os import random
buttonPin = 17
directory = "/home/stephen/simpsons/"
GPIO.setmode(GPIO.BCM) GPIO.setup(buttonPin, GPIO.IN)
def playEpisode(): episode = random.choice(os.listdir(directory)) cmd = "nohup omxplayer -b -o hdmi "+"'"+directory+episode+"' &" os.system('killall omxplayer.bin') os.system(cmd)
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
    os.system('sudo python /home/stephen/randomSimpsonsShutdown.py')
except KeyboardInterrupt:
GPIO.cleanup()
import pyaudio
import sys, pygame, math
import numpy as np
from pygame.locals import *

CHUNK = 2**10
RATE = 44100

p=pyaudio.PyAudio()

stream=p.open(format=pyaudio.paInt16,channels=1,rate=RATE,input=True,frames_per_buffer=CHUNK)
audiopeaksize = 0
while True:
	data = np.fromstring(stream.read(CHUNK),dtype=np.int16)
	peak = np.average(np.abs(data))*2
	bars = "."*int(600*peak/2**16)
	#print("%05d %s"%(peak,bars))
	audiopeaksize += 0.1
	y_sine = 100 + int(100*math.sin(audiopeaksize))
	print("%05d"%(peak))


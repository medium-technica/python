import numpy as np
import scipy.signal as signal
import matplotlib.pyplot as plt
import pyaudio
import sys, pygame, math, random
from pygame.locals import *

CHUNK = 2**11
RATE = 44100

p=pyaudio.PyAudio()

stream=p.open(format=pyaudio.paInt16,channels=1,rate=RATE,input=True,frames_per_buffer=CHUNK)
data = np.fromstring(stream.read(CHUNK),dtype=np.int16)

fig, ax = plt.subplots()

y = np.fromstring(stream.read(CHUNK),dtype=np.int16)
lines = ax.plot(y)

fig.canvas.manager.show() 

while True:
    y = np.fromstring(stream.read(CHUNK),dtype=np.int16)
    lines[0].set_ydata(y)
    fig.canvas.draw()
    fig.canvas.flush_events()

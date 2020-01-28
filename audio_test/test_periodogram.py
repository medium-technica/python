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
avg_audio = np.average(np.abs(data))*2
n_avg_audio = 10000*avg_audio/2**16

fs = 10e3
N = 1e5
amp = 2*np.sqrt(2)
freq = 1270.0
noise_power = 0.001 * fs / 2
time = np.arange(N) / fs
x = amp*np.sin(2*np.pi*freq*time)
x += np.random.normal(scale=np.sqrt(noise_power), size=time.shape)

data = np.fromstring(stream.read(CHUNK),dtype=np.int16)
f, Pper_spec = signal.periodogram(data, RATE, 'flattop', scaling='spectrum')

plt.semilogy(f, Pper_spec)
plt.xlabel('frequency [Hz]')
plt.ylabel('PSD')
plt.grid()
plt.ion()
plt.show()

while True:
	data = np.fromstring(stream.read(CHUNK),dtype=np.int16)
	f, Pper_spec = signal.periodogram(data, RATE, 'flattop', scaling='spectrum')
	plt.semilogy(f, Pper_spec)
	plt.draw()
	plt.pause(0.001)


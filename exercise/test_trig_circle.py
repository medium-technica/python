# Examples of the math.sin() and math.cos() trig functions
# Al Sweigart al@inventwithpython.com

# You can learn more about Pygame with the
# free book "Making Games with Python & Pygame"
#
# http://inventwithpython.com/pygame
#
import pyaudio
import sys, pygame, math, random
import numpy as np
from pygame.locals import *

CHUNK = 2**11
RATE = 44100

p=pyaudio.PyAudio()

stream=p.open(format=pyaudio.paInt16,channels=1,rate=RATE,input=True,frames_per_buffer=CHUNK)

# set up a bunch of constants
BRIGHTBLUE = (  0,  50, 255)
RED        = (255,   0,   0)
WHITE      = (255, 255, 255)
BLACK      = (  0,   0,   0)
DARKRED    = (128,   0,   0)
YELLOW     = (255, 255,   0)


BGCOLOR = WHITE

WINDOWWIDTH = 640 # width of the program's window, in pixels
WINDOWHEIGHT = 480 # height in pixels
WIN_CENTERX = int(WINDOWWIDTH / 2)
WIN_CENTERY = int(WINDOWHEIGHT / 2)

FPS = 180

AMPLITUDE = 100

BALLSIZE = 20

# standard pygame setup code
pygame.init()
FPSCLOCK = pygame.time.Clock()
DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
pygame.display.set_caption('Trig Circle')

step = 0

# main application loop
while True:
    # event handling loop for quit events
    for event in pygame.event.get():
        if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
            pygame.quit()
            sys.exit()
            
    # fill the screen to draw from a blank state
    DISPLAYSURF.fill(BGCOLOR)
    
    data = np.fromstring(stream.read(CHUNK),dtype=np.int16)
    avg_audio = np.average(np.abs(data))*2
    n_avg_audio = 10000*avg_audio/2**16
    #print("%04f"%(n_avg_audio))
    
    circle_size = int(200*(1-.5**(n_avg_audio*(0.003))))
    
    r_value = int(255*(1-.5**(n_avg_audio*(0.03))))
    g_value = 255
    b_value = 0
    
    COLOUR = (r_value, g_value, b_value)
    
    # draw blue ball
    pygame.draw.circle(DISPLAYSURF, COLOUR, (WIN_CENTERX, WIN_CENTERY), circle_size)

    pygame.display.update()
    FPSCLOCK.tick(FPS)
    pygame.display.update()

    step += 0.02
    step %= 2 * math.pi

# Examples of the math.sin() and math.cos() trig functions
# Al Sweigart al@inventwithpython.com

# You can learn more about Pygame with the
# free book "Making Games with Python & Pygame"
#
# http://inventwithpython.com/pygame
#

import sys, pygame, math
from pygame.locals import *

# set up a bunch of constants
BRIGHTBLUE = (  0,  50, 255)
RED        = (255,   0,   0)
WHITE      = (255, 255, 255)
BLACK      = (  0,   0,   0)
DARKRED    = (128,   0,   0)
YELLOW     = (255, 255,   0)

BLINK = (WHITE, BLACK)

BGCOLOR = BLACK

WINDOWWIDTH = 300 # width of the program's window, in pixels
WINDOWHEIGHT = 300 # height in pixels
WIN_CENTERX = int(WINDOWWIDTH / 2)
WIN_CENTERY = int(WINDOWHEIGHT / 2)

FPS = 15

BALLSIZE = 30

# standard pygame setup code
pygame.init()
FPSCLOCK = pygame.time.Clock()
DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
pygame.display.set_caption('Python Blink')

i = 0

# main application loop
while True:
    # event handling loop for quit events
    for event in pygame.event.get():
        if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
            pygame.quit()
            sys.exit()

    # fill the screen to draw from a blank state
    DISPLAYSURF.fill(BGCOLOR)

    '''
    # draw center lines
    pygame.draw.line(DISPLAYSURF, WHITE, (WIN_CENTERX, 0), (WIN_CENTERX, WINDOWHEIGHT))
    pygame.draw.line(DISPLAYSURF, WHITE, (0, WIN_CENTERY), (WINDOWWIDTH, WIN_CENTERY))
    '''
	
    # draw blue ball
    xPos = int(WIN_CENTERX)
    yPos = int(WIN_CENTERY)
    pygame.draw.circle(DISPLAYSURF, BLINK[i%2], (int(xPos), int(yPos)), BALLSIZE)
    i=i+1;
	
    # draw border
    pygame.draw.rect(DISPLAYSURF, BLACK, (0, 0, WINDOWWIDTH, WINDOWHEIGHT), 1)

    pygame.display.update()
    FPSCLOCK.tick(FPS)

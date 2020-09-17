#http://anh.cs.luc.edu/handsonPythonTutorial/graphics.html
from graphics import *

import keyboard as key
import numpy as np
import time

widthWin = 1024	
heightWin = 768
win = GraphWin("Clock", widthWin, heightWin)
win.setBackground("black")
frames = 2000
tStep = 1/frames
radiusClock = heightWin/2*0.75
xCentreClock = widthWin/2
yCentreClock = heightWin/2

message1 = Text(Point(xCentreClock, yCentreClock), "Week Cycle")
message2 = Text(Point(xCentreClock, yCentreClock*(1.05)), "")
message1.setTextColor("white")
message2.setTextColor("white")

message1.draw(win)
message2.draw(win)

pointCentreClock = Point(xCentreClock, yCentreClock)
rUnit = 2*np.pi/7
for i in range(7):
 sPoint = Point(xCentreClock + radiusClock*0.9*np.cos(i*rUnit), yCentreClock + radiusClock*0.9*np.sin(i*rUnit))
 ePoint = Point(xCentreClock + radiusClock*np.cos(i*rUnit), yCentreClock + radiusClock*np.sin(i*rUnit))
 lineFrame = Line(sPoint, ePoint)
 lineFrame.setOutline("white")
 lineFrame.draw(win)

rUnit = 2*np.pi/(24*7)
for i in range(24*7):
 sPoint = Point(xCentreClock + radiusClock*0.95*np.cos(i*rUnit), yCentreClock + radiusClock*0.95*np.sin(i*rUnit))
 ePoint = Point(xCentreClock + radiusClock*np.cos(i*rUnit), yCentreClock + radiusClock*np.sin(i*rUnit))
 lineFrame = Line(sPoint, ePoint)
 lineFrame.setOutline("white")
 lineFrame.draw(win)

radiusOrbitS = []
xCentreOrbitS = []
yCentreOrbitS = []
centreOrbitS = []
orbitS = []
radiusS = []
centreS = []
x0S = []
y0S = []
x1S = []
y1S = []
s = []
thetaS = []

for i in range(7):
 radiusOrbitS.append(0)
 xCentreOrbitS.append(0)
 yCentreOrbitS.append(0)
 centreOrbitS.append(0)
 orbitS.append(0)
 radiusS.append(0)
 centreS.append(0)
 x0S.append(0)
 y0S.append(0)
 x1S.append(0)
 y1S.append(0)
 s.append(0)
 thetaS.append(0)

 radiusOrbitS[i] = radiusClock * (1-i*0.05)
 xCentreOrbitS[i] = xCentreClock
 yCentreOrbitS[i] = yCentreClock
 centreOrbitS[i] = Point(xCentreOrbitS[i], yCentreOrbitS[i])
 orbitS[i] = Circle(centreOrbitS[i], radiusOrbitS[i])
 orbitS[i].setOutline("white")
 orbitS[i].draw(win)
 
 
 radiusS[i] = 5
 x0S[i] = xCentreOrbitS[i] + radiusOrbitS[i]
 y0S[i] = yCentreOrbitS[i]
 centreS[i] = Point(x0S[i], y0S[i])
 centreOrbitS[i] = Point(xCentreOrbitS[i], y0S[i])
 orbitS[i] = Circle(centreOrbitS[i], radiusOrbitS[i])
 s[i] = Circle(centreS[i], radiusS[i])  # set center and radius
 s[i].setOutline("yellow")
 s[i].setFill("yellow")
 s[i].draw(win)
 orbitS[i].setOutline("white")
 orbitS[i].draw(win)

i = 0
k=1
while(True):
 iS = i % 7
 n = i/frames
 #thetaS[iS] = (-2*np.pi*(i * (iS+1))/frames)
 thetaS[iS] = -2*np.pi*n
 #thetaS[iS] = (-2*np.pi*i/frames)
 x1S[iS] = xCentreOrbitS[iS] + radiusOrbitS[iS]*np.cos(thetaS[iS])
 y1S[iS] = yCentreOrbitS[iS] + radiusOrbitS[iS]*np.sin(thetaS[iS])
 s[iS].move(x1S[iS]-x0S[iS], y1S[iS]-y0S[iS])
 
 time.sleep(tStep)

 x0S[iS] = x1S[iS]
 y0S[iS] = y1S[iS]
 i += k
 if(key.is_pressed('p')):
  time.sleep(0.2)
  if (k == 0):
   k = 1
  else:
   k = 0



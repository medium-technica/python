#http://anh.cs.luc.edu/handsonPythonTutorial/graphics.html
from graphics import *

import numpy as np
import time

widthWin = 640	
heightWin = 480
win = GraphWin("Clock", widthWin, heightWin)
win.setBackground("black")
frames = 2000
tStep = 1/frames
radiusClock = heightWin/2*0.75
xCentreClock = widthWin/2
yCentreClock = heightWin/2

message1 = Text(Point(xCentreClock, yCentreClock), "Jyothish Clock")
message2 = Text(Point(xCentreClock, yCentreClock*(1.05)), "")
message1.setTextColor("white")
message2.setTextColor("white")

message1.draw(win)
message2.draw(win)

pointCentreClock = Point(xCentreClock, yCentreClock)
rUnit = 2*np.pi/24
for i in range(24):
	sPoint = Point(xCentreClock + radiusClock*0.9*np.cos(i*rUnit), yCentreClock + radiusClock*0.9*np.sin(i*rUnit))
	ePoint = Point(xCentreClock + radiusClock*np.cos(i*rUnit), yCentreClock + radiusClock*np.sin(i*rUnit))
	lineFrame = Line(sPoint, ePoint)
	lineFrame.setOutline("white")
	lineFrame.draw(win)

periodMoon = 29.53
periodVenus = 0.2

radiusOrbitSun = radiusClock
radiusSun = 10
xCentreOrbitSun = xCentreClock
yCentreOrbitSun = yCentreClock
x0Sun = xCentreOrbitSun + radiusOrbitSun
y0Sun = yCentreOrbitSun
centreSun = Point(x0Sun, y0Sun)
centreOrbitSun = Point(xCentreOrbitSun, y0Sun)
orbitSun = Circle(centreOrbitSun, radiusOrbitSun)
sun = Circle(centreSun, radiusSun)  # set center and radius
sun.setOutline("yellow")
sun.setFill("yellow")
sun.draw(win)
orbitSun.setOutline("white")
orbitSun.draw(win)

radiusOrbitMoon = radiusOrbitSun
radiusMoon = 10
xCentreOrbitMoon = widthWin/2
yCentreOrbitMoon = heightWin/2
x0Moon = xCentreOrbitMoon + radiusOrbitMoon
y0Moon = yCentreOrbitMoon
centreMoon = Point(x0Moon, y0Moon)
centreOrbitMoon = Point(xCentreOrbitMoon, y0Moon)
orbitMoon = Circle(centreOrbitMoon, radiusOrbitMoon)
moon = Circle(centreMoon, radiusMoon)  # set center and radius
moon.setOutline("white")
moon.setFill("white")
moon.draw(win)
orbitMoon.setOutline("white")
orbitMoon.draw(win)

radiusOrbitVenus = 30
radiusVenus = 5
xCentreOrbitVenus = x0Sun
yCentreOrbitVenus = y0Sun
x0Venus = xCentreOrbitVenus + radiusOrbitVenus
y0Venus = yCentreOrbitVenus
centreVenus = Point(x0Venus, y0Venus)
centreOrbitVenus = Point(x0Sun, y0Sun)
orbitVenus = Circle(centreOrbitVenus, radiusOrbitVenus)
venus = Circle(centreVenus, radiusVenus)  # set center and radius
venus.setOutline("white")
venus.setFill("white")
venus.draw(win)
orbitVenus.setOutline("white")
orbitVenus.draw(win)

i = 0
while(True):
	thetaSun = (-2*np.pi*i/frames)
	x1Sun = xCentreOrbitSun + radiusOrbitSun*np.cos(thetaSun)
	y1Sun = yCentreOrbitSun + radiusOrbitSun*np.sin(thetaSun)
	sun.move(x1Sun-x0Sun, y1Sun-y0Sun)
	
	thetaMoon = (-2*np.pi*i*(1 - 1/periodMoon)/frames) % (2*np.pi)
	x1Moon = xCentreOrbitMoon + radiusOrbitMoon*np.cos(thetaMoon)
	y1Moon = yCentreOrbitMoon + radiusOrbitMoon*np.sin(thetaMoon)
	moon.move(x1Moon-x0Moon, y1Moon-y0Moon)
	
	thetaVenus = (-2*np.pi*i*(1-1/periodVenus)/frames) % (2*np.pi)
	x1Venus = x1Sun + radiusOrbitVenus*np.cos(thetaVenus)
	y1Venus = y1Sun + radiusOrbitVenus*np.sin(thetaVenus)
	venus.move(x1Venus-x0Venus, y1Venus-y0Venus)
	x0Venus = x1Venus
	y0Venus = y1Venus	
	orbitVenus.move(x1Sun-x0Sun, y1Sun-y0Sun)
	
	time.sleep(tStep)
	
	x0Sun = x1Sun
	y0Sun = y1Sun
	
	x0Moon = x1Moon
	y0Moon = y1Moon
	days = -thetaSun / (2*np.pi) % periodMoon
	if (i%frames == 0):
		textDays = "Day: " + str(int(days))
		message2.setText(textDays)
		#print(days)
		time.sleep(1)
	i += 1

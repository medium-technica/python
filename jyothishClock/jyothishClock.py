from graphics import *
import numpy as np
import time

widthWin = 1024	
heightWin = 768
win = GraphWin("Clock", widthWin, heightWin)
win.setBackground("black")
frames = 4000
tStep = 5/frames

periodMoon = 29.53
periodVenus = 0.2

radiusOrbitSun = heightWin/2*0.75
radiusSun = 10
xCentreOrbitSun = widthWin/2
yCentreOrbitSun = heightWin/2
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
	thetaSun = 2*np.pi*i/frames
	x1Sun = xCentreOrbitSun + radiusOrbitSun*np.cos(thetaSun)
	y1Sun = yCentreOrbitSun + radiusOrbitSun*np.sin(thetaSun)
	sun.move(x1Sun-x0Sun, y1Sun-y0Sun)
	
	thetaMoon = 2*np.pi*i*(1 - 1/periodMoon)/frames
	x1Moon = xCentreOrbitMoon + radiusOrbitMoon*np.cos(thetaMoon)
	y1Moon = yCentreOrbitMoon + radiusOrbitMoon*np.sin(thetaMoon)
	moon.move(x1Moon-x0Moon, y1Moon-y0Moon)
	
	thetaVenus = 2*np.pi*i*(1-1/periodVenus)/frames
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
		
	i += 1

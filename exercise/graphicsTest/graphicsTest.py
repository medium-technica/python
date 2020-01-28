from graphics import *
import numpy as np
import time
widthWin = 500
heightWin = 500
win = GraphWin("Clock", widthWin, heightWin)
win.setBackground("black")


radiusOrbitSun = 200
radiusSun = 10
xCentreOrbitSun = widthWin/2
yCentreOrbitSun = heightWin/2
x0Sun = xCentreOrbitSun + radiusOrbitSun
y0Sun = yCentreOrbitSun
centreSun = Point(x0Sun,y0Sun)
centreOrbitSun = Point(xCentreOrbitSun, y0Sun)
orbitSun = Circle(centreOrbitSun, radiusOrbitSun)
sun = Circle(centreSun, radiusSun) # set center and radius
sun.setOutline("yellow")
sun.setFill("yellow")
sun.draw(win)
orbitSun.setOutline("white")
orbitSun.draw(win)

radiusOrbitVenus = 30
radiusVenus = 5
xCentreOrbitVenus = x0Sun
yCentreOrbitVenus = y0Sun
x0Venus = xCentreOrbitVenus + radiusOrbitVenus
y0Venus = yCentreOrbitVenus
centreVenus = Point(x0Venus,y0Venus)
centreOrbitVenus = Point(x0Sun, y0Sun)

orbitVenus = Circle(centreOrbitVenus, radiusOrbitVenus)
venus = Circle(centreVenus, radiusVenus) # set center and radius
venus.setOutline("white")
venus.setFill("white")
venus.draw(win)
orbitVenus.setOutline("white")
orbitVenus.draw(win)

i=0
while(True):
	thetaSun = 2*np.pi*i/1000
	x1Sun = xCentreOrbitSun + radiusOrbitSun*np.cos(thetaSun)
	y1Sun = yCentreOrbitSun + radiusOrbitSun*np.sin(thetaSun)
	sun.move(x1Sun-x0Sun, y1Sun-y0Sun)
	
	thetaVenus = 2*np.pi*i/200
	x1Venus = x1Sun + radiusOrbitVenus*np.cos(thetaVenus)
	y1Venus = y1Sun + radiusOrbitVenus*np.sin(thetaVenus)
	venus.move(x1Venus-x0Venus, y1Venus-y0Venus)
	x0Venus = x1Venus
	y0Venus = y1Venus
	
	orbitVenus.move(x1Sun-x0Sun, y1Sun-y0Sun)
	
	time.sleep(0.01)
	x0Sun = x1Sun
	y0Sun = y1Sun
	i += 1
input()

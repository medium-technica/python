#http://rhodesmill.org/skyfield/
from skyfield.api import load
from skyfield.api import Topos

planets = load('de421.bsp')
earth, sun, moon, mercury, mars = planets['earth'], planets['sun'], planets['moon'], planets['mercury'], planets['mars']

ts = load.timescale()
t = ts.now()
astrometric = earth.at(t).observe(sun)
ra, dec, distance = astrometric.radec()

print(ra)
print(dec)
print(distance)

kozhikode = earth + Topos('11 N', '76 E')
astrometric = kozhikode.at(t).observe(sun)
alt, az, d = astrometric.apparent().altaz()

print(alt)
print(az)
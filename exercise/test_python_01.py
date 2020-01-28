import math
R = 5;
C = 1
for i in range(1000):
	x = int(255*(1-.5**(i*(0.003))))
	if x%50 == 0:
		print("%03d"%(x))

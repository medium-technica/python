rows = 3
cols = 4
arr = [[0] * cols for i in range(rows)]

i=0
j=0

def on_connect(msg):
	global i
	global j
	arr[(i%rows)][(j%cols)] = msg
	j+=1
	if ((j%cols)==0):
		i+=1
	
for k in range(rows*cols):
	on_connect(k)

print (arr)		



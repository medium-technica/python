import time
 
def timestamp():
   now = time.time()
   localtime = time.localtime(now)
   milliseconds = '%03d' % int((now - int(now)) * 1000)
   return time.strftime('%Y%m%d%H%M%S', localtime) + milliseconds

print timestamp()
print (time.strftime("%Y-%m-%d, %H:%M:%S"))


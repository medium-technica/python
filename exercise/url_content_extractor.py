import urllib2
import urllib
import os
import time
from termcolor import colored
#import time
sid = input("Enter the Unique Id(ex:4816): ")
sem = input("Enter the Semester(ex:6): ")
regi = raw_input("Enter the Univ. Reg code(ex:jyamecs): ")
sno = input("Enter the starting number(ex:1): ")
fno = input("Enter the last number(ex:61): ")
sems="SEM"+str(sem)+"_"+time.strftime("%d-%m-%Y")
#sems="SEM"+sem
if not os.path.exists(sems):
    os.makedirs(sems)
print "Calicut University B.Tech Result PDF Downloader"
print colored('Scripted by SP, CSE Dept, JECC','yellow')
for reg in xrange(sno,fno+1):
	url='http://202.88.252.21/CuPbhavan/res_newregentry.php'
	url2='http://202.88.252.21/CuPbhavan/rs_newcheck.php'
	url3='http://202.88.252.21/CuPbhavan/cubtech7/sugrres.php'
	if reg < 10:
		regnum=regi+"00"+str(reg)
	else:
		regnum=regi+"0"+str(reg)
	fn=str(reg)+"."+"pdf"
	#os.chdir(sems)
	#path='sems/fn'
	#if os.path.isfile(path):
	#	continue
	print "Downloading pdf for %s..." % regnum
	#time.sleep(1)
	values = {'regno' : regnum,
	   'sum' : '107',
	   'id' : sid,
	   'sessionok' :'yes' }
	data = urllib.urlencode(values)

	req = urllib2.Request(url,data)


	req.add_header('Origin', 'http://202.88.252.21')
	req.add_header("Accept-Encoding", "gzip,deflate,sdch")
	req.add_header('Host', '202.88.252.21')
	req.add_header('Accept-Language', 'en-GB,en-US;q=0.8,en;q=0.6')
	req.add_header('User-Agent', 'Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/30.0.1599.114 Chrome/30.0.1599.114 Safari/537.36')
	req.add_header('Content-Type', 'application/x-www-form-urlencoded')
	req.add_header('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8')
	req.add_header('Referer', 'http://202.88.252.21/CuPbhavan/res_newregentry.php?id=sid')
	req.add_header('Cookie', 'PHPSESSID=ben46a7bbde3h48n733gc3jhs0')
	req.add_header('Connection', 'keep-alive')
	req.add_header('DNT', '1')
	res = urllib2.urlopen(req)
	webContent = res.read()
	os.chdir(sems)
	f = open('1.html', 'w')
	f.write(webContent)
	f.close
	req2 = urllib2.Request(url2,data)
	req2.add_header('DNT', '1')
	req2.add_header("Accept-Encoding", "gzip,deflate,sdch")
	req2.add_header('Host', '202.88.252.21')
	req2.add_header('Accept-Language', 'en-GB,en-US;q=0.8,en;q=0.6')
	req2.add_header('User-Agent', 'Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/30.0.1599.114 Chrome/30.0.1599.114 Safari/537.36')
	req2.add_header('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8')
	req2.add_header('Referer', 'http://202.88.252.21/CuPbhavan/res_newregentry.php')
	req2.add_header('Cookie', 'PHPSESSID=ben46a7bbde3h48n733gc3jhs0')
	req2.add_header('Connection', 'keep-alive')
	res2 = urllib2.urlopen(req2)
	webContent2 = res2.read()
	#os.chdir(sems)
	f2 = open('2.html', 'w')
	f2.write(webContent2)
	f2.close
	req3 = urllib2.Request(url3,data)
	req3.add_header('DNT', '1')
	req3.add_header("Accept-Encoding", "gzip,deflate,sdch")
	req3.add_header('Host', '202.88.252.21')
	req3.add_header('Accept-Language', 'en-GB,en-US;q=0.8,en;q=0.6')
	req3.add_header('User-Agent', 'Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/30.0.1599.114 Chrome/30.0.1599.114 Safari/537.36')
	req3.add_header('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8')
	req2.add_header('Referer', 'http://202.88.252.21/CuPbhavan/rs_newcheck.php')
	req3.add_header('Origin', 'http://202.88.252.21')
	req3.add_header('Cookie', 'PHPSESSID=ben46a7bbde3h48n733gc3jhs0')
	req3.add_header('Connection', 'keep-alive')
	res3 = urllib2.urlopen(req3)
	webContent3 = res3.read()
	#fn=str(reg)+"."+"pdf"
	#os.chdir(sems)
	#if not os.path.isfile(fn):
	f3 = open(fn, 'w')
	f3.write(webContent3)
	f3.close
	os.remove("1.html")
	os.remove("2.html")
	os.chdir("..")
print colored('Download Completed !!!','red')

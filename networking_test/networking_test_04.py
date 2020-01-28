import ipaddress

net4 = ipaddress.ip_network("192.168.2.5 ")
for x in net4.hosts():
	print(x)

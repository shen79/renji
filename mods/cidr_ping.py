#!/usr/bin/python

def run(val):
	"""ping all hosts in this network"""
	import urllib
	from scapy.all import sr,IP,ICMP
	val = urllib.unquote(val).decode('utf8') 
	print val
	#
	ret = [];
	src = {'method': 'ping', 'type': 'cidr', 'value': val}
	#
	#scapy.conf.verb = 0
	a,u = sr(IP(dst=val) / ICMP(), timeout=4)
	for p in a:
		print p[1].show()
		dst = {
			'method': 'ICMP echo request',
			'type': 'ip',
			'value': p[1]['IP'].src
		}
		ret.append({'request': src, 'response': dst });
	return ret

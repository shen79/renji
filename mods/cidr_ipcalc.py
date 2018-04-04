#!/usr/bin/python

def run(val):
	"""IPCalc"""
	import netaddr
	import urllib
	import pprint as pp
	val = urllib.unquote(val).decode('utf8') 
	print val
	#
	ret = [];
	src = {'method': 'ipcalc', 'type': 'cidr', 'value': val}
	#
	na = netaddr.IPNetwork(val)
	pp.pprint(na)
	net, bits = val.split('/')
	print net, bits
	v = []
	v.append("network: " + str(na.network))
	v.append("netmask: " + str(na.netmask))
	v.append("hosts: " + str(2**(32-int(bits))-2))
	dst = {
		'method': 'IPcalc',
		'type': 'text',
		'value': "\n".join(v)
	}
	ret.append({'request': src, 'response': dst });
	return ret

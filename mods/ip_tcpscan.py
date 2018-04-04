#!/usr/bin/python

def run(val):
	"""TCP Portscan"""
	from scapy.all import sr,IP,TCP
	#
	ret = [];
	src = {'method': 'dns', 'type': 'ip', 'value': val}
	#
	ports = [21,22,80,443,445]
	a,u = sr(IP(dst=val) / TCP(sport=55555, dport=ports, flags="S"), timeout=4)
	for p in a:
		print p[1].show()
		if p[1]['TCP'].flags == 18:
			dst = {
				'method': 'TCP port scan',
				'type': 'service',
				'value': p[1]['IP'].src + ':' + str(p[1]['TCP'].sport)
			}
			ret.append({'request': src, 'response': dst });
	return ret

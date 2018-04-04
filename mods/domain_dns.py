#!/usr/bin/python

def run(val):
	"""DNS"""
	import dns.resolver
	#
	ret = [];
	src = {'method': 'dns', 'type': 'domain', 'value': val}
	#
	recordTypes =  {
		'A': 'ip',
		'MX': 'domain',
		'NS': 'domain',
		'TXT': 'text',
		'AAAA': 'ip6'
	}
	res = dns.resolver.Resolver()
	for rec in recordTypes:
		ans = []
		try:
			ans = res.query(val, rec)
		except:
			pass
		for a in ans:
			v = str(a)
			if rec == 'MX':
				v = v.split(' ')[1]
			dst = {
				'method': 'DNS "' + rec + '" record',
				'type': recordTypes[rec],
				'value': v
			}
			ret.append({'request': src, 'response': dst });
	return ret

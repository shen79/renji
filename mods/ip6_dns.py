#!/usr/bin/python

def run(val):
	"""DNS"""
	from dns import resolver
	from dns import reversename
	#
	ret = [];
	src = {'method': 'dns', 'type': 'ip', 'value': val}
	#
	addr = reversename.from_address(val)
	dst = {
		'method': 'dns/ptr',
		'type': 'domain',
		'value': str(resolver.query(addr, "PTR")[0])
	}
	ret.append({'request': src, 'response': dst });
	
	return ret

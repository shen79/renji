#!/usr/bin/python

def run(val):
	"""DNS"""
	from dns import resolver
	from dns import reversename
	#
#	ret = [];
	src = {'method': 'dns', 'type': 'ip', 'value': val}
	
	try:
		addr = reversename.from_address(val)
		v = str(resolver.query(addr, "PTR")[0])
	except:
		print 'eh'
	else:
#		ret.append();
		return [{'request': src, 'response': {
			'method': 'dns/ptr',
			'type': 'domain',
			'value': v
		}}]

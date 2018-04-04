#!/usr/bin/python

def run(val):
	"""Whois"""
	import whois
	import pprint as pp
	#
	ret = [];
	src = {'method': 'whois', 'type': 'domain', 'value': val}
	#
	wi = whois.whois(val)
	pp.pprint(wi)


	dst = {
		'method': 'domain-whois',
		'type': 'domain',
		'value': wi
	}
	ret.append({'request': src, 'response': dst	});
	for n in wi['nets']:
		dst = {
			'method': 'whois',
			'type': 'cidr',
			'value': n['cidr']
		}
		ret.append({
			'request': src,
			'response': dst
		});
#			childRequest = dst
		wFields = {
			'description': 'text',
			'country': 'countrycode',
			'city': 'city'
		}
		for field in wFields:
			# pp.pprint({field: n[field]})
			if n[field]:
				ret.append({
					'request': dst,
					'response': {
						'method': field,
						'type': wFields[field],
						'value': n[field]
					}
				});

#			if wi[key] is not None:
	return ret

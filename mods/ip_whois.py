#!/usr/bin/python

def run(cvalue):
	"""Whois"""
	from ipwhois import IPWhois
	import pprint as pp
	ret = [];
	src = {'method': 'whois', 'type': 'ip', 'value': cvalue}
	r = IPWhois(cvalue).lookup_whois()
	pp.pprint(r)
	dst = {
		'method': 'ip-whois',
		'type': 'asn',
		'value': r['asn']
	}
	ret.append({'request': src, 'response': dst	});
	for n in r['nets']:
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
			pp.pprint({field: n[field]})
			if n[field]:
				ret.append({
					'request': dst,
					'response': {
						'method': field,
						'type': wFields[field],
						'value': n[field]
					}
				});
	return ret

#!/usr/bin/python

def run(val):
	import pygeoip
	import pprint as pp
	#/usr/share/GeoIP/GeoIP.dat
	#/usr/share/GeoIP/GeoIPv6.dat
	#/usr/share/GeoIP/GeoIPASNum.dat
	#/usr/share/GeoIP/GeoIPCity.dat
	g = pygeoip.GeoIP('/usr/share/GeoIP/GeoIP.dat')
	g6 = pygeoip.GeoIP('/usr/share/GeoIP/GeoIPv6.dat')
	gas = pygeoip.GeoIP('/usr/share/GeoIP/GeoIPASNum.dat')
	gcity = pygeoip.GeoIP('/usr/share/GeoIP/GeoIPCity.dat')
	#
	ret = [];
	src = {'method': 'geoip', 'type': 'ip', 'value': val}
	#
	
	ret.append({'request': src, 'response': {
		'method': "geoip",
		'type': "country",
		'value': g.country_name_by_addr(val)
	}});
	return ret

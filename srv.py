#!/usr/bin/python

from flask import Flask, request, Response, render_template, send_from_directory
from flask_restful import Resource, Api, reqparse, abort
from parser import *
import pprint
pp = pprint.PrettyPrinter(indent=4)

from jsonrpcserver import methods
import importlib, scandir, sys, os, json
# scriptroot = os.path.dirname(os.path.realpath(__file__))
# sys.path.append(scriptroot + "/mods")
# sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/mods")


# https://bcb.github.io/jsonrpc/flask
#rq = json.loads(asd) # json.dumps


@methods.add
def ping():
	return 'pong'
	
@methods.add
def ip_2_mac(ip):
	rp = []
	ls(scapy)
#	mac = scapy.scapy.getmacbyip(ip)
#	rp.append({'mac': 'mac'})
	return rp

app = Flask(__name__)
app.jinja_env.cache = {}

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/js/<path:path>')
def send_js(path):
	return send_from_directory('js', path)

@app.route('/css/<path:path>')
def send_css(path):
	return send_from_directory('css', path)




# === API ==========================================================================================

# parser.add_argument('task')
class Methods():
	def ip_whois(self, cvalue):
		"""Get whois record for this IP"""
		from ipwhois import IPWhois
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

	def ip_dns(self, val):
		"""Get PTR recor for this IP"""
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
	def domain_whois(self, val):
		"""Get whois record for this domain"""
		import whois
		#
		ret = [];
		src = {'method': 'dns', 'type': 'domain', 'value': val}
		#
		wi = whois.whois(val)
		pp.pprint(wi)
		recordTypes =  {
			'country': 'country',
			'state': 'state',
			'city': 'city',
			'address': 'address',
			'name': 'name',
			'creation_date': 'date',
			'address': 'address'
		}
		for key in recordTypes:
			dst = {
				'method': 'whois/'+key,
				'type': recordTypes[key],
				'value': str(wi[key])
			}
			ret.append({'request': src, 'response': dst });
		return ret
			

	def domain_dns(self, val):
		"""Get DNS record for this domain"""
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

	def cidr_ipcalc(self, val):
		"""Calculate for this CIDR"""
		import netaddr
		import urllib
		val = urllib.unquote(val).decode('utf8') 
		print val
		#
		ret = [];
		src = {'method': 'ipcalc', 'type': 'cidr', 'value': val}
		#
		na = netaddr.IPNetwork(val)
		dst = {
			'method': 'IPcalc net',
			'type': 'network',
			'value': str(na.network)
		}
		ret.append({'request': src, 'response': dst });
		dst = {
			'method': 'IPcalc net',
			'type': 'netmask',
			'value': str(na.netmask)
		}
		ret.append({'request': src, 'response': dst });
		return ret
	def cidr_ping(self, val):
		"""Calculate for this CIDR"""
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



	
class ApiTest(Resource, Methods):
	def get(self,cmethod,ctype,cvalue):
		m = Methods()
		print dir(m)
		
		originalRequest = {'method': cmethod, 'type': ctype, 'value': cvalue}
		ret = [];
		# TODO : chk type against value
		
		if ctype == 'ip':
			if cmethod == 'whois':		ret = self.ip_whois(cvalue)
			elif cmethod == 'dns':		ret = self.ip_dns(cvalue)
		elif ctype == 'domain':
			if cmethod == 'dns':		ret = self.domain_dns(cvalue)
			elif cmethod == 'whois':	ret = self.domain_whois(cvalue)
		elif ctype == 'cidr':
			if cmethod == 'ipcalc':		ret = self.cidr_ipcalc(cvalue)
			elif cmethod == 'ping':		ret = self.cidr_ping(cvalue)
		return ret

api = Api(app)
api.add_resource(ApiTest, '/api/<string:cmethod>/<string:ctype>/<string:cvalue>')



# === MAIN =========================================================================================


if __name__ == '__main__':
	app.run()









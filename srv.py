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
	def domain_dns(self, val):
		"""Get DNS record for this domain"""
		import dns.resolver
		#
		ret = [];
		src = {'method': 'dns', 'type': 'domain', 'value': val}
		#
		res = dns.resolver.Resolver()
		for rec in ['A','MX','NS','TXT','AAAA']:
			ans = []
			try:
				ans = res.query(val, rec)
			except:
				pass
			for a in ans:
				dst = {
					'method': 'DNS "' + rec + '" record',
					'type': 'ip',
					'value': str(a)
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
		if cmethod == 'whois':
			if ctype == 'ip':			ret = self.ip_whois(cvalue)
		elif cmethod == 'dns':
			if ctype == 'ip':			ret = self.ip_dns(cvalue)
			if ctype == 'domain':		ret = self.domain_dns(cvalue)
		return ret

api = Api(app)
api.add_resource(ApiTest, '/api/<string:cmethod>/<string:ctype>/<string:cvalue>')



# === MAIN =========================================================================================


if __name__ == '__main__':
	app.run()









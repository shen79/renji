#!/usr/bin/python

from flask import Flask, request, Response, render_template, send_from_directory
from flask_restful import Resource, Api, reqparse, abort
from parser import *
import pprint
pp = pprint.PrettyPrinter(indent=4)

from jsonrpcserver import methods
import importlib, scandir, sys, os, json
SCRIPTROOT = os.path.dirname(os.path.realpath(__file__))
MODS_DIRNAME = 'mods'
sys.path.append(SCRIPTROOT + "/mods")
import mods
# https://bcb.github.io/jsonrpc/flask
#rq = json.loads(asd) # json.dumps

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

class Methods():
	def _getMethods(self):
		ret = {'nul': {
			"add-node": {"name": "add node"},
			"import-nmap": {"name": "import nmap"}
			},
			'text': {}
		}
		for fName in mods._mod_names:
			fu = mods.mods[fName]
			src_type, t_method = fName.split('_', 1)
			if src_type not in ret:
				ret[src_type] = {}
			ret[src_type][t_method] =  {'name': t_method};
		return ret

class ApiTest(Resource, Methods):
	def get(self,cmethod,ctype,cvalue):
		originalRequest = {'method': cmethod, 'type': ctype, 'value': cvalue}
		ret = [];
		if cmethod == 'transformations':
			ret = self._getMethods()
		else:
			fName = ctype + '_' + cmethod
			m = mods.mods[fName]
			ret = m.run(cvalue)
#		print json.dumps(ret)
		return ret

api = Api(app)
api.add_resource(ApiTest, '/api/<string:cmethod>/<string:ctype>/<string:cvalue>')

if __name__ == '__main__':
	app.run()




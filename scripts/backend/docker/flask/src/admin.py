#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
"""

"""
from flask import Flask, render_template, jsonify, request, session, redirect, send_from_directory
from flask_restful import Resource, Api
from config import Config
from login import logged_in
from formatting import *
import get
from CEVAC.Connectors import SQLConnector
from CEVAC.utils import getPipes
from CEVAC.Pipe import Pipe
from sql import connector
import json

app = Flask(__name__, static_url_path='/static')
app.config.from_object(Config)
api = Api(app)

pipes = getPipes(connector=connector, dict=True)

class Attributes(Resource):
    def get(self, BuildingSName, Metric):
        return pipes[BuildingSName][Metric].attributes

class ExistingTables(Resource):
    def get(self, BuildingSName, Metric):
        return pipes[BuildingSName][Metric].existingTables


api.add_resource(Attributes, '/attributes/<string:BuildingSName>/<string:Metric>')
api.add_resource(ExistingTables, '/existingTables/<string:BuildingSName>/<string:Metric>')

get_functions = {
    'table_html': get.table_html,
    'buildings_select': buildings_select_html,
    'metrics_select': metrics_select_html,
    'bin_value': get.bin_value,
    'building_info': get.building_info,

}

@app.route('/')
def index():
    return render_static('/manage')
    #  if logged_in(): return render_static('/manage')
        #  return render_static('login')
@app.route('/<string:page_name>/')
def render_static(page_name):
    return render_template(f'{page_name}.html')

@app.route('/get/<string:name>/')
def get_func(name):
    args = get.clean_args(request.args)
    args.update({'connector':connector})
    return get_functions[name](**args)

app.run(host='0.0.0.0', debug=True, port=5000)

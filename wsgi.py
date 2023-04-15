import os
import json
from flask import Flask, jsonify, request
from db_binding import db_bind

application = Flask(__name__)


@application.route('/')
@application.route('/status')
def status():
    if 'SERVICE_BINDING_ROOT' in os.environ:
    	return jsonify({'status': 'DB binding ok'})
    else:
    	return jsonify({'status': 'DB binding missing'})


@application.route('/dbbind', methods=['POST'])
def create_db_bind():
    data = request.data or '{}'
    body = json.loads(data)
    return jsonify(db_bind(body))

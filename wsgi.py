import os
import json
from flask import Flask, jsonify, request
from confluent_kafka import Consumer, KafkaError

application = Flask(__name__)


@application.route('/')
def default_status():
    if 'SERVICE_BINDING_ROOT' in os.environ:
    	return jsonify({'def status': 'DB binding ok'})
    else:
    	return jsonify({'def status': 'DB binding missing'})

@application.route('/status')
def status():
    if 'SERVICE_BINDING_ROOT' in os.environ:
    	return jsonify({'status': 'DB binding ok'})
    else:
    	return jsonify({'status': 'DB binding missing'})


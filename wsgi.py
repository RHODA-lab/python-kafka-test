import os
import json
from flask import Flask, jsonify, request
from confluent_kafka import Consumer, KafkaError

application = Flask(__name__)

# Kafka data array
data = []

# Kafka cluster config
conf = {
    'bootstrap.servers': 'crdb-cluster-kafka-bootstrap.crdb-kafka.svc.cluster.local',
    'group.id': 'my-group-id',
    'auto.offset.reset': 'earliest'
}

# Initialize Consumer and subscribe to kafka topic
consumer = Consumer(conf)
consumer.subscribe(['user7-table-changes'])

@application.route('/')
def default_status():
    msg = consumer.poll(1.0)
    if msg is not None:
        print('Received message: {}'.format(msg.value().decode('utf-8')))
        # The kafka messages you receive on the topic are appended to the messages array
        # The contents of messages array can be accessed using an http GET
        data.append(msg.value().decode('utf-8'))
        return jsonify(data)
    else:
        return jsonify({'status': 'no kafka messages'})

@application.route('/status')
def status():
    if 'SERVICE_BINDING_ROOT' in os.environ:
    	return jsonify({'status': 'DB binding ok'})
    else:
    	return jsonify({'status': 'DB binding missing'})


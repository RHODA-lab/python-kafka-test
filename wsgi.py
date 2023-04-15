import os
import json
from flask import Flask, jsonify, request
from confluent_kafka import Consumer, Producer, KafkaError

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
producer = Producer(conf)

# Define the callback function to handle delivery reports
def delivery_report(err, msg):
    if err is not None:
        print(f"Delivery failed: {err}")
    else:
        print(f"Message delivered to {msg.topic()} [{msg.partition()}]")

@application.route('/')
def consumer():
    msg = consumer.poll(1.0)
    if msg is not None:
        print('Received message: {}'.format(msg.value().decode('utf-8')))
        # The kafka messages you receive on the topic are appended to the messages array
        # The contents of messages array can be accessed using an http GET
        data.append(msg.value().decode('utf-8'))
        return jsonify(data)
    else:
        return jsonify({'status': 'no kafka messages'})

@application.route('/producer')
def producer():
    # Construct the message to be produced
    message = f"Kafka Test Message {100}".encode("utf-8")
    # Use the producer instance to produce the message to the topic
    producer.produce(topic, key=str(100), value=message, callback=delivery_report)
    # Wait for any outstanding messages to be delivered and delivery reports to be received
    producer.flush()
    return jsonify({'producer': 'posted kafka messages'})


@application.route('/status')
def status():
    if 'SERVICE_BINDING_ROOT' in os.environ:
    	return jsonify({'status': 'DB binding ok'})
    else:
    	return jsonify({'status': 'DB binding missing'})


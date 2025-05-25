from flask import Flask, request
import json
import pika

app = Flask(__name__)

@app.route('/vote', methods=['POST'])
def vote():
    data = request.json
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()
    channel.queue_declare(queue='vote_queue', durable=True)
    channel.basic_publish(
        exchange='',
        routing_key='vote_queue',
        body=json.dumps(data),
        properties=pika.BasicProperties(delivery_mode=2)  # make message persistent
    )
    connection.close()
    return "Vote Received", 200

if __name__ == '__main__':
    app.run(port=5001)

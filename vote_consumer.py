import pika
import json
import os

VOTE_STORE = 'vote_store.json'
if not os.path.exists(VOTE_STORE):
    with open(VOTE_STORE, 'w') as f:
        json.dump({}, f)

def callback(ch, method, properties, body):
    vote = json.loads(body)
    with open(VOTE_STORE, 'r+') as f:
        votes = json.load(f)
        voter_id = vote['voter_id']
        if voter_id not in votes:
            votes[voter_id] = vote['candidate']
        f.seek(0)
        json.dump(votes, f, indent=2)
    ch.basic_ack(delivery_tag=method.delivery_tag)

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()
channel.queue_declare(queue='vote_queue', durable=True)
channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue='vote_queue', on_message_callback=callback)

print("✅ Vote Consumer started...")
channel.start_consuming()

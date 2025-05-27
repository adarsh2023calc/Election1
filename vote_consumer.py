import pika
import json
import os

from db import Vote, SessionLocal, init_db

# Initialize DB schema if not exists
init_db()

def callback(ch, method, properties, body):
    vote_data = json.loads(body)
    voter_id = vote_data['voter_id']
    candidate = vote_data['candidate']

    db = SessionLocal()
    try:
        # Check if voter already voted
        existing_vote = db.query(Vote).filter_by(voter_id=voter_id).first()
        if not existing_vote:
            new_vote = Vote(voter_id=voter_id, candidate=candidate)
            db.add(new_vote)
            db.commit()
            print(f"✅ Vote recorded: {voter_id} -> {candidate}")
        else:
            print(f"⚠️ Voter {voter_id} already voted")
    except Exception as e:
        print(f"❌ Error: {e}")
        db.rollback()
    finally:
        db.close()

    ch.basic_ack(delivery_tag=method.delivery_tag)

# Connect to RabbitMQ
url = os.getenv("CLOUDAMQP_URL")
params = pika.URLParameters(url)
connection = pika.BlockingConnection(params)
channel = connection.channel()
channel.queue_declare(queue='vote_queue', durable=True)
channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue='vote_queue', on_message_callback=callback)

print("🎯 Vote Consumer started. Waiting for messages...")
channel.start_consuming()

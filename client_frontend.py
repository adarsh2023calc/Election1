from flask import Blueprint, render_template, request
import requests
import os
import pika
import json
from dotenv import load_dotenv



client_bp = Blueprint('client', __name__, template_folder='templates')

@client_bp.route('/')
def vote_form():
    return render_template('vote_form.html')

@client_bp.route('/submit_vote', methods=['POST'])
def submit_vote():
    voter_id = request.form.get('voter_id')
    candidate = request.form.get('candidate')

    payload = {
        'voter_id': voter_id,
        'candidate': candidate
    }

    try:
        status = vote(payload)
        if status == 200:
            return f"<h3>Vote submitted successfully!</h3><a href='/client'>Vote Again</a>"
        else:
            return f"<h3>Error while submitting vote.</h3><a href='/client'>Try Again</a>"
    except Exception as e:
        return f"<h3>Server error: {e}</h3>"

def vote(data):
    try:
        url = os.getenv("CLOUDAMQP_URL")
        if not url:
            raise ValueError("CLOUDAMQP_URL environment variable not set")

        params = pika.URLParameters(url)
        connection = pika.BlockingConnection(params)
        channel = connection.channel()
        channel.queue_declare(queue='vote_queue', durable=True)

        channel.basic_publish(
            exchange='',
            routing_key='vote_queue',
            body=json.dumps(data),
            properties=pika.BasicProperties(delivery_mode=2)  # make message persistent
        )
        connection.close()
        return 200
    except Exception as e:
        print(f"❌ RabbitMQ error: {e}")
        return 0

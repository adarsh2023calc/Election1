import pika
import os

def get_channel(queue_name):
    url = os.environ["CLOUDAMQP_URL"]
    params = pika.URLParameters(url)
    connection = pika.BlockingConnection(params)
    channel = connection.channel()
    channel.queue_declare(queue=queue_name, durable=True)
    return channel

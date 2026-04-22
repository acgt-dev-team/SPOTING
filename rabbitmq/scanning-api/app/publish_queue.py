import pika
import json

credentials = pika.PlainCredentials(
    username='admin',
    password='strongpassword'
)

def queue_tugasan(message: str):

    connection = pika.BlockingConnection(
        pika.ConnectionParameters(
            host='178.128.116.198',
            port=5672,
            credentials=credentials
        )
)
    channel = connection.channel()
    channel.queue_declare(queue='tugasan_queue')

    channel.basic_publish(
        exchange='',
        routing_key='tugasan_queue',
        body=message
    )

    connection.close()
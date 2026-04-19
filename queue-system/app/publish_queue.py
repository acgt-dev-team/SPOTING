import pika
import json

credentials = pika.PlainCredentials(
    username='admin',
    password='strongpassword'
)

connection = pika.BlockingConnection(
    pika.ConnectionParameters(
        host='178.128.116.198',
        port=5672,
        credentials=credentials
    )
)

def queue_tugasan(list_scanned: list):
    channel = connection.channel()
    channel.queue_declare(queue='tugasan_queue')

    channel.basic_publish(
        exchange='',
        routing_key='tugasan_queue',
        body=json.dumps(list_scanned)
    )

    # connection.close()
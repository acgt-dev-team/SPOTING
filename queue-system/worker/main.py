import pika
from sqlmodel import Session
from .model.cbom_model import Cbom
from db.config import engine
import time
import json
from datetime import datetime
import requests

credentials = pika.PlainCredentials(username='admin', password='strongpassword')

connection = pika.BlockingConnection(
    pika.ConnectionParameters(
        host='178.128.116.198',
        port=5672,
        credentials=credentials
    )
)

channel = connection.channel()

channel.queue_declare(queue='tugasan_queue')

def callback(ch, method, properties, body):
    time.sleep(2)

    body_str = body.decode('utf-8')

    body = json.loads(body_str)
    
    cbom = Cbom(
        tugasan_id=body['tugasan_id'],
        cbom_data=body['cbom_data']
    )

    with Session(engine) as session:
        session.add(cbom)
        session.commit()
        session.refresh(cbom)
        print(cbom)

    url = f'http://localhost:1234/done-scanning/{body['tugasan_id']}'
    data = {
        'selesai_pada': datetime.now()
    }

    # Create request to backend api which indicate scanning done
    requests.post(url, data)




channel.basic_consume(
    queue='tugasan_queue',
    on_message_callback=callback,
    auto_ack=True
)

try:

    channel.start_consuming()

except KeyboardInterrupt:

    channel.stop_consuming()
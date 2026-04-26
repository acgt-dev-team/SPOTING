import pika
from sqlmodel import Session
from db.config import engine
from db.model.imbasan import Imbasan
from db.model.profil_tugasan import ProfilTugasan
import json
from datetime import datetime, timezone

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

    body_str = body.decode('utf-8')

    body = json.loads(body_str)

    profil_tugasan_id = body['profil_tugasan_id']
    data_imbasan = body['data_imbasan']

    hasil_imbasan = Imbasan(
        x_profil_tugasan_id=profil_tugasan_id,
        data_imbasan=data_imbasan
    )

    with Session(engine) as session:
        session.add(hasil_imbasan)
        session.commit()
        session.refresh(hasil_imbasan)

    obj = session.get(ProfilTugasan, profil_tugasan_id)
    obj.selesai_pada = datetime.now(timezone.utc)
    obj.status_id = 3
    session.add(obj)
    session.commit()

    print('done update x_profil_tugasan id = ', obj.id)

channel.basic_consume(
    queue='tugasan_queue',
    on_message_callback=callback,
    auto_ack=True
)

try:

    channel.start_consuming()

except KeyboardInterrupt:

    channel.stop_consuming()
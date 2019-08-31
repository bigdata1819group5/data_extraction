from celery import Celery
import os
from requests import get
from kafka import KafkaProducer


redis_backend = os.environ.get('REDIS_BACKEND', 'redis://172.20.0.10:6379/0')

ENDPOINT = 'https://api.openstreetmap.org/api/0.6/trackpoints?bbox={}&page={}'
LEFT_BOTTOM = (35.6060, 51.2086)
RIGHT_TOP = (35.8056, 51.5753)
KAFKA_BROKER = os.environ.get('KAFKA_BROKER', 'localhost:19092')
JOB_PERIOD = os.environ.get('JOB_PERIOD', '60')

lastcontent = ''
app = Celery('tasks', broker=redis_backend)
app.conf.worker_concurrency = 1


@app.on_after_configure.connect
def setup_periodic_task(sender, **kwargs):
    sender.add_periodic_task(int(JOB_PERIOD), collect_data.s())


@app.task
def collect_data():
    global lastcontent

    area = ','.join(map(str, (LEFT_BOTTOM + RIGHT_TOP)))
    url = ENDPOINT.format(area, 0)
    rsp = get(url)

    if rsp.content != lastcontent:
        print('change')
        lastcontent = rsp.content
        producer = KafkaProducer(bootstrap_servers=[KAFKA_BROKER])
        producer.send('contents', value=rsp.content)
    else:
        print('nochange')

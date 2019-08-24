from celery import Celery
from celery.schedules import crontab
import os
from requests import get

lastcontent = ''
app = Celery('tasks', broker='redis://172.20.0.10:6379/0')

@app.on_after_configure.connect
def setup_periodic_task(sender, **kwargs):
    sender.add_periodic_task(10.0,test.s())


@app.task
def test():
    global lastcontent
    Endpoint='https://api.openstreetmap.org/api/0.6/trackpoints?bbox={}&page={}'
    DATa_dir='data/'
    LEFT_BOTTOM=(35.6060,51.2086)
    RIGHT_TOP=(35.8056,51.5753)
    area=','.join(map(str,(LEFT_BOTTOM + RIGHT_TOP)))
    url=Endpoint.format(area,0)
    rsp=get(url)

    if rsp.content != lastcontent :
        print('change')
        lastcontent=rsp.content
        path=os.path.join(DATa_dir,'tehran_{}.gpx'.format(1))
        with open(path,'wb') as f:
            f.write(rsp.content)
    else:
        print('nochange')
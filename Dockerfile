FROM python:3

ADD consume.py .
ADD requirements.txt

RUN pip install -r requirements.txt

CMD celery -A live_extract worker -B

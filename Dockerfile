FROM python:3

ADD live_extract.py .
ADD requirements.txt .

RUN pip install -r requirements.txt

RUN groupadd user && useradd --create-home --home-dir /home/app -g user user && \
    chown --recursive user:user .

USER user

CMD celery -A live_extract worker -B

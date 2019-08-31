FROM python:3

RUN groupadd user && useradd --create-home --home-dir /home/app -g user user
WORKDIR /home/app
RUN chown --recursive user:user .

ADD requirements.txt .
ADD live_extract.py .

RUN pip install -r requirements.txt

USER user
CMD celery -A live_extract worker -B

FROM python:3
ENV PYTHONUNBUFFERED 1

ADD requirements.txt /code/
RUN pip install -r /code/requirements.txt
RUN pip install git+https://github.com/aeternity/aepp-sdk-python.git@develop#egg=aeternity

RUN pip install gunicorn
EXPOSE 8000

ADD . /code/

RUN mkdir /srv/logs/

WORKDIR /code

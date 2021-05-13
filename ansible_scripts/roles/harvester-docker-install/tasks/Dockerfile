FROM python:3

RUN mkdir /harvester

COPY TwitterHarvester.py   /harvester

RUN pip install tweepy
RUN pip install couchdb

WORKDIR /harvester

CMD ["python", "TwitterHarvester.py"]
FROM python:3

RUN mkdir harvesterApp

COPY TwitterHarvester.py   harvesterApp

RUN pip install tweepy
RUN pip install couchdb

WORKDIR harvesterApp

CMD ["python3", "TwitterHarvester.py"]
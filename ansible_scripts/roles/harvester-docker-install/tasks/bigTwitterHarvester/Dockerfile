FROM python:3

RUN mkdir /harvester

COPY BigTwitterHarvester.py   /harvester

RUN pip install couchdb

WORKDIR /harvester

CMD ["python", "BigTwitterHarvester.py"]
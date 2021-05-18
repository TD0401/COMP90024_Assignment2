FROM python:3

RUN mkdir analysisApp

COPY analysis.py analysisApp
COPY AURIN_datasets analysisApp

RUN curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
RUN python3 get-pip.py
RUN pip install couchdb
RUN pip install pandas
RUN pip install numpy
RUN pip install nltk
RUN pip install corpora
RUN pip install empath
RUN pip install scikit-learn
RUN pip install gensim
RUN pip install matplotlib
RUN pip install seaborn
RUN pip install geojson
RUN pip install shapely

WORKDIR analysisApp

CMD ["python3", "analysis.py"]
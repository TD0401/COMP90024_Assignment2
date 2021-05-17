FROM python:3

RUN mkdir dashboardAPI

COPY app.py   dashboardAPI

RUN curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
RUN python3 get-pip.py
RUN pip install flask
RUN pip install flask-cors
RUN pip install requests

WORKDIR dashboardAPI
EXPOSE 5000

CMD ["python3", "app.py"]


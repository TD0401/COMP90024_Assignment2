FROM node:12.18.1

RUN mkdir dashboard

COPY code   dashboard

RUN npm install -g http-server


EXPOSE 8080
WORKDIR /

CMD ["http-server","." ,"0.0.0.0"]


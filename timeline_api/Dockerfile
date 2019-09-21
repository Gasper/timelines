
# Manual setup of the Timeline API using docker:
#
# docker network create timeline
# docker build -f Dockerfile --rm -t timeline_api .
# docker run -d --rm -p 27017:27017 --net timeline --name timeline-mongo mongo
# docker run -it --rm -p 5080:80 --net timeline --name timeline-api timeline_api

FROM nginx:stable-alpine

RUN apk add --no-cache bash python3 py3-pip uwsgi uwsgi-python3

COPY . /opt/timeline_api/
COPY ./build/nginx.conf /etc/nginx/nginx.conf

RUN pip3 install -r /opt/timeline_api/requirements.txt

ENV MONGO_HOST=timeline-mongo.timeline
ENV MONGO_PORT=27017

ENTRYPOINT [ "bash", "/opt/timeline_api/build/startup.sh" ]
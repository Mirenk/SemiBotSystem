FROM python:buster

RUN apt update && apt install -y nginx

RUN mkdir -p /app/matchingproj
WORKDIR /app/matchingproj

COPY matchingproj/requirements.txt /app/matchingproj/

RUN pip install -r requirements.txt

COPY /matchingproj/. /app/matchingproj/

RUN mkdir -p /tmp/matchingapis
COPY /matchingapis/. /tmp/matchingapis/
RUN /tmp/matchingapis/build.sh

RUN pip install /tmp/matchingapis/matching_pb

COPY nginx/nginx.conf /etc/nginx/conf.d/nginx.conf
COPY nginx/uwsgi_params /etc/nginx/uwsgi_params

RUN python manage.py collectstatic
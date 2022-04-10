FROM python:buster

RUN apt update && apt install -y nginx

RUN mkdir -p /app/semiproj
WORKDIR /app/semiproj

COPY semiproj/requirements.txt /app/semiproj/

RUN pip install -r requirements.txt

COPY /semiproj/. /app/semiproj/

RUN mkdir -p /tmp/matchingapis
COPY /matchingapis/. /tmp/matchingapis/
RUN /tmp/matchingapis/build.sh

RUN pip install /tmp/matchingapis/matching_pb

COPY nginx/nginx.conf /etc/nginx/conf.d/nginx.conf
COPY nginx/uwsgi_params /etc/nginx/uwsgi_params

RUN python manage.py collectstatic
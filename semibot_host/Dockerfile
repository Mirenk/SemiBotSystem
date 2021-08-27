FROM python

RUN mkdir -p /app/semibot
WORKDIR /app/semibot

COPY semibot/requirements.txt /app/semibot/

RUN pip install -r requirements.txt

COPY /semibot/. /app/semibot/
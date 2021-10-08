FROM python

RUN mkdir -p /app/semibot
WORKDIR /app/semibot

COPY semibot/requirements.txt /app/semibot/

RUN pip install -r requirements.txt

COPY /semibot/. /app/semibot/

RUN mkdir -p /tmp/matchingapis
COPY /matchingapis/. /tmp/matchingapis/
RUN /tmp/matchingapis/build.sh

RUN pip install /tmp/matchingapis/matching_pb
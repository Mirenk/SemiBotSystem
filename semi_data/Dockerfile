FROM python

RUN mkdir -p /app/dataproj
WORKDIR /app/dataproj

COPY dataproj/requirements.txt /app/dataproj/

RUN pip install -r requirements.txt

COPY /dataproj/. /app/dataproj/

RUN mkdir -p /tmp/matchingapis
COPY /matchingapis/. /tmp/matchingapis/
RUN /tmp/matchingapis/build.sh

RUN pip install /tmp/matchingapis/matching_pb
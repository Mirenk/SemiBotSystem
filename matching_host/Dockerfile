FROM python

RUN mkdir -p /app/matchingproj
WORKDIR /app/matchingproj

COPY matchingproj/requirements.txt /app/matchingproj/

RUN pip install -r requirements.txt

COPY /matchingproj/. /app/matchingproj/

RUN mkdir -p /tmp/matchingapis
COPY /matchingapis/. /tmp/matchingapis/
RUN /tmp/matchingapis/build.sh

RUN pip install /tmp/matchingapis/matching_pb
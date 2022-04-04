FROM python

RUN mkdir -p /app/semiproj
WORKDIR /app/semiproj

COPY semiproj/requirements.txt /app/semiproj/

RUN pip install -r requirements.txt

COPY /semiproj/. /app/semiproj/

RUN mkdir -p /tmp/matchingapis
COPY /matchingapis/. /tmp/matchingapis/
RUN /tmp/matchingapis/build.sh

RUN pip install /tmp/matchingapis/matching_pb
#!/usr/bin/env sh

cd `dirname $0`

rm -rf matching_host/matchingapis
rm -rf semi_app/matchingapis
rm -rf semi_data/matchingapis

cp -r matchingapis matching_host/
cp -r matchingapis semi_app/
cp -r matchingapis semi_data/

docker compose up -d --build
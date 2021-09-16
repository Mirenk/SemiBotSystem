#!/usr/bin/env sh

cd `dirname $0`

mkdir -p out

for file in `ls -1 matching_pb/*.proto`
do
  python3 -m grpc_tools.protoc -I./ -I ./vendor/googleapis/ --python_out=./out --grpc_python_out=./out ./"$file"
done

touch out/matching_pb/__init__.py
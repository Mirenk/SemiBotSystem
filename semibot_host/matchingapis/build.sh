#!/usr/bin/env sh

cd `dirname $0`

rm -rf matching_pb
mkdir -p matching_pb

for file in `ls -1 matching/*.proto`
do
  python3 -m grpc_tools.protoc -I./matching -I ./vendor/googleapis/ --python_out=./matching_pb --grpc_python_out=./matching_pb ./"$file"
done

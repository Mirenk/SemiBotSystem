#!/usr/bin/env sh

cd `dirname $0`

rm -rf matching_pb/matching_pb
mkdir -p matching_pb/matching_pb

echo "import sys" > matching_pb/matching_pb/__init__.py
echo "from pathlib import Path" >> matching_pb/matching_pb/__init__.py
echo "sys.path.append(str(Path(__file__).parent))" >> matching_pb/matching_pb/__init__.py

for file in `ls -1 matching/*.proto`
do
  python3 -m grpc_tools.protoc -I./matching -I ./vendor/googleapis/ --python_out=./matching_pb/matching_pb --grpc_python_out=./matching_pb/matching_pb ./"$file"
done

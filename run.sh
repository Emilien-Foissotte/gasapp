#!/bin/bash

set -euo pipefail;

if [ $# -lt 3 ]; then
  echo "Usage `basename $0` imagename containername port"
  exit 1
fi

IMAGENAME=${1:-gasapp:latest}
CONTAINERNAME=${2:-gasappcontainer}
PORT=${2:-8080}

docker run -it -p $PORT:8080 --rm --name $CONTAINERNAME $IMAGENAME

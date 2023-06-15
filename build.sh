#!/bin/bash

set -euo pipefail;

if [ $# -lt 2 ]; then
  echo "Usage `basename $0` imagename tag "
  exit 1
fi

IMAGENAME=${1:-gasapp}
TAGNAME=${2:-latest}

docker build . --tag $IMAGENAME:$TAGNAME

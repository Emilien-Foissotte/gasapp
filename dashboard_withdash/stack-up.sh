#!/bin/bash
set -euo pipefail

SCRIPT_DIR=$(cd $(dirname "${BASH_SOURCE[0]}") && pwd)
export DOCKER_BUILDKIT=1
docker-compose -f $SCRIPT_DIR/docker-compose.yml up -d --build
now=$(date --rfc-3339=ns)
echo "Build done at $now"
docker-compose -f $SCRIPT_DIR/docker-compose.yml logs -f --tail=20

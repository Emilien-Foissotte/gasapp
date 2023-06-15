#!/bin/bash
set -euo pipefail

SCRIPT_DIR=$(cd $(dirname "${BASH_SOURCE[0]}") && pwd)

docker-compose -f $SCRIPT_DIR/docker-compose.yml down --remove-orphans
now=$(date --rfc-3339=ns)
echo "Service stopped at $now"

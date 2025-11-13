#!/usr/bin/env bash
set -euo pipefail
curl -X POST http://localhost:8000/sms/inbound \
  -d 'From=%2B33600000000' \
  -d 'To=%2B15005550006' \
  -d 'Body=Test inbound'

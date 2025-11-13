#!/usr/bin/env bash
set -euo pipefail
curl -X POST http://localhost:8000/sms/status \
  -d 'MessageSid=SMxxxxxxxxxxxxxxxx' \
  -d 'MessageStatus=delivered'

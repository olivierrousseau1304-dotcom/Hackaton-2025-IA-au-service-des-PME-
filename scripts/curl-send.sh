#!/usr/bin/env bash
set -euo pipefail
curl -X POST http://localhost:8000/sms/send \
  -H "Content-Type: application/json" \
  -d '{"to":"+33XXXXXXXXX","body":"Hello from Hackprint ✅"}'

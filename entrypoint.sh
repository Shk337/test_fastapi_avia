#!/bin/bash
PATH="/app/venv/bin:$PATH"
LOG_LEVEL="${LOG_LEVEL:=info}"
exec uvicorn main:app --host 0.0.0.0 --port 3042 --reload --log-level $LOG_LEVEL
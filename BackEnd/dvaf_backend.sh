#!/bin/bash

cd /opt/dvaf_backend
/opt/dvaf_backend/venv/bin/gunicorn --bind 127.0.0.1:6000 --timeout=300 dvaf:app

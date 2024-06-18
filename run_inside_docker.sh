#!/bin/bash
creds_json_string="$(echo $GCP_AUTH_CREDS|base64 -d)"
./cloud-sql-proxy -j "${creds_json_string}" noted-terra-425611-e9:asia-south1:cura-app-pgdb --port 9999 &
uvicorn main:app --log-config=log_conf.yaml --host 0.0.0.0 --port "${PORT}" --workers 1
sleep 2
ps -ef|egrep "cloud-sql-proxy|uvicorn"
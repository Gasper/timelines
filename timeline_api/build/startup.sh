#!/bin/bash

cd /opt/timeline_api/
uwsgi -s /tmp/timeline_api.sock --plugin python3 --manage-script-name --mount /=api:flask_app --uid nginx &> /var/log/uwsgi/uwsgi.log &

nginx -g "daemon off;"
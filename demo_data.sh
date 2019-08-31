#!/bin/bash

# Populate the database with some demo data
docker exec timeline_timeline_api_1 python3 /opt/timeline_api/tools/bootstrap_demo_mongodb.py --host mongo.timeline_default

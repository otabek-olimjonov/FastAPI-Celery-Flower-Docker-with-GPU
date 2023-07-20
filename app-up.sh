#!/usr/bin/env bash
sudo docker-compose -f docker-compose.yml up --scale cpu_worker=5 --build
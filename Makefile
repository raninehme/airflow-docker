SHELL := /bin/bash

# Variables
PROJECT_NAME = $(notdir $(CURDIR)) # Current Folder Name

# Docker Environment Variables
export PROJECT_NAME

# +-+-+-+-+-+-+-
# a|I|R|F|L|O|W|
# +-+-+-+-+-+-+-
airflow-up: airflow-down
	docker-compose up --detach --build --remove-orphans
	-docker image prune --force

airflow-down:
	-docker-compose down --volumes --remove-orphans

airflow-start: airflow-stop
	-docker-compose start

airflow-stop:
	-docker-compose stop

airflow-clean:
	-docker-compose down --rmi 'all' --volumes --remove-orphans
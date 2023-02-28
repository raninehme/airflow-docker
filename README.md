# airflow-docker

## About
This is a repository for building Docker container of Apache Airflow using docker-compose simplified with a makefile


## Setup
* Install docker, docker-compose
* install make


## Run
1. `make airflow-up` to run a new airflow instance (it will always start a new instance)
   1. The webserver will be available on port 8080
2. `make airflow-down` to stop the Airflow instance & remove all resources
3. Check Makefile for more details and additional options

#### Additional Information
* Changes to the Dags will be automatically (1min) reflected in the webserver (UI)
* Replace the version in the Dockerfile from latest to the version you need
* Check .env file for any credentials or configuration.

## References and articles
* [Airflow Official - Docker](https://airflow.apache.org/docs/apache-airflow/stable/howto/docker-compose/index.html)
* [Airflow Docker Example](https://towardsdatascience.com/setting-up-apache-airflow-with-docker-compose-in-5-minutes-56a1110f4122)
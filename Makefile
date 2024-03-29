install:
	poetry install

build:
	./build.sh

lint:
	poetry run flake8 page_analyzer

dev:
	poetry run flask --app page_analyzer:app run

PORT ?= 8000
start:
	poetry run gunicorn -w 5 -b 0.0.0.0:$(PORT) page_analyzer:app

all:
	db-create database-load

load:
	psql python-project-83 < database.sql

start-debag:
	poetry run flask --app page_analyzer:app --debug run --port 8000
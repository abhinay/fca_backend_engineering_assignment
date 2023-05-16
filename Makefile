docker_run = docker run --env FLASK_ENV='development' --network=host --rm --mount type=bind,source="$(shell pwd)/",target=/root/ backend-engineer-assessment:0.0.1
test_docker_run = docker run --env FLASK_ENV='test' --rm --mount type=bind,source="$(shell pwd)/",target=/root/ backend-engineer-assessment:0.0.1

.DEFAULT_GOAL := help

.PHONY: help
help: ## Show available targets
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

.PHONY: build-docker-image
build-docker-image: ## Build the docker image and install python dependencies
	docker build --no-cache -t backend-engineer-assessment:0.0.1 .
	$(docker_run) pipenv install --dev

.PHONY: tidy
tidy: ## Tidy code
	$(docker_run) pipenv run tidy

.PHONY: lint
lint: ## Lint the code
	$(docker_run) pipenv run lint

.PHONY: test
test: ## Run tests
	$(test_docker_run) pipenv run test

.PHONY: ingest-data
ingest-data: ## Invoke the ingestion process
	$(docker_run) pipenv run python src/ingest.py data.csv

.PHONY: web
web: ## Run container
	$(docker_run) pipenv run flask --app=src/app.py run

.PHONY: run-query
run-query: ## Run an arbitrary query against the database (i.e. make query="select * from books" run-query)
	$(docker_run) sqlite3 warehouse.db "$(query)"

.PHONY: run
run: build-docker-image ingest-data web

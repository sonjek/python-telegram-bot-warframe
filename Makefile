CONTAINER_NAME  = tbot

.PHONY: help logs build clean rebuild
.DEFAULT_GOAL := help

help: ## Show this message
	@mawk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-0-9]+:.*?## / {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

build: ## Build and run container
	@docker-compose up --build -d

stop: ## Stop container
	@docker stop $(CONTAINER_NAME)

start: ## Start container
	@docker start $(CONTAINER_NAME)

restart: ## Stop and start container
	@docker stop $(CONTAINER_NAME)
	@docker start $(CONTAINER_NAME)

remove: ## Remove container
	@docker rm -f $(CONTAINER_NAME)

logs: ## Show container logs
	@docker logs --tail=10 -f $(CONTAINER_NAME)

clean: ## Remove container
	@docker-compose down -v --remove-orphans

rebuild: clean build logs ## Clean and rerun container

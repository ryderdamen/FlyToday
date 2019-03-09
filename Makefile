
.PHONY: install
install:
	@echo "Setting up Virtual Environment & Installing Requirements"; \
	virtualenv -p python3 env; \
	. env/bin/activate; \
	pip install -r src/requirements.txt; \
	echo "Please confirm gcloud CLI is installed"

.PHONY: deploy
deploy:
	@echo "Deploying to GCF as DEV_FlyTodayFulfillment"; \
	gcloud functions deploy DEV_FlyTodayFulfillment --entry-point main --runtime python37 --trigger-http --source ./src/ --project flytoday-912ec

.PHONY: deploy-prod
deploy-prod:
	@echo "Deploying to GCF as PROD (FlyTodayFulfillment)"; \
	gcloud functions deploy FlyTodayFulfillment --entry-point main --runtime python37 --trigger-http --source ./src/ --project flytoday-912ec

.PHONY: test
test:
	@echo "Running unit tests"; \
	. env/bin/activate; \
	pytest tests/

.PHONY: lint
lint:
	@echo "Linting Source -----------------"; \
	. env/bin/activate; \
	pycodestyle --max-line-length=120 ./src; \
	echo "Linting Tests -----------------"; \
	pycodestyle --max-line-length=120 ./tests

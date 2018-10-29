
.PHONY: install
install:
	source env/bin/activate
	pip install -r requirements.txt
	echo "Please confirm gcloud CLI is installed"

.PHONY: deploy
deploy:
	gcloud functions deploy FlyTodayFulfillment --entry-point main --runtime python37 --trigger-http --source ./src/ --project flytoday-912ec

.PHONY: test
test:
	pytest tests/

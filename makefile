.PHONY: build run test build-lambda docker-build docker-run

build:
	python -m venv .venv
	. .venv/bin/activate && pip install -r requirements.txt

run:
	uvicorn service.app.main:app --reload --port 8080

test:
	pytest -q

build-lambda:
	chmod +x kms/build_lambda.sh
	./kms/build_lambda.sh

docker-build:
	docker build -t capability-sandbox-service -f service/Dockerfile service

docker-run:
	docker run --rm -p 8080:8080 capability-sandbox-service
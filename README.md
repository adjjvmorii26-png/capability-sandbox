# capability-sandbox

## Quick start
1. Build and run dev stack
   make build
   docker-compose up --build

2. Run tests
   make test

3. Build Lambda artifact
   make build-lambda

## Structure
- service: FastAPI token service
- agents: autonomous agents using Redis Streams
- kms: key rotation and sweep tooling
- supervisor: policy microservice prototype
- tests: unit and integration tests

## Notes
- Replace ORCHESTRATOR_SECRET with a KMS or secret manager value.
- Dry-run defaults are safe; destructive operations require explicit flags.
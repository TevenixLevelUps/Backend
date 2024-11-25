DC = docker compose
EXEC = docker exec
LOGS = docker logs
ENV = --env-file .env
RABBIT_FILE = docker-compose.yaml
RABBIT_CONTAINER = rabbitmq
# APP_CONTAINER = main-app

.PHONY: rabbit
rabbit:
	${DC} -f ${RABBIT_FILE} ${ENV} up --build -d

.PHONY: rabbit-logs
rabbit-logs:
	${LOGS} ${RABBIT_CONTAINER} -f

# .PHONY: app-down
# app-down:
# 	${DC} -f ${APP_FILE} down

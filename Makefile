DC = docker compose
EXEC = docker exec
LOGS = docker logs

ENV = --env-file .env
SERVICES_ENV= --env-file services_service/.env
SPECIALISTS_ENV= --env-file specialists_service/.env
ORDERS_ENV= --env-file orders_service/.env

RABBIT_FILE = docker-compose.yaml
SERVICES_FILE = services_service/docker-compose.yaml
SPECIALISTS_FILE = specialists_service/docker-compose.yaml
ORDERS_FILE = orders_service/docker-compose.yaml

RABBIT_CONTAINER = rabbitmq
SERVICES_CONTAINER = service-app
SPECIALISTS_CONTAINER = specialist-app
ORDERS_CONTAINER = order-app 

.PHONY: rabbit
rabbit:
	${DC} -f ${RABBIT_FILE} ${ENV} up --build -d

.PHONY: rabbit-logs
rabbit-logs:
	${LOGS} ${RABBIT_CONTAINER} -f

.PHONY: all
all: rabbit services specialists orders

.PHONY: services
services:
	${DC} -f ${SERVICES_FILE} ${SERVICES_ENV} up --build -d

.PHONY: specialists
specialists:
	${DC} -f ${SPECIALISTS_FILE} ${SPECIALISTS_ENV} up --build -d

.PHONY: orders
orders:
	${DC} -f ${ORDERS_FILE} ${ORDERS_ENV} up --build -d

.PHONY: rabbit-down
rabbit-down:
	${DC} -f ${RABBIT_FILE} down

.PHONY: all-down
down: rabbit-down services-down specialists-down orders-down

.PHONY: services-down
services-down:
	${DC} -f ${SERVICES_FILE} down

.PHONY: specialists-down
specialists-down:
	${DC} -f ${SPECIALISTS_FILE} down

.PHONY: orders-down
orders-down:
	${DC} -f ${ORDERS_FILE} down

.PHONY: services-logs
services-logs:
	${LOGS} ${SERVICES_CONTAINER} -f

.PHONY: specialists-logs
specialists-logs:
	${LOGS} ${SPECIALISTS_CONTAINER} -f

.PHONY: orders-logs
orders-logs:
	${LOGS} ${ORDERS_CONTAINER} -f

.PHONY: test-services
test-services:
	${EXEC} ${SERVICES_CONTAINER} pytest $(path)

.PHONY: test-specialists
test-specialists:
	${EXEC} ${SPECIALISTS_CONTAINER} pytest $(path)

.PHONY: test-orders
test-orders:
	${EXEC} ${ORDERS_CONTAINER} pytest $(path)

.PHONY: test-cov-services
test-cov-services:
	${EXEC} ${SERVICES_CONTAINER} pytest --cov=$(path)

.PHONY: test-cov-specialists
test-cov-specialists:
	${EXEC} ${SPECIALISTS_CONTAINER} pytest --cov=$(path)

.PHONY: test-cov-orders
test-cov-orders:
	${EXEC} ${ORDERS_CONTAINER} pytest --cov=$(path)


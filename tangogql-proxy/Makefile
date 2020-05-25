

build:
	@docker build -t tangogql-proxy:1.0.0 -f Dockerfile .

start: 
	@docker run -d -p=5000:5000 --env AUTH_URL=http://192.168.93.69:32763/login --env TANGOGQL_URL=http://192.168.93.69:32762/db --name tangogql-proxy tangogql-proxy:1.0.0

stop:
	@docker stop tangogql-proxy || true; \
	docker rm tangogql-proxy || true

all: build start
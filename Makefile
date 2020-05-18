

build:
	docker build -t tango-exporter:1.0.0 -f Dockerfile .

deploy:
	kubectl apply -f yaml/deployment.yaml -f yaml/service.yaml

delete:
	kubectl delete -f yaml/deployment.yaml -f yaml/service.yaml || true

curl: 
	./get_metrics.sh

all: build delete deploy
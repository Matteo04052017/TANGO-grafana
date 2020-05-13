


build:
	docker build -t tango-exporter:1.0.0 -f Dockerfile .

deploy:
	kubectl apply -f yaml/deployment.yaml -f yaml/service.yaml

delete:
	kubectl delete -f yaml/deployment.yaml -f yaml/service.yaml

curl: 
	curl $(kubectl get svc -n integration -o jsonpath='{.items[?(@.metadata.name=="tango-exporter-service")].spec.clusterIP}')/metrics

all: build delete deploy
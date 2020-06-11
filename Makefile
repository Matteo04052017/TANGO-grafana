
CHART_VERSION=1.0.0
DIRS = exporter grafana tangogql-proxy
BUILDDIRS = $(DIRS:%=build-%)
PUSHDIRS = $(DIRS:%=push-%)
HELM_HOST ?= https://nexus.engageska-portugal.pt

.DEFAULT_GOAL := help

build: $(DIRS)  ## build all images
$(DIRS): $(BUILDDIRS)
$(BUILDDIRS):
	$(MAKE) -C $(@:build-%=%) build

push: $(PUSHDIRS)  ## push images to Docker hub
$(PUSHDIRS):
	$(MAKE) -C $(@:push-%=%) push

help:  ## show this help.
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

publish-chart: ## publish chart on the 
	@helm package helm-chart && \
	curl -v -u $(HELM_USERNAME):$(HELM_PASSWORD) --upload-file tango-grafana-$(CHART_VERSION).tgz $(HELM_HOST)/repository/helm-chart/tango-grafana-$(CHART_VERSION).tgz

install-chart: ## install the tango-grafana helm chart on the namespace tango-grafana
	helm install tango-grafana0 helm-chart/ --namespace tango-grafana 

uninstall-chart: ## uninstall the tango-grafana helm chart on the namespace tango-grafana
	helm template  tango-grafana0 helm-chart/ --namespace tango-grafana | kubectl delete -f - ; \
	helm uninstall tango-grafana0 --namespace tango-grafana

reinstall-chart: uninstall-chart install-chart ## reinstall the tango-grafana helm chart on the namespace tango-grafana

upgrade-chart: ## upgrade the tango-grafana helm chart on the namespace tango-grafana
	helm upgrade tango-grafana0 helm-chart/ --namespace tango-grafana

.PHONY: subdirs $(DIRS)
.PHONY: subdirs $(BUILDDIRS)
.PHONY: subdirs $(PUSHDIRS)
.PHONY: build push help
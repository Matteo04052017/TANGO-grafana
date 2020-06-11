#
#   Copyright 2015  Xebia Nederland B.V.
#   Modifications copyright (c) 2019 SKA Organisation
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.
#
NAME?=$(shell basename $(CURDIR))

ifeq ($(strip $(DOCKER_REGISTRY_HOST)),)
  DOCKER_REGISTRY_HOST = nexus.engageska-portugal.pt
endif

ifeq ($(strip $(DOCKER_REGISTRY_USER)),)
  DOCKER_REGISTRY_USER = ska-docker
endif

IMAGE?=$(DOCKER_REGISTRY_HOST)/$(DOCKER_REGISTRY_USER)/$(NAME)

VERSION?=1.0.0
TAG?=1.0.0

SHELL=/bin/bash

DOCKER_BUILD_CONTEXT=.
DOCKER_FILE_PATH=Dockerfile

.PHONY: pre-build docker-build post-build build release patch-release minor-release major-release tag check-status check-release showver \
	push pre-push do-push post-push

build: pre-build docker-build post-build

pre-build:

post-build:

pre-push:

post-push:

docker-build: 
	docker build $(DOCKER_BUILD_ARGS) -t $(IMAGE):$(VERSION) $(DOCKER_BUILD_CONTEXT) -f $(DOCKER_FILE_PATH) --build-arg DOCKER_REGISTRY_HOST=$(DOCKER_REGISTRY_HOST) --build-arg DOCKER_REGISTRY_USER=$(DOCKER_REGISTRY_USER)
	@DOCKER_MAJOR=$(shell docker -v | sed -e 's/.*version //' -e 's/,.*//' | cut -d\. -f1) ; \
	DOCKER_MINOR=$(shell docker -v | sed -e 's/.*version //' -e 's/,.*//' | cut -d\. -f2) ; \
	if [ $$DOCKER_MAJOR -eq 1 ] && [ $$DOCKER_MINOR -lt 10 ] ; then \
		echo docker tag -f $(IMAGE):$(VERSION) $(IMAGE):latest ;\
		docker tag -f $(IMAGE):$(VERSION) $(IMAGE):latest ;\
	else \
		echo docker tag $(IMAGE):$(VERSION) $(IMAGE):latest ;\
		docker tag $(IMAGE):$(VERSION) $(IMAGE):latest ; \
	fi

push: pre-push do-push post-push

do-push:
	docker push $(IMAGE):$(VERSION)
	docker push $(IMAGE):latest

snapshot: build push

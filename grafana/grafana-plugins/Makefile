PLUGINS ?= ajax-panel grafana-plotly-panel tango-attribute tango-command

build:
	@for plugin in $(PLUGINS); do \
	cd $$chartname; yarn install; yarn dev; \
	done
#FROM grafana/grafana:7.0.3

# ADD grafana-plugins /var/lib/grafana/plugins/

# RUN cd /var/lib/grafana/plugins/ajax-panel && yarn install && yarn build
# RUN cd /var/lib/grafana/plugins/grafana-plotly-panel && yarn install && yarn build 
# RUN cd /var/lib/grafana/plugins/tango-attribute && yarn install && yarn build 
# RUN cd /var/lib/grafana/plugins/tango-command && yarn install && yarn build

# FROM grafana/grafana:7.0.3

# COPY --from=js-builder /var/lib/grafana/plugins /var/lib/grafana/plugins



ARG GRAFANA_VERSION="7.0.3"

FROM grafana/grafana:${GRAFANA_VERSION}

USER root

ARG GF_INSTALL_IMAGE_RENDERER_PLUGIN="false"

ENV GF_PATHS_PLUGINS="/var/lib/grafana-plugins"

RUN mkdir -p "$GF_PATHS_PLUGINS" && \
    chown -R grafana:grafana "$GF_PATHS_PLUGINS"

ADD grafana-plugins "$GF_PATHS_PLUGINS"

RUN apk add yarn; \
    for plugin in ${GF_PATHS_PLUGINS}/*; do \
        cd ${plugin}; \
        yarn install; \
        yarn build; \
    done; 

RUN if [ $GF_INSTALL_IMAGE_RENDERER_PLUGIN = "true" ]; then \
    echo "http://dl-cdn.alpinelinux.org/alpine/edge/community" >> /etc/apk/repositories && \
    echo "http://dl-cdn.alpinelinux.org/alpine/edge/main" >> /etc/apk/repositories && \
    echo "http://dl-cdn.alpinelinux.org/alpine/edge/testing" >> /etc/apk/repositories && \
    apk --no-cache  upgrade && \
    apk add --no-cache udev ttf-opensans chromium && \
    rm -rf /tmp/* && \
    rm -rf /usr/share/grafana/tools/phantomjs; \
fi

USER grafana

ENV GF_RENDERER_PLUGIN_CHROME_BIN="/usr/bin/chromium-browser"

RUN if [ $GF_INSTALL_IMAGE_RENDERER_PLUGIN = "true" ]; then \
    grafana-cli \
        --pluginsDir "$GF_PATHS_PLUGINS" \
        --pluginUrl https://github.com/grafana/grafana-image-renderer/releases/latest/download/plugin-linux-x64-glibc-no-chromium.zip \
        plugins install grafana-image-renderer; \
fi

ARG GF_INSTALL_PLUGINS=""

RUN if [ ! -z "${GF_INSTALL_PLUGINS}" ]; then \
    OLDIFS=$IFS; \
        IFS=','; \
    for plugin in ${GF_INSTALL_PLUGINS}; do \
        IFS=$OLDIFS; \
        grafana-cli --pluginsDir "$GF_PATHS_PLUGINS" plugins install ${plugin}; \
    done; \
fi

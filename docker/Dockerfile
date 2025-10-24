FROM docker.n8n.io/n8nio/n8n

USER root

# Install Chrome dependencies and Chrome
RUN apk add --no-cache \
    chromium \
    nss \
    glib \
    freetype \
    freetype-dev \
    harfbuzz \
    ca-certificates \
    ttf-freefont \
    udev \
    ttf-liberation \
    font-noto-emoji

# Tell Puppeteer to use installed Chrome instead of downloading it
ENV PUPPETEER_SKIP_CHROMIUM_DOWNLOAD=true \
    PUPPETEER_EXECUTABLE_PATH=/usr/bin/chromium-wrapper

# Install n8n-nodes-puppeteer in a permanent location
RUN mkdir -p /opt/n8n-custom-nodes && \
    cd /opt/n8n-custom-nodes && \
    npm install n8n-nodes-puppeteer && \
    chown -R node:node /opt/n8n-custom-nodes

# Create a wrapper script for Chromium with safe Docker flags
RUN echo '#!/bin/sh' > /usr/bin/chromium-wrapper && \
    echo 'exec /usr/bin/chromium \
    --no-sandbox \
    --disable-setuid-sandbox \
    --disable-dev-shm-usage \
    --disable-gpu \
    --no-first-run \
    --no-zygote \
    --single-process \
    --disable-extensions \
    --disable-background-timer-throttling \
    --disable-renderer-backgrounding \
    --disable-backgrounding-occluded-windows \
    "$@"' >> /usr/bin/chromium-wrapper && \
    chmod +x /usr/bin/chromium-wrapper

# Copy our custom entrypoint
COPY docker/docker-custom-entrypoint.sh /docker-custom-entrypoint.sh
RUN chmod +x /docker-custom-entrypoint.sh && \
    chown node:node /docker-custom-entrypoint.sh

USER node

ENTRYPOINT ["/docker-custom-entrypoint.sh"]

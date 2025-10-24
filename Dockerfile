FROM docker.n8n.io/n8nio/n8n

USER root

# Install system dependencies for Puppeteer (headless Chrome) on Alpine
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
    PUPPETEER_EXECUTABLE_PATH=/usr/bin/chromium

# Install the community node globally (no build step needed)
USER node
RUN npm install --location=global n8n-nodes-puppeteer

USER root

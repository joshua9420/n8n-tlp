FROM docker.n8n.io/n8nio/n8n

# Install system dependencies for Puppeteer (headless Chrome) on Alpine
RUN apk add --no-cache \
    chromium \
    nss \
    freetype \
    harfbuzz \
    ttf-freefont \
    nodejs \
    yarn

# Install n8n community Puppeteer node
USER node
RUN npm install --location=global n8n-nodes-puppeteer
USER root

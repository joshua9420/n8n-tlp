# n8n-tlp

This repository contains a Docker Compose setup for n8n with Puppeteer support and LightRAG integration.

## Services

- **n8n**: Workflow automation platform with Puppeteer node
- **Traefik**: Reverse proxy with SSL certificates
- **PostgreSQL**: Database for n8n
- **Qdrant**: Vector database for LightRAG
- **LightRAG**: RAG (Retrieval-Augmented Generation) server

## Access URLs

- **n8n**: https://n8n.srv1075445.hstgr.cloud
- **LightRAG Dashboard**: https://rag.srv1075445.hstgr.cloud

## Authentication

### LightRAG Dashboard
- **URL**: https://rag.srv1075445.hstgr.cloud
- **Username**: admin
- **Password**: H6s2QLkWFOYsvmO7EuFtgseZmmHokPBR2uUrjFb6djw=

*Note: Change the password in the `.env` file for production use*

## Setup Instructions

1. Clone this repository
2. Copy `.env.example` to `.env` and configure your settings
3. Update domain names in `.env` file
4. Run: `docker-compose up -d`

## Security Features

- SSL/TLS certificates via Let's Encrypt
- HTTP Basic Authentication for LightRAG
- Secure password generation
- Network isolation between services

## Generating New Passwords

To generate a new password for LightRAG:

```bash
# Generate a secure password
openssl rand -base64 32

# Generate the hash for Traefik
./generate-auth.sh admin "your_new_password"

# Update the RAG_PASSWORD_HASH in .env file
```

## DNS Setup

Make sure to configure your DNS to point the following subdomains to your server:
- `n8n.srv1075445.hstgr.cloud` → Your server IP
- `rag.srv1075445.hstgr.cloud` → Your server IP

## Environment Variables

Key environment variables in `.env`:
- `DOMAIN_NAME`: Your base domain
- `SUBDOMAIN`: Subdomain for n8n
- `LR_SUBDOMAIN`: Subdomain for LightRAG
- `RAG_USERNAME`: Basic auth username for LightRAG
- `RAG_PASSWORD`: Basic auth password for LightRAG
- `RAG_PASSWORD_HASH`: Hashed password for Traefik

## Troubleshooting

### LightRAG Not Accessible
1. Check DNS configuration
2. Verify Traefik labels in docker-compose.yml
3. Check SSL certificate generation in Traefik logs
4. Verify authentication credentials

### SSL Certificate Issues
1. Check that port 80 and 443 are open
2. Verify DNS propagation
3. Check Traefik logs: `docker-compose logs traefik`

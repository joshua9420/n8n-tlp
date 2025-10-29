#!/bin/bash

# Script to generate Traefik Basic Auth hash
# Usage: ./generate-auth.sh username password

if [ "$#" -ne 2 ]; then
    echo "Usage: $0 <username> <password>"
    echo "Example: $0 admin mypassword123"
    exit 1
fi

USERNAME="$1"
PASSWORD="$2"

# Generate hash using htpasswd format (Apache MD5)
HASH=$(openssl passwd -apr1 "$PASSWORD")

# Create the auth string in Traefik format
AUTH_STRING="${USERNAME}:${HASH}"

echo "Add this to your .env file:"
echo "RAG_PASSWORD_HASH=\"${AUTH_STRING}\""
echo ""
echo "Full auth string for testing:"
echo "${AUTH_STRING}"
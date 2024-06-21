#!/bin/sh

# Directory where certificates will be stored
CERT_DIR="/certs"

# Check if the certificates already exist
if [ ! -f "$CERT_DIR/_wildcard.pem" ] || [ ! -f "$CERT_DIR/_wildcard.key.pem" ]; then
    echo "Certificates not found, generating new ones..."
    openssl genpkey -algorithm RSA -out "$CERT_DIR/_wildcard.key.pem" -pkeyopt rsa_keygen_bits:2048
    openssl req -new -key "$CERT_DIR/_wildcard.key.pem" -out "$CERT_DIR/_wildcard.csr" -subj "/CN=*.${DOMAIN}"
    openssl x509 -req -days 365 -in "$CERT_DIR/_wildcard.csr" -signkey "$CERT_DIR/_wildcard.key.pem" -out "$CERT_DIR/_wildcard.pem"
else
    echo "Certificates already exist, skipping generation..."
fi
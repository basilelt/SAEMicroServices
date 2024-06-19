# Builder SSL
FROM alpine:3.20 as openssl

ARG DOMAIN
ENV DOMAIN=${DOMAIN}

RUN apk add --no-cache openssl
WORKDIR /certs

RUN openssl genpkey -algorithm RSA -out _wildcard.key.pem -pkeyopt rsa_keygen_bits:2048
RUN openssl req -new -key _wildcard.key.pem -out _wildcard.csr -subj "/CN=*.${DOMAIN}"
RUN openssl x509 -req -days 365 -in _wildcard.csr -signkey _wildcard.key.pem -out _wildcard.pem

# Traefik
FROM traefik:v3.0

COPY --from=openssl /certs/_wildcard.pem /certs/
COPY --from=openssl /certs/_wildcard.key.pem /certs/

VOLUME /certs
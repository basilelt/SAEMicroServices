FROM alpine:3.20

ARG DOMAIN
ENV DOMAIN=${DOMAIN}

RUN apk add --no-cache openssl
WORKDIR /certs

COPY generate-certs.sh /usr/local/bin/generate-certs.sh
RUN chmod +x /usr/local/bin/generate-certs.sh

RUN /usr/local/bin/generate-certs.sh
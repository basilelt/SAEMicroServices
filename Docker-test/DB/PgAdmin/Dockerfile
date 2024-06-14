# Stage 1
FROM alpine:3.20 as builder

RUN apk add --no-cache bash curl jq

ARG POSTGRES_DB
ARG POSTGRES_USER
ARG POSTGRES_PASSWORD

ENV POSTGRES_DB=${POSTGRES_DB} \
    POSTGRES_USER=${POSTGRES_USER} \
    POSTGRES_PASSWORD=${POSTGRES_PASSWORD}

ADD ./generate_servers_json.sh /generate_servers_json.sh
RUN chmod +x /generate_servers_json.sh && /generate_servers_json.sh > /servers.json

# Final stage
FROM dpage/pgadmin4:8.8
COPY --from=builder /servers.json /pgadmin4/servers.json

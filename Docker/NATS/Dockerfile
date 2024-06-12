FROM nats:2.10.16

WORKDIR /app
COPY nats.conf /app/nats.conf

EXPOSE 4222

CMD ["nats-server", "-c", "/app/nats.conf"]
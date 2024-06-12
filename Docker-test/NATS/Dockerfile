FROM nats:2.10

WORKDIR /app
ADD ./nats.conf /app/nats.conf

CMD ["nats-server", "-c", "/app/nats.conf"]
FROM python:3.12

COPY ./NATS/banque /app

RUN set -ex \
    && python -m venv /env \
    && /env/bin/pip install --upgrade pip \
    && /env/bin/pip install --no-cache-dir -r /app/requirements.txt

WORKDIR /app

ENV VIRTUAL_ENV /env
ENV PATH /env/bin:$PATH

CMD ["python", "banque.py"]
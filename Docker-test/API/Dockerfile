FROM python:3.12

ADD ./Django_api/ /app

RUN set -ex \
    && python -m venv /env \
    && /env/bin/pip install --upgrade pip \
    && /env/bin/pip install --no-cache-dir -r /app/requirements.txt

WORKDIR /app/airline

ENV VIRTUAL_ENV /env
ENV PATH /env/bin:$PATH

COPY ./Docker-test/API/entrypoint.sh /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]

EXPOSE 80
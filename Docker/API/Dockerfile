FROM python:3.12

ADD ../../../Django_api/ /app

RUN set -ex \
    && python -m venv /env \
    && /env/bin/pip install --upgrade pip \
    && /env/bin/pip install --no-cache-dir -r /app/requirements.txt

WORKDIR /app/airline

ENV VIRTUAL_ENV /env
ENV PATH /env/bin:$PATH

RUN python manage.py djecrety -s

CMD ["daphne", "-b", "0.0.0.0", "-p", "8000", "airline.asgi:application"]

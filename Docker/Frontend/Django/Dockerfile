FROM python:3.12

ADD ./Django_Frontend/ /app

RUN set -ex \
    && python -m venv /env \
    && /env/bin/pip install --upgrade pip \
    && /env/bin/pip install --no-cache-dir -r /app/requirements.txt

WORKDIR /app/monprojet

ENV VIRTUAL_ENV /env
ENV PATH /env/bin:$PATH

CMD ["daphne", "-b", "0.0.0.0", "-p", "80", "monprojet.asgi:application"]

EXPOSE 80

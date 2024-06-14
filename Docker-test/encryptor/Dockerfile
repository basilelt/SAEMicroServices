# Stage 1: Encrypt passwords
FROM python:3.12-slim

RUN pip install bcrypt
COPY encrypt.py /encrypt.py

ARG PGADMIN_DEFAULT_PASSWORD_CLEAR
ENV PGADMIN_DEFAULT_PASSWORD_CLEAR=${PGADMIN_DEFAULT_PASSWORD_CLEAR}

CMD ["sh", "-c", "python /encrypt.py PGADMIN_DEFAULT_PASSWORD_CLEAR > /pgadmin.env"]
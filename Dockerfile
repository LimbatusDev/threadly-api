FROM python:3.8

ENV PYTHONUNBUFFERED=1

# Env vars
ENV DJANGO_SETTINGS_MODULE ${DJANGO_SETTINGS_MODULE}
# QvaPay secrets
ENV QVAPAY_APP_ID ${QVAPAY_APP_ID}
ENV QVAPAY_APP_SECRET ${QVAPAY_APP_SECRET}
# Config secrets
ENV REDIS_URL ${REDIS_URL}
ENV SECRET_KEY ${SECRET_KEY}
ENV SECRET_TOKEN ${SECRET_TOKEN}
# Twitter secrets
ENV TWITTER_API_KEY ${TWITTER_API_KEY}
ENV TWITTER_API_KEY_SECRET ${TWITTER_API_KEY_SECRET}
# database secrets
ENV DB_NAME ${DB_NAME}
ENV DB_HOST ${DB_HOST}
ENV DB_PORT ${DB_PORT}
ENV DB_USER ${DB_USER}
ENV DB_PASSWORD ${DB_PASSWORD}

WORKDIR /code

RUN pip3 install --upgrade pip
# Install poetry
RUN curl -sSL https://install.python-poetry.org | python3 -
ENV PATH="/root/.local/bin:$PATH"

COPY pyproject.toml poetry.lock /code/
RUN poetry export -f requirements.txt --output requirements.txt --without-hashes
RUN pip install -r requirements.txt

COPY . /code/
RUN mkdir /code/logs

RUN chmod +x manage.py
RUN chmod +x entrypoint.sh
CMD python3 ./manage.py migrate --no-input; \
    python3 ./manage.py collectstatic --no-input; \
    ./entrypoint.sh
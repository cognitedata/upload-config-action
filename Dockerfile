FROM python:3.10

WORKDIR /

COPY poetry.lock .
COPY pyproject.toml .
COPY cognite cognite

RUN set -ex && pip install --upgrade pip && pip install poetry

RUN poetry install --no-dev

ENTRYPOINT [ "poetry", "run", "upload" ]
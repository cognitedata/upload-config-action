FROM python:3.11

WORKDIR /

COPY poetry.lock .
COPY pyproject.toml .
COPY cognite cognite

RUN set -ex && pip install --upgrade pip && pip install poetry

RUN poetry config virtualenvs.create false
RUN poetry install --no-dev

ENTRYPOINT [ "python", "/cognite/config_upload/__main__.py", "upload" ]
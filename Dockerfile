FROM python:3.10-slim

WORKDIR /

COPY poetry.lock .
COPY pyproject.toml .
COPY cognite/ .

RUN pip3 install poetry
RUN poetry config virtualenvs.create false

RUN pip3 install --target=/app -r requirements.txt --no-deps

RUN poetry install --no-dev

ENTRYPOINT [ "poetry", "run", "upload" ]
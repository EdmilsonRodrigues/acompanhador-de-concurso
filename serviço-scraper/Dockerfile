FROM python:3.13

WORKDIR /app

RUN pip install poetry && poetry config virtualenvs.create false

COPY arquivos/ ./arquivos

COPY pyproject.toml poetry.lock ./

RUN poetry install --no-root

COPY src/ .

ENTRYPOINT ["poetry", "run", "python", "-m", "serviço_scraper.app"]
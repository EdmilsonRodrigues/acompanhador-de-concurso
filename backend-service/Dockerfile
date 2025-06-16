FROM python:3.13

WORKDIR /app

RUN pip install poetry && poetry config virtualenvs.create false

COPY pyproject.toml poetry.lock ./

RUN poetry install --no-root

COPY backend_service/ .

ENTRYPOINT ["poetry", "run", "fastapi", "run", "main.py"]

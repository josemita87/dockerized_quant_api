FROM python:3.12-slim

RUN pip3 install poetry

WORKDIR /app
COPY . /app

RUN poetry install
CMD ["poetry", "run", "python", "src/main.py"]
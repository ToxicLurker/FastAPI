FROM python:3.8.2

RUN mkdir app

COPY . /app

RUN cd app \
    && pip install poetry \
    && poetry install

CMD ["poetry", "run", "uvicorn", "src.test_project.funcs:app", "--reload", "--host", "0.0.0.0", "--port", "80"]
# CMD ["sleep", "1000"]

WORKDIR /app